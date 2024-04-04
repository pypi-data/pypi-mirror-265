#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_api
# @Time         : 2024/4/3 16:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

base_url = os.getenv("SUNO_BASE_URL")


def custom_generate_audio(payload):
    """
    {
      "prompt": "歌词",
      "tags": "pop metal male melancholic",
      "title": "歌名",
      "make_instrumental": False,
      "wait_audio": False,
    }

    :param payload:
    :return:
    """
    url = f"{base_url}/api/custom_generate"
    response = httpx.post(url, json=payload)
    return response.json()


def generate_audio_by_prompt(payload):
    """
    {
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "wait_audio": False
    }
    :param payload:
    :return:
    """
    url = f"{base_url}/api/generate"
    response = httpx.post(url, json=payload)
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = httpx.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = httpx.get(url)
    return response.json()


def func(s):
    """df[["audio_url", "video_url", "image_url"]]"""
    if s.endswith(".mp3"):
        return f"[🎧点击听歌]({s})"

    elif s.endswith(".mp4"):
        return f"[🖥点击观看]({s})"

    elif s.endswith(".png"):
        return f"![🖼]({s})"

    else:
        return s


def song_info(df):
    return f"""
🎵 **「{df['title'][0]}」**

`{df['tags'][0]}`

```toml
{df['lyric'][0]}
```


{df[["audio_url", "video_url", "image_url"]].map(func).to_markdown(index=False)}
    """


from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.smooth_queue import SmoothQueue

from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.schemas.suno_types import SunoRequest
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk

from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse


class Completions(object):

    def __init__(self, api_key):
        self.httpx_aclient = httpx.AsyncClient(base_url=os.getenv("SUNO_BASE_URL", api_key), follow_redirects=True)

    async def acreate(self, request: ChatCompletionRequest):
        async for content in self._acreate(request):
            chat_completion_chunk.choices[0].delta.content = content
            yield chat_completion_chunk
        # 结束标识
        chat_completion_chunk.choices[0].delta.content = ""
        chat_completion_chunk.choices[0].finish_reason = "stop"
        yield chat_completion_chunk

    async def _acreate(self, request: ChatCompletionRequest):
        if request.model.startswith("suno-custom"):  # todo: gpt解析入参
            payload = {
                "prompt": request.messages[-1]["content"],
                # "tags": "歌曲风格（英文）",
                # "title": "歌名",
            }
            df = await self.custom_generate(payload)
        else:
            payload = {
                "prompt": request.messages[-1]["content"],
                "make_instrumental": False,
                "wait_audio": False
            }
            df = await self.generate_by_prompt(payload)

        ids = ','.join(df['id'].tolist())

        yield f"""```\nTask ids: {ids}\n```\n"""
        yield f"""[任务执行]("""

        for i in range(100):
            yield f"""{'🎵' if i % 2 else '🔥'}"""
            await asyncio.sleep(5)

            if i > 20:  # 100秒后才开始回调
                df = await self.get_information(ids)

                # logger.debug("回调歌曲")

                if all(df.status == 'complete'):
                    yield f""")💯"""
                    break

        yield song_info(df)

    def create_sse(self, request: ChatCompletionRequest):
        return openai_response2sse(self.acreate(request), redirect_model=request.model)

    async def custom_generate(self, payload):
        response = await self.httpx_aclient.post("/api/custom_generate", json=payload)
        return pd.DataFrame(response.json())

    async def generate_by_prompt(self, payload):
        response = await self.httpx_aclient.post("/api/generate", json=payload)
        return pd.DataFrame(response.json())

    async def get_information(self, ids):
        response = await self.httpx_aclient.get(f"/api/get?ids={ids}")
        return pd.DataFrame(response.json())


if __name__ == '__main__':
    data = generate_audio_by_prompt({
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)
