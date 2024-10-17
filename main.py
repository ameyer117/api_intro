from fastapi import FastAPI
from routers.cves.endpoint import router as cves_router
from routers.users.endpoint import router as users_router

app = FastAPI(title="CVE Training API")

app.include_router(cves_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello stackArmor!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}!"}
