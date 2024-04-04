import json
from pathlib import Path
from typing import Optional, List

from keble_helpers import AwsTextract
from keble_helpers import TextractResponse, hash_string
from langchain_core.documents import Document
from langchain_core.runnables import run_in_executor
from redis import Redis


class KebleImageLoader:

    def __init__(self, image_filepath: str | Path, *,
                 redis: Optional[Redis] = None,
                 aws_access_key_id: str,
                 aws_access_secret: str,
                 aws_region: str
                 ):
        self.__image_filepath = image_filepath
        self.__key = hash_string(image_filepath)
        self.__redis = redis
        self.__aws_access_key_id = aws_access_key_id
        self.__aws_access_secret = aws_access_secret
        self.__aws_region = aws_region

    @property
    def cache_key(self):
        return f"keble-image-loader:{self.__key}"

    def get_cache(self) -> Optional[TextractResponse]:
        if self.__redis is None: return None
        h = self.__redis.get(self.cache_key)
        if h is None: return None
        return TextractResponse(**json.loads(h))

    def set_cache(self, response: TextractResponse):
        if self.__redis is None: return
        self.__redis.set(self.cache_key, response.model_dump_json(), 7 * 24 * 60 * 60) # expire after 7 days

    def load(self) -> List[Document]:
        h = self.get_cache()
        if h is None:
            textract = AwsTextract(access_key=self.__aws_access_key_id,
                                   secret=self.__aws_access_secret,
                                   region=self.__aws_region
                                   )
            response: TextractResponse = textract.textract(filepath=self.__image_filepath)
            self.set_cache(response)
            return [self.textract_response_to_document(response)]
        else:
            return [self.textract_response_to_document(h)]

    async def aload(self) -> List[Document]:
        return await run_in_executor(None, self.load)

    @classmethod
    def textract_response_to_document(cls, response: TextractResponse) -> Document:
        texts: List[str] = []
        for block in response.Blocks:
            if block.Text is not None:
                texts.append(f"<{block.BlockType}> {block.Text}")
        return Document(page_content="\n".join(texts))
