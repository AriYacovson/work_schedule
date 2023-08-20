from fastapi import FastAPI
from app.routers import EmployeeController, ShiftsController

app = FastAPI()

app.include_router(router=EmployeeController.router)
app.include_router(router=ShiftsController.router)



