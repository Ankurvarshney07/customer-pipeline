# Customer Pipeline Project

## Overview
This project is a data pipeline with 3 Docker services:
- **Flask API** - Mock customer data server
- **FastAPI** - Data ingestion pipeline
- **PostgreSQL** - Data storage

## Features
- Load customer data from JSON file
- Ingest data into PostgreSQL
- Paginated API responses
- Dockerized services with `docker-compose`

## How to Run
```bash
docker compose up --build
curl http://localhost:5000/api/customers?page=1&limit=5
curl -X POST http://localhost:8000/api/ingest
curl http://localhost:8000/api/customers?page=1&limit=5
