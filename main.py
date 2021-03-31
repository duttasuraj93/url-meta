from fastapi import FastAPI
app = FastAPI()


from routers.metadata import router


app.include_router(router, prefix='')


@app.get("/")
async def root():
    return {"message": "Hello World"}