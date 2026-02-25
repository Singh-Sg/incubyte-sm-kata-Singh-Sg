import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_salary_calculation_india():
    employee = {
        "full_name": "Test India",
        "job_title": "Developer",
        "country": "India",
        "salary": 100000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    response = client.post(f"/salary/{emp_id}", json={"gross_salary": 100000})
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000
    assert data["deductions"] == 10000  # 10% TDS
    assert data["net_salary"] == 90000


def test_salary_calculation_us():
    employee = {
        "full_name": "Test US",
        "job_title": "Developer",
        "country": "United States",
        "salary": 120000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    response = client.post(f"/salary/{emp_id}", json={"gross_salary": 120000})
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 120000
    assert data["deductions"] == 14400  # 12% TDS
    assert data["net_salary"] == 105600


def test_salary_calculation_other():
    employee = {
        "full_name": "Test Other",
        "job_title": "Developer",
        "country": "Canada",
        "salary": 80000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    response = client.post(f"/salary/{emp_id}", json={"gross_salary": 80000})
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 80000
    assert data["deductions"] == 0
    assert data["net_salary"] == 80000


def test_salary_calculation_employee_not_found():
    response = client.post(f"/salary/99999", json={"gross_salary": 50000})
    assert response.status_code == 404
    assert "detail" in response.json()
