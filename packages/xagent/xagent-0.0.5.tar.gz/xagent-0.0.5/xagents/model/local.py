#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/02/20 15:47:53
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from typing import List, Dict


import requests
import re
from snippets import *
from xagents.model.core import LLM, EMBD

from loguru import logger


def call_local_embedding(url: str, contents: List[str], norm=True) -> List[List[float]]:
    # embeddings = []
    # url = "http://36.103.177.140:8001/v2/embeddings"
    resp = requests.post(url=url, json=dict(texts=contents, norm=norm))
    resp.raise_for_status()
    return resp.json()["data"]['embeddings']


class ZhipuLocalEmbedding(EMBD):

    def __init__(self,  url="http://36.103.177.140:8001/v2/embeddings", batch_size=16, norm=True):
        self.batch_size = batch_size
        self.norm = norm
        self.url = url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        logger.info(f"embedding {len(texts)} with {self.batch_size=}")

        embeddings = []
        from tqdm import tqdm

        for idx, batch in tqdm(enumerate(batchify(texts, self.batch_size))):
            try:
                embds = call_local_embedding(url=self.url, contents=batch, norm=self.norm)
                embeddings.extend(embds)
                pct = idx*self.batch_size/len(texts)
                logger.info(f"{idx*self.batch_size}/{len(texts)} [{pct:2.2%}] embeddings done")
            except Exception as e:
                logger.error(f"embedding service error")
                logger.error(batch)
                raise e
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        embedding = call_local_embedding(url=self.url, contents=[text], norm=self.norm)[0]
        return embedding

    @classmethod
    def get_dim(cls) -> int:
        return 1024


class LocalLLM(LLM):
    """
    本地调用LLM
    """

    @classmethod
    def list_versions(cls):
        return [
            "v1.0.0",
        ]

    def __init__(self, url, name="LocalGLM", version="v1.0.0"):
        super().__init__(name=name, version=version)
        self.url = url

    def generate(self, messages, stream=False, temperature=0.01, **kwargs):

        response = self.__call_glm3_chat(messages=messages, stream=stream,
                                         temperature=temperature, **kwargs)
        resp_message = response
        return (e for e in resp_message) if stream else "".join(resp_message)

    def __call_glm3_chat(self, messages: List[Dict], stream=False, temperature=0.01,
                         top_p=0.7, max_new_token=1024, do_sample=True, **kwargs):

        # prompt拼接
        prompt = ""
        if messages:
            for ele in messages:
                role = ele["role"]
                assert role in ["system", "user", "assistant"], f"invalid role : {role} "
                content = ele["content"]
                prompt += f"<|{role}|>\n{content}\n"
            prompt += "<|assistant|>\n"

        # data传参
        data = {
            "inputs": prompt,
            "stream": stream,
            "parameters": {
                "do_sample": do_sample,
                "temperature": temperature,
                "top_p": top_p,
                "max_new_tokens": max_new_token,
                "seed": None,
                "stop":  ["<|endoftext|>", "<|user|>", "<|observation|>"]
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }

        logger.debug(f"data: {data}")
        resp = requests.post(self.url, headers=headers, json=data, stream=stream)
        resp.raise_for_status()

        # 调用url
        try:
            if stream:
                for content in resp:
                    content_decode = content.decode('utf-8', "ignore")
                    content_decode_res = ''.join(re.findall(r'text":"(.*?)"', content_decode))
                    if content_decode_res not in ["<|endoftext|>", "<|user|>", "<|observation|>", ""]:
                        yield content_decode_res
                    else:
                        continue
            else:
                yield resp.json()[0]["generated_text"]
        except Exception as e:
            logger.error(f"LLM generate error")
            logger.error(prompt)

            raise e


if __name__ == "__main__":

    # zeta_llm = LocalLLM("http://hz-model.bigmodel.cn/")
    # messages = [
    #     {"role": "system", "content": "用中文回答"},
    #     {"role": "user", "content": "舔狗该死吗"}
    # ]
    # # resp =
    # resp = zeta_llm.generate(messages, stream=False)
    # # for r in resp:
    # print(resp)
    # print(''.join(resp))
    # print(f"llm resp:{resp}")

    zeta_embd = ZhipuLocalEmbedding(batch_size=8, norm=True)
    contents = ["万得", "金融"]
    embds = zeta_embd.embed_documents(texts=contents)
    print(embds)
    print(contents)
    print(f"embd num {len(embds)}")
    l2_norm = sum(e**2 for e in embds[0])
    print(f"l2_norm {l2_norm}")
    print(f"embd dim {len(embds[0])}")
    assert len(embds[0]) == zeta_embd.get_dim(), "not match embd dim"
