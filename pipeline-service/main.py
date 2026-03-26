from fastapi import FastAPI, HTTPException
from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import fetch_all_data

app = FastAPI()

import time
import psycopg2

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="customer_db",
                user="postgres",
                password="password",
                host="postgres",
                port="5432"
            )
            conn.close()
            print("✅ Database is ready!")
            break
        except psycopg2.OperationalError:
            print("⏳ Waiting for database...")
            time.sleep(2)

wait_for_db()

Base.metadata.create_all(bind=engine)



@app.post("/api/ingest")
def ingest():
    db = SessionLocal()
    data = fetch_all_data()

    count = 0

    for item in data:
        existing = db.query(Customer).filter_by(customer_id=item["customer_id"]).first()

        if existing:
            for key, value in item.items():
                setattr(existing, key, value)
        else:
            db.add(Customer(**item))

        count += 1

    db.commit()
    db.close()

    return {"status": "success", "records_processed": count}


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()

    query = db.query(Customer)
    total = query.count()

    data = query.offset((page - 1) * limit).limit(limit).all()

    db.close()

    return {
        "data": [c.__dict__ for c in data],
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    customer = db.query(Customer).filter_by(customer_id=customer_id).first()

    db.close()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.__dict__