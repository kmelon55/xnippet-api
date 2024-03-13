from fastapi import APIRouter
from dotenv import load_dotenv
from starlette.config import Config


from api.snippet.snippet_service import create_lambda_function 

router = APIRouter(
    prefix="/snippet",
    tags=["lambda function apis"], 
)

@router.post("/post")
def coupang_post(request):
	response = ""

	return response