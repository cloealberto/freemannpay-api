from playwright.sync_api import APIRequestContext

# US01: Create a payment.
def test_create_pix_payment_successfully(api: APIRequestContext):
    """
    Maps to: tests/features/payment_creation.feature 
    Cenário: Caminho Feliz - Processamento com sucesso
    """
    payload = {
        "user_id": 105,
        "amount": 150.75,
        "currency": "BRL",
        "method": "PIX"
    }
    
    response = api.post("/payments", data=payload)
    assert response.status == 201

    data = response.json()
    
    # Validate the response structure and data types.
    assert "id" in data
    assert data["status"] == "PENDING"
    assert data["amount"] == 150.75
    assert isinstance(data["amount"], float)

def test_reject_payment_with_negative_amount(api: APIRequestContext):
    """
    Maps to: tests/features/payment_creation.feature 
    Cenário: Caminho de Exceção - Rejeição de pagamento com valor negativo
    """
    payload = {
        "user_id": 105,
        "amount": -50.00,
        "currency": "BRL",
        "method": "CREDIT_CARD"
    }
    
    response = api.post("/payments", data=payload)
    assert response.status == 400
    
    error_data = response.json()
    assert error_data["detail"] == "Amount must be greater than zero"


# US02: Retrieve a payment.
def test_get_payment_by_id_successfully(api: APIRequestContext):
    """
    Maps to: tests/features/payment_query.feature 
    Cenário: Consulta de pagamento com sucesso via ID
    """
    payload = {
        "user_id": 105,
        "amount": 150.75,
        "currency": "BRL",
        "method": "PIX"
    }

    create_response = api.post("/payments", data=payload)
    assert create_response.status == 201

    payment_id = create_response.json()["id"]
    get_response = api.get(f"/payments/{payment_id}")

    assert get_response.status == 200
    data = get_response.json()
    assert data["id"] == payment_id
    assert data["user_id"] == payload["user_id"]
    assert data["amount"] == payload["amount"]
    assert data["currency"] == payload["currency"]
    assert data["method"] == payload["method"]
    assert data["status"] == "PENDING"