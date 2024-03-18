from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.config import Config

from apis.log.log_service import get_log_events
from apis.log.log_schema import GetLogsRequest

router = APIRouter(
    prefix="/log",
    tags=["cloudwatch log"], 
)

@router.get("/")
def get_logs(request: GetLogsRequest):
    function_name = request.function_name    

    return get_log_events(function_name)

