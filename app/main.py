from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mangum import Mangum

from apis.snippet.snippet_router import router as snippet_router
from apis.log.log_router import router as log_router

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

app.include_router(snippet_router)
app.include_router(log_router)

handler = Mangum(app)