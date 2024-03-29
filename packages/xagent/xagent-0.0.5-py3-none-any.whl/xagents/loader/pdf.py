#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/11 16:42:25
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from typing import Iterable
from xagents.config import *
from xagents.loader.common import Chunk, ContentType, AbstractLoader
from loguru import logger



class PDFLoader(AbstractLoader):
    def __init__(self, max_page:int=None, extract_images=False):
        """构建pdf加载器

        Args:
            max_page (int, optional): 最大页数. Defaults to None：不限定页数
            extract_images (bool, optional): 是否使用ocr抽取其中的图片. Defaults to False.
        """
        self.max_page = max_page
        self.extract_images = extract_images

    def load(self, file_path: str) -> Iterable[Chunk]:
        from langchain_community.document_loaders.pdf import PyMuPDFLoader
        logger.info(f"loading pdf file {file_path}")
        loader = PyMuPDFLoader(file_path, extract_images=self.extract_images)
        pages = loader.lazy_load()
        idx = 0
        for page in pages:
            idx +=1 
            if self.max_page and idx > self.max_page:
                break
            chunk = Chunk(content=page.page_content, page_idx=idx, content_type=ContentType.TEXT)
            yield chunk


if __name__ == "__main__":
    from xagents.config import XAGENT_HOME
    import sys
    logger.add(sys.stdout)
    loader = PDFLoader(max_page=5, extract_images=True)
    doc_path = os.path.join(XAGENT_HOME, "data/kb_file")
    logger.info(f"parsing all file in {doc_path}")
    print(doc_path)

    for doc in os.listdir(doc_path):
        logger.info(f"loading doc {doc}")
        if doc.endswith(".pdf"):
            pages = loader.load(os.path.join(doc_path, doc))
            for page in pages:
                logger.info(f"*********************page:{page.page_idx}*********************")
                logger.info(page.content)
                logger.info("\n\n")