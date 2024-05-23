from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app=app)


local_storage = dict()



def test_loan_application_apply():
    response = client.post("/api/loan_application/applications", json={
        "name": "John",
        "credit_score": 750,
        "loan_amount": 25,
        "loan_purpose": "Salary",
        "income": 10,
        "employment_status": "Unemployed",
        "debt_to_income_ratio": 0.6
    })
    assert response.status_code == 201
    response_json = response.json()
    assert "application_id" in response_json
    print(f"""application_id - {response_json["application_id"]}""")

    local_storage["application_id"] = response_json["application_id"]

def test_loan_application_info():
    application_id = local_storage["application_id"]
    response = client.get(f"/api/loan_application/applications?uuid={application_id}")
    assert response.status_code == 200
    print(response.json()) 

def test_loan_application_update():
    application_id = local_storage["application_id"]
    response = client.put(f"/api/loan_application/applications", json={
        "uuid": application_id,
        "employment_status": "Employed"
    })
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Approved"

def test_loan_application_delete():
    application_id = local_storage["application_id"]
    response = client.delete(f"/api/loan_application/applications?uuid={application_id}")
    assert response.status_code == 204

    