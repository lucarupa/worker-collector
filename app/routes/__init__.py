from fastapi import APIRouter, HTTPException

from app.core.Enum.error_code import ErrorCodeEnum
from app.adapter import CollectorAdapter
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException

router = APIRouter()


def data():
    return {"id": "str", "retryAttempts": 0, "status": "", "hasMaxRetries": ""}


def create_router(collector: CollectorAdapter):

    @router.get("/ready")
    async def ready_operation():
        return data()

    @router.post("/start-scrapper", operation_id="start-scrapper")
    async def start_scrapper(info: StartCollector):
        try:
            collector.execute(info)
            return {
                "id": info.id,
                "code": None,
                "message": None,
                "success": True,
            }
        except GeneralException as e:
            response = {
                "execution_id": info.id,
                "code": e.error_code.value,
                "message": e.message,
                "success": False,
            }
            if e.error_code == ErrorCodeEnum.NOT_FOUND_DATA:
                status_code = 404
            else:
                status_code = 500
            response["message"] = str(e)
            raise HTTPException(status_code=status_code, detail=response)
        except Exception as e:
            response = {
                "execution_id": info.id,
                "code": ErrorCodeEnum.INTERNAL_ERROR_SITE.value,
                "message": str(e),
                "success": False,
            }
            raise HTTPException(status_code=500, detail=response)

    return router
