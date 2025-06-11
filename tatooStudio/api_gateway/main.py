from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Микросервисы
SERVICES = {
    "booking": "http://localhost:8000",
    "catalog": "http://localhost:8001",
    "user": "http://localhost:8002",
}


@app.get("/{service}/{path:path}")
async def gateway_get(service: str, path: str):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    async with httpx.AsyncClient(base_url=SERVICES[service]) as client:
        response = await client.get(f"/{path}")
        return response.json()


@app.post("/{service}/{path:path}")
async def gateway_post(service: str, path: str, body: dict):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    async with httpx.AsyncClient(base_url=SERVICES[service]) as client:
        response = await client.post(f"/{path}", json=body)
        return response.json()