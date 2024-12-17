from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, transaction_id, user_id, amount, currency, timestamp):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.timestamp = datetime.fromisoformat(timestamp)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
