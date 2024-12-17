# Transaction Management API

## Overview

This project provides a RESTful API for managing financial transactions. It allows users to create, delete, and retrieve statistics about transactions. The API is built using Python with the FastAPI framework, and it uses PostgreSQL for data storage and Redis for task queuing with Celery.

## Key Features


## Technologies Used


## Setup Instructions

### Running Locally

1.  **Prerequisites:**
    -   Python 3.11
    -   pip
    -   PostgreSQL
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Up PostgreSQL:**
    -   Create a database named `transactions_db`.
    -   Use the credentials specified in `docker-compose.yml` or set the `DATABASE_URL` environment variable.
5.  **Run the Application:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
6.  **Access the API Documentation:**
    Open your browser and go to `http://localhost:8000/docs`.

### Running with Docker Compose

1.  **Prerequisites:**
    -   Docker
    -   Docker Compose
2.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```
3.  **Access the Application:**
    Open your browser and go to `http://localhost:8000/docs`.

## API Usage

### Authentication

All API endpoints require an API key in the `Authorization` header. The API key should be in the format `ApiKey your_secret_api_key`. You can find the default API key in the `docker-compose.yml` file, but it is recommended to set it via an environment variable.

### Endpoints

    -   Request Body:
        ```json
        {
            "transaction_id": "unique_id",
            "user_id": "user_id",
            "amount": 100.0,
            "currency": "USD",
            "timestamp": "2024-12-12T12:00:00"
        }
        ```
    -   Response:
        ```json
        {
            "message": "Transaction received",
            "task_id": "celery_task_id"
        }
        ```
    -   Response:
        ```json
        {
            "message": "All transactions deleted"
        }
        ```
    -   Response:
        ```json
        {
            "total_transactions": 10,
            "average_transaction_amount": 123.45,
            "top_transactions": [
                {"transaction_id": "id1", "amount": 500.0},
                {"transaction_id": "id2", "amount": 400.0},
                {"transaction_id": "id3", "amount": 300.0}
            ]
        }
        ```

## Testing

The project includes unit tests using pytest. To run the tests:

1.  Install pytest:
    ```bash
    pip install pytest
    ```
2.  Run the tests:
    ```bash
    pytest tests/test_main.py
    ```

## Contribution Guidelines

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure tests pass.
4.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License.
