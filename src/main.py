from fastapi import FastAPI, Request
from .api.routes import api_router, auth_router

tags_metadata = [
    {"name": "Auth"},
    {"name": "Users"},
]

app = FastAPI(title="Final Project API", openapi_tags=tags_metadata)

# Include our API routes
app.include_router(api_router)
# Let's include our auth routes aside from the API routes
app.include_router(auth_router)


@app.get("/", include_in_schema=False)
def home(request: Request):
    return {"message": "Hello World"}
