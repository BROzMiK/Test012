# /app/tasks.py
from celery import Celery
from .config import REDIS_URL, DATABASE_URL
from .models import SessionLocal, Transaction
from .utils import RunningAverage, find_top_transactions
from sqlalchemy import func

celery = Celery(__name__, broker=REDIS_URL)

@celery.task
def update_statistics():
    session = SessionLocal()
    try:
        total_transactions = session.query(func.count(Transaction.transaction_id)).scalar()
        
        running_average = RunningAverage()
        for transaction in session.query(Transaction).all():
            running_average.update(transaction.amount)
        average_transaction_amount = running_average.get_average()

        all_transactions = session.query(Transaction).all()
        top_transactions = find_top_transactions(all_transactions)
        
        top_transactions_list = [{"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions]

        return {
            "total_transactions": total_transactions,
            "average_transaction_amount": average_transaction_amount,
            "top_transactions": top_transactions_list
        }
    finally:
        session.close()
