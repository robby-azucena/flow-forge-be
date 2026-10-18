from typing import Annotated

from fastapi import File, Form
from fastapi.datastructures import UploadFile
from pydantic import BaseModel


class DocumentAnalysisResponseSchema(BaseModel):
    file_name: str | None
    question: str
    answer: str


class DocumentAnalysisFormSchema(BaseModel):
    file: Annotated[UploadFile, File(...)]
    question: Annotated[str, Form(...)]
    # file: UploadFile = Field(description="File attachment to be analyzed")
    # question: str = Field(description="Question to analyze the file for")
