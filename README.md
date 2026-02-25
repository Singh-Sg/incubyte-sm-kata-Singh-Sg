# Employee API Assignment

## Overview
This project implements a production-ready FastAPI application for employee management and salary analytics. It follows strict Test-Driven Development (TDD) and leverages AI for scaffolding, test generation, and documentation.

## Features
- Employee CRUD endpoints (Create, Read, Update, Delete)
- Salary calculation endpoint (deductions and net salary by country)
- Salary metrics endpoints (min, max, avg by country; avg by job title)
- Sqlite database persistence
- Comprehensive unit tests (pytest)

## API Endpoints
### Employee CRUD
- `POST /employees` — Create employee
- `GET /employees/{employee_id}` — Get employee by ID
- `PUT /employees/{employee_id}` — Update employee
- `DELETE /employees/{employee_id}` — Delete employee

### Salary Calculation
- `POST /salary/{employee_id}` — Calculate deductions and net salary
  - India: TDS 10%
  - United States: TDS 12%
  - Others: No deductions

### Salary Metrics
- `GET /salary/metrics/country/{country}` — Min, max, avg salary for country
- `GET /salary/metrics/job_title/{job_title}` — Avg salary for job title

## Running the Project
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests:
   ```bash
   pytest
   ```
3. Start API server:
   ```bash
   uvicorn main:app --reload
   ```

## Implementation Details
- **AI Usage:** AI was used for scaffolding FastAPI code, generating test cases, and drafting this README. All code changes and test cases were reviewed for correctness and clarity.
- **TDD Workflow:** All features were developed using red → green → refactor cycles, with incremental commits for each step.
- **Test Isolation:** Salary metrics tests include a fixture to clear the database for reliable results.

## Notes
- No UI is included; this is a pure API.
- All endpoints return JSON responses.
- The codebase is ready for production and extensible for future requirements.

---