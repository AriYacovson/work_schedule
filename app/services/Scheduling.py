import pulp
from datetime import timedelta


from app.backend.database import SessionLocal
from app.models import EmployeeModel, ShiftModel, EmployeeUnavailableShiftModel

problem = pulp.LpProblem("EmployeeShiftAssignment", pulp.LpMaximize)

# Create a new session instance
db = SessionLocal()

try:
    # Fetch active employees from the database
    employees = db.query(EmployeeModel).filter(EmployeeModel.is_active == True).all()
    shifts = db.query(ShiftModel).all()
    employee_unavailable_shifts = db.query(EmployeeUnavailableShiftModel).all()
finally:
    db.close()  # Ensure you close the session after you're done

x = {}
for employee in employees:
    for shift in shifts:
        var_name = f"x_{employee.id}_{shift.id}"
        x[(employee.id, shift.id)] = pulp.LpVariable(
            var_name,0, 1, pulp.LpBinary
        )

# Objective function: Maximize the number of shifts covered
problem += pulp.lpSum(x)

# Constraint: Each shift must be covered by at least one employee
for shift in shifts:
    problem += (
        pulp.lpSum(x[(employee.id, shift.id)] for employee in employees) >= 1
    )

# Constraint: Each employee can only work one shift per day
# for employee in employees:
#     for day in unique_days:  # This is a hypothetical list of unique days in your shifts
#         total_hours = pulp.lpSum([shift.duration * x[(employee.id, shift.id)] for shift in shifts if shift.day == day])
#         prob += total_hours <= 12


# Constraint: Each employee needs to have at least 8 hours of rest between shifts
for employee in employees:
    for i in range(len(shifts) - 1):
        if (shifts[i+1].start_time - shifts[i].end_time) < timedelta(hours=8):
            problem += x[(employee.id, shifts[i].id)] + x[(employee.id, shifts[i+1].id)] <= 1


# Constraint: Each employee can only work a maximum of 5 shifts per week
for employee in employees:
    total_shifts = pulp.lpSum([x[(employee.id, shift.id)] for shift in shifts])
    problem += total_shifts <= 5


# Constraint: Respect employee unavailable shifts
for unavailable in employee_unavailable_shifts:
    problem += x[(unavailable.employee_id, unavailable.shift_id)] == 0


problem.solve()


if pulp.LpStatus[problem.status] == "Optimal":
    print("An Optimal Solution Found!\n")
    for employee in employees:
        for shift in shifts:
            if x[(employee.id, shift.id)].value() == 1.0:
                print(f"Employee {employee.id} covers shift {shift.id}")
else:
    print("No optimal solution found.")


