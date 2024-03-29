#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/08 14:38:44
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import copy
import re
from abc import abstractmethod
from typing import Iterable, List

from xagents.config import *
from xagents.kb.common import Chunk
from snippets import batchify
from loguru import logger


class AbstractSplitter:
    def __init__(self, invalid_chunks: List[str] = []):
        self.invalid_chunks = invalid_chunks

    @abstractmethod
    def split(self, text: str) -> List[str]:
        raise NotImplementedError

    def split_chunk(self, chunk: Chunk) -> List[Chunk]:
        rs_chunks = []
        for content in self.split(chunk.content):
            content = content.strip()
            if content in self.invalid_chunks:
                continue
            rs_chunks.append(Chunk(content=content,  content_type=chunk.content_type, page_idx=chunk.page_idx))
        return rs_chunks

# 将文本切分、合并到（min_len~max_len）之间的长度


def merge_cut_texts(texts: Iterable[str], min_len: int, max_len: int) -> Iterable[str]:
    acc = ""
    for text in texts:
        acc += text
        if len(acc) < min_len:
            continue
        if len(acc) > max_len:
            for item in batchify(acc, max_len):
                item = "".join(item)
                if len(item) >= min_len:
                    yield item
                    acc = ""
                else:
                    acc = item
        else:
            yield acc
            acc = ""
    if acc:
        yield acc


class BaseSplitter(AbstractSplitter):

    def __init__(self,
                 separator="\n|。|？|\?|！|！|，",
                 parse_table=False,
                 max_len=100,
                 min_len=5,
                 **kwargs):
        super().__init__(**kwargs)
        self.parse_table = parse_table
        self.separator = separator
        self.max_len = max_len
        self.min_len = min_len

    def _parse_text(self, text: str) -> str:
        text = text.strip()
        text = re.sub("\s+", " ", text)
        text = re.sub(f"\.{3,}", "", text)
        text = text.strip()
        return text

    def split(self, text: str) -> List[str]:
        # logger.info(f"{text=}")
        # logger.info(f"{self.separator=}")
        
        texts = re.split(self.separator, text)
        texts = [self._parse_text(t) for t in texts]
        # logger.debug(f"{texts=}")
        texts = list(merge_cut_texts(texts, self.min_len, self.max_len))
        # logger.debug(f"{text=}")
        return texts

    # def split_chunk(self, chunk: Chunk) -> List[Chunk]:
    #     rs_chunks: List[Chunk] = []
    #     if chunk.content_type == ContentType.TABLE and self.parse_table:
    #         table_chunks = []
    #         tables = markdown2tables(chunk.content)
    #         for table in tables:
    #             descs = table.to_desc()
    #             table_chunks.extend([Chunk(content=e, content_type=ContentType.PARSED_TABLE, page_idx=chunk.page_idx) for e in descs])
    #         rs_chunks.extend(table_chunks)
    #     else:
    #         rs_chunks = super().split_chunk(chunk)
    #         logger.debug(f"{rs_chunks=}")

    #     return rs_chunks


_SPLITTERS = [BaseSplitter]
_NAME2SPLITTER = {s.__name__: s for s in _SPLITTERS}


def get_splitter(config: dict) -> AbstractSplitter:
    tmp_config = copy.copy(config)
    splitter_cls = tmp_config.pop("splitter_cls")
    splitter_cls = _NAME2SPLITTER[splitter_cls]
    return splitter_cls(**tmp_config)


if __name__ == "__main__":
    # splitter = BaseSplitter()
    # texts = ["第一节  释义  ................................ ", " "]
    # for text in texts:
    #     print(splitter.split(text))

    texts = ["a"*4, "b"*5, "b"*4, "c"*51, "d"*4]
    for ele in merge_cut_texts(texts, min_len=5, max_len=25):
        print(f"{ele}, {len(ele)}")
