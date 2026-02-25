import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_salary_metrics_country():
    employees = [
        {"full_name": "A", "job_title": "Dev", "country": "India", "salary": 10000},
        {"full_name": "B", "job_title": "Dev", "country": "India", "salary": 20000},
        {"full_name": "C", "job_title": "Dev", "country": "India", "salary": 30000},
        {"full_name": "D", "job_title": "Dev", "country": "US", "salary": 40000}
    ]
    for emp in employees:
        client.post("/employees", json=emp)
    response = client.get("/salary/metrics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["min_salary"] == 10000
    assert data["max_salary"] == 30000
    assert data["avg_salary"] == 20000


def test_salary_metrics_job_title():
    employees = [
        {"full_name": "E", "job_title": "QA", "country": "India", "salary": 15000},
        {"full_name": "F", "job_title": "QA", "country": "India", "salary": 25000},
        {"full_name": "G", "job_title": "Dev", "country": "India", "salary": 35000}
    ]
    for emp in employees:
        client.post("/employees", json=emp)
    response = client.get("/salary/metrics/job_title/QA")
    assert response.status_code == 200
    data = response.json()
    assert data["avg_salary"] == 20000


def test_salary_metrics_country_no_employees():
    response = client.get("/salary/metrics/country/Atlantis")
    assert response.status_code == 200
    data = response.json()
    assert data["min_salary"] is None
    assert data["max_salary"] is None
    assert data["avg_salary"] is None


def test_salary_metrics_job_title_no_employees():
    response = client.get("/salary/metrics/job_title/Unknown")
    assert response.status_code == 200
    data = response.json()
    assert data["avg_salary"] is None
