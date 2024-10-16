from fastapi import FastAPI
from routers.cves.endpoint import router as cves_router

app = FastAPI(title="CVE Training API")

app.include_router(cves_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
