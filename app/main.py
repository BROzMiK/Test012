from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from .models import SessionLocal, Transaction
from .tasks import update_statistics
from .config import API_KEY
from sqlalchemy.exc import IntegrityError

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def api_key_auth(api_key: str = Header(...)):
    if api_key != f"ApiKey {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

class TransactionCreate(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: str

@app.post("/transactions", dependencies=[Depends(api_key_auth)])
async def create_transaction(transaction: TransactionCreate, db: SessionLocal = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Transaction ID must be unique")
    task = update_statistics.delay()
    return {"message": "Transaction received", "task_id": task.id}

@app.delete("/transactions", dependencies=[Depends(api_key_auth)])
async def delete_transactions(db: SessionLocal = Depends(get_db)):
    db.query(Transaction).delete()
    db.commit()
    return {"message": "All transactions deleted"}

@app.get("/statistics", dependencies=[Depends(api_key_auth)])
async def get_statistics(db: SessionLocal = Depends(get_db)):
    task_result = update_statistics.delay().get()
    return task_result
