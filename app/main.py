from fastapi import FastAPI
from app.routers import (
    EmployeeController,
    ShiftsController,
    EmployeeShiftAssignmentController,
    EmployeeUnavailableShiftController,
    ShiftTypeController,
)
import config
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()


app.include_router(router=EmployeeController.router)
app.include_router(router=ShiftTypeController.router)
app.include_router(router=ShiftsController.router)
app.include_router(router=EmployeeShiftAssignmentController.router)
app.include_router(router=EmployeeUnavailableShiftController.router)
