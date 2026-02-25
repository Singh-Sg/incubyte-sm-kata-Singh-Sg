import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_employee():
    employee = {
        "full_name": "John Doe",
        "job_title": "Engineer",
        "country": "India",
        "salary": 50000
    }
    response = client.post("/employees", json=employee)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == employee["full_name"]
    assert data["job_title"] == employee["job_title"]
    assert data["country"] == employee["country"]
    assert data["salary"] == employee["salary"]


def test_get_employee():
    employee = {
        "full_name": "Jane Smith",
        "job_title": "Manager",
        "country": "United States",
        "salary": 70000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    get_response = client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == emp_id
    assert data["full_name"] == employee["full_name"]


def test_update_employee():
    employee = {
        "full_name": "Alice Brown",
        "job_title": "Analyst",
        "country": "India",
        "salary": 40000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    updated = {
        "full_name": "Alice Brown",
        "job_title": "Senior Analyst",
        "country": "India",
        "salary": 45000
    }
    put_response = client.put(f"/employees/{emp_id}", json=updated)
    assert put_response.status_code == 200
    data = put_response.json()
    assert data["job_title"] == "Senior Analyst"
    assert data["salary"] == 45000


def test_delete_employee():
    employee = {
        "full_name": "Bob Green",
        "job_title": "Consultant",
        "country": "India",
        "salary": 60000
    }
    post_response = client.post("/employees", json=employee)
    emp_id = post_response.json()["id"]
    del_response = client.delete(f"/employees/{emp_id}")
    assert del_response.status_code == 200
    assert del_response.json()["message"] == "Employee deleted"
    get_response = client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 404
    assert "detail" in get_response.json()
