from pathlib import Path
from typing import Optional, List

from keble_helpers import AwsTextract
from keble_helpers import TextractResponse
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
        self.__redis = redis
        self.__aws_access_key_id = aws_access_key_id
        self.__aws_access_secret = aws_access_secret
        self.__aws_region = aws_region

    def load(self) -> List[Document]:
        textract = AwsTextract(access_key=self.__aws_access_key_id,
                               secret=self.__aws_access_secret,
                               region=self.__aws_region
                               )
        response: TextractResponse = textract.textract(filepath=self.__image_filepath)
        return [self.textract_response_to_document(response)]

    async def aload(self) -> List[Document]:
        return await run_in_executor(None, self.load, filepath=self.__image_filepath)

    @classmethod
    def textract_response_to_document(cls, response: TextractResponse) -> Document:
        texts: List[str] = []
        for block in response.Blocks:
            if block.Text is not None:
                texts.append(f"<{block.BlockType}> {block.Text}")
        return Document(page_content="\n".join(texts))
