# Payment Simulation API & QA Backend Automation

This project demonstrates the structuring of a complete Quality Assurance architecture for Backend services. The main focus is on contract validation, data integrity, and environment isolation.

Instead of consuming public APIs (which frequently lead to *flaky tests* due to third-party data manipulation), this repository contains its own Payment microservice built in **Python (FastAPI)**, automatically tested via **Pytest + Playwright**, and 100% orchestrated via **Docker**.

## Tech Stack and Architecture Decisions

*   **FastAPI (Python):** Used to mock the microservice. It provides data predictability and an interactive, auto-generated Swagger documentation.
*   **Pytest + Playwright (Python):** Stack unification. Using Python for both the API and the test automation reduces context switching and simplifies the handling of complex data types and business rules.
*   **Docker & Docker Compose:** Total isolation. Guarantees environment parity, allowing the test suite to run identically on any local machine or CI/CD pipeline.
*   **Healthchecks:** The Docker Compose setup includes healthcheck routines to ensure the test container only starts executing after the API is 100% ready to receive HTTP requests, preventing race conditions.

---

## Project Structure

```text
api-automation-payments/
├── api/
│   ├── main.py                
│   └── requirements.txt       
├── tests/
│   ├── conftest.py            
│   ├── test_payments.py     
│   └── requirements.txt       
├── Dockerfile.tests       
├── docker-compose.yml         
└── run-tests.ps1
```

## Testing Strategy and Data Validation

The automation was designed with a strong emphasis on **Data Quality**, applying formal software testing techniques to HTTP traffic.

### 1. Separation of Concerns (Clean Code)

The `conftest.py` file centralizes the creation of the network session (`APIRequestContext`) using Pytest **fixtures**. This ensures the test files contain only business rules, adhering to the Single Responsibility Principle (SRP) and making the project highly scalable if the API requires authentication tokens in the future.

### 2. Happy Path and Transactional Integrity (GET & POST)

The suite ensures the successful creation (`POST`) and retrieval (`GET`) of financial resources.

- **Analytical approach:** The test validates the correct generation of the primary key (`id`) and the initial business state (`PENDING`). Strict type validation (`isinstance`) ensures the financial value is returned as a floating-point number (`float`), preventing precision loss from affecting downstream integrations such as databases or BI dashboards.

### 3. Negative Scenario and Equivalence Partitioning

- **Applied technique:** Use of **Equivalence Partitioning**. According to the business rule, any financial value less than or equal to zero belongs to the invalid class.
- The test sends a payload with a negative amount (`-50.00`) and asserts that the backend blocks the anomaly at the entry point, returns a `400 Bad Request` status, and outputs the exact exception message defined in the contract.

## How to Run Locally

Because the project is orchestrated via Docker, there is no need to install local dependencies on your machine other than Docker itself.

1. Clone the repository.
2. Navigate to the project's root folder.
3. Execute the orchestration command or run the `run-tests.ps1` script:

```bash
docker-compose up --build
```

Docker will download the necessary images, start the API on port `8000` after validating its health status, and execute the Pytest suite in an isolated container.

To access the interactive API documentation generated automatically by Swagger, open your browser and navigate to [`http://localhost:8000/docs`](http://localhost:8000/docs).

