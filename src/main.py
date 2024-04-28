from fastapi import FastAPI

app = FastAPI()


@app.get("/helloworld")
async def helloworld():
    return "Hello World!"
