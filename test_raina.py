from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/api/raina_chat")
async def raina_chat(req: Request):
    data = await req.json()
    msg = data.get("message", "")
    return JSONResponse({"reply": f"Message received: {msg}"})

if __name__ == "__main__":
    uvicorn.run("test_raina:app", host="127.0.0.1", port=8080, reload=True)
