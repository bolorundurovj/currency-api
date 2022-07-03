import uvicorn
from fastapi import FastAPI, Request
from app.controllers.currency import router as currency_router
from app.controllers.auth import router as auth_router
from app.utils.error_handler import OpsException
from fastapi.responses import JSONResponse

app = FastAPI(title="Currency API")

ROUTERS = (currency_router, auth_router)


@app.exception_handler(OpsException)
async def OpsExceptionHandler(request: Request, exception: OpsException):
    return JSONResponse(
        status_code=exception.code,
        content={"message": exception.message, "status": exception.status},
    )


for r in ROUTERS:
    app.include_router(r)


@app.get("/")
async def health_check():
    return {"message": "API up and running"}


if __name__ == "__main__":
    uvicorn.run(app="web:app", port=4001, reload=True)
