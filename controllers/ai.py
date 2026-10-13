from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_CONTENT

from schemas.document_schema import (
    DocumentAnalysisResponseSchema,
)
from services.ai import AIService
from utils.auth_bearer import JWTBearer

router = APIRouter()
tag = "AI"


@cbv(router)
class AIController:
    @router.post(
        "/analyze",
        tags=[tag],
        response_model=DocumentAnalysisResponseSchema,
        dependencies=[Depends(JWTBearer())],
    )
    async def analyze_document(
        self,
        request: Request,
        file: Annotated[UploadFile, File(...)],
        question: Annotated[str, Form(...)],
    ):
        request.state.audit_event = "DOC_ANALYZE"

        doc_file = file
        doc_question = question

        if not doc_file:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="A file is required"
            )

        if not doc_question.strip():
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Question cannot be empty",
            )

        try:
            service = AIService()

            answer = await service.analyze(file=doc_file, question=doc_question.strip())

            return DocumentAnalysisResponseSchema(
                file_name=doc_file.filename,
                question=doc_question.strip(),
                answer=answer,
            )

        finally:
            await doc_file.close()
