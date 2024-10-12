from fastapi import FastAPI, Request

tags_metadata = []

app = FastAPI(title="Final Project API", openapi_tags=tags_metadata)


@app.get("/", include_in_schema=False)
def home(request: Request):
    return {"message": "Hello World"}
