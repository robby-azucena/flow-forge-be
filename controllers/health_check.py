from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi_utils.cbv import cbv
from starlette.status import HTTP_200_OK

router = APIRouter()
tag = "Health check"

@cbv(router)
class HealthCheckController:
    @router.get("/", tags=[tag], dependencies=[])
    def health_check(self):
        return JSONResponse("API is OK", status_code=HTTP_200_OK)
