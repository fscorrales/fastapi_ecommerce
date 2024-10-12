from fastapi import FastAPI, Request
from .api.routes import api_router

tags_metadata = []

app = FastAPI(title="Final Project API", openapi_tags=tags_metadata)

# Include our API routes
app.include_router(api_router)


@app.get("/", include_in_schema=False)
def home(request: Request):
    return {"message": "Hello World"}
