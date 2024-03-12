from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mangum import Mangum


app = FastAPI(
    title="Xnippet API",
    description="Provides an API that interworks code snippets with cloud services",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


handler = Mangum(app)