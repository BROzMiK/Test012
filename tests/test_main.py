from fastapi.testclient import TestClient
from app.main import app
from app.models import Transaction
from sqlalchemy import create_engine
from app.config import DATABASE_URL, API_KEY
import pytest
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client():
    return TestClient(app)

def test_create_transaction(client, test_db):
    headers = {"Authorization": f"ApiKey {API_KEY}"}
    transaction_data = {
        "transaction_id": "test_1",
        "user_id": "user_1",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    response = client.post("/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction received"
    assert test_db.query(Transaction).filter(Transaction.transaction_id == "test_1").first()

def test_create_duplicate_transaction(client, test_db):
    headers = {"Authorization": f"ApiKey {API_KEY}"}
    transaction_data = {
        "transaction_id": "test_1",
        "user_id": "user_1",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    client.post("/transactions", json=transaction_data, headers=headers)
    response = client.post("/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Transaction ID must be unique"

def test_delete_transactions(client, test_db):
    headers = {"Authorization": f"ApiKey {API_KEY}"}
    # Add a transaction first
    transaction_data = {
        "transaction_id": "test_2",
        "user_id": "user_1",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    client.post("/transactions", json=transaction_data, headers=headers)
    
    response = client.delete("/transactions", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "All transactions deleted"
    assert test_db.query(Transaction).count() == 0

def test_get_statistics(client, test_db):
    headers = {"Authorization": f"ApiKey {API_KEY}"}
    # Add some transactions first
    transactions = [
        {
            "transaction_id": "test_3",
            "user_id": "user_1",
            "amount": 100.0,
            "currency": "USD",
            "timestamp": "2024-12-12T12:00:00"
        },
        {
            "transaction_id": "test_4",
            "user_id": "user_2",
            "amount": 200.0,
            "currency": "USD",
            "timestamp": "2024-12-12T13:00:00"
        },
        {
            "transaction_id": "test_5",
            "user_id": "user_1",
            "amount": 150.0,
            "currency": "USD",
            "timestamp": "2024-12-12T14:00:00"
        },
    ]
    for transaction in transactions:
        client.post("/transactions", json=transaction, headers=headers)

    response = client.get("/statistics", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 3
    assert data["average_transaction_amount"] == 150.0
    assert len(data["top_transactions"]) == 3
    top_transaction_amounts = [t["amount"] for t in data["top_transactions"]]
    assert sorted(top_transaction_amounts, reverse=True) == [200.0, 150.0, 100.0]
