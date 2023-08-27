from fastapi import FastAPI
from app.routers import (
    EmployeeController,
    ShiftsController,
    EmployeeShiftAssignmentController,
    EmployeeUnavailableShiftController
)

app = FastAPI()


app.include_router(router=EmployeeController.router)
app.include_router(router=ShiftsController.router)
app.include_router(router=EmployeeShiftAssignmentController.router)
app.include_router(router=EmployeeUnavailableShiftController.router)
