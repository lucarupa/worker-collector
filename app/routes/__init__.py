from fastapi import APIRouter

router = APIRouter()

def data():
    return {
        "id": "str",
        "retryAttempts": 0,
        "status": "",
        "hasMaxRetries": ""
    }

def create_router():
    @router.get('/ready')
    async def ready_operation():
        return data()
    return router