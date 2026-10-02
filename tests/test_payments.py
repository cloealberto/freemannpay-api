from pytest_bdd import given, parsers, scenarios, then, when


scenarios("features/payment_creation.feature")
scenarios("features/payment_query.feature")


@given("que o endpoint de criação de pagamentos está acessível")
def payment_creation_endpoint_is_accessible(api):
    assert api is not None


@when(
    parsers.parse(
        'eu envio um payload válido para o método "{method}" no valor de "{amount}"'
    )
)
def create_payment_with_valid_payload(api, scenario_state, method, amount):
    payload = {
        "user_id": 105,
        "amount": float(amount),
        "currency": "BRL",
        "method": method,
    }
    scenario_state["payload"] = payload
    scenario_state["response"] = api.post("/payments", data=payload)


@given("a regra de negócio de que valores financeiros devem ser maiores que zero")
def positive_payment_amount_rule_is_required():
    pass


@when(parsers.parse('eu envio um payload com o valor negativo de "{amount}"'))
def create_payment_with_negative_amount(api, scenario_state, amount):
    payload = {
        "user_id": 105,
        "amount": float(amount),
        "currency": "BRL",
        "method": "CREDIT_CARD",
    }
    scenario_state["response"] = api.post("/payments", data=payload)


@given("que um pagamento foi criado com sucesso no sistema")
def create_payment_for_query(api, scenario_state):
    payload = {
        "user_id": 105,
        "amount": 150.75,
        "currency": "BRL",
        "method": "PIX",
    }
    response = api.post("/payments", data=payload)
    assert response.status == 201, (
        "Não foi possível preparar o cenário de consulta. "
        f"Esperado HTTP 201, recebido HTTP {response.status}: {response.text()}"
    )
    scenario_state["created_payment"] = response.json()


@when("eu consulto a API utilizando o ID gerado na transação")
def query_created_payment(api, scenario_state):
    payment_id = scenario_state["created_payment"]["id"]
    scenario_state["response"] = api.get(f"/payments/{payment_id}")


@then(parsers.parse("o sistema deve retornar o status code {status_code:d} ({status_text})"))
def assert_payment_status_code(scenario_state, status_code, status_text):
    response = scenario_state["response"]
    assert response.status == status_code, (
        f"Esperado HTTP {status_code} ({status_text}), recebido HTTP "
        f"{response.status}: {response.text()}"
    )


@then(
    parsers.parse(
        "o sistema deve barrar a transação na entrada e retornar o status code "
        "{status_code:d} ({status_text})"
    )
)
def assert_invalid_payment_status_code(scenario_state, status_code, status_text):
    response = scenario_state["response"]
    assert response.status == status_code, (
        f"Esperado HTTP {status_code} ({status_text}), recebido HTTP "
        f"{response.status}: {response.text()}"
    )


@then("a resposta deve informar que o valor deve ser maior que zero")
def assert_invalid_payment_error_message(scenario_state):
    response = scenario_state["response"]
    error = response.json()
    assert error["detail"] == "Amount must be greater than zero", (
        "Esperada a mensagem de validação para valor não positivo; "
        f"recebida: {error!r}"
    )


@then(parsers.parse('o status do pagamento deve ser registrado como "{status}"'))
def assert_payment_status(scenario_state, status):
    response = scenario_state["response"]
    data = response.json()
    assert data["status"] == status, (
        f"Esperado status do pagamento {status!r}, recebido {data.get('status')!r}."
    )
    assert data["amount"] == scenario_state["payload"]["amount"]
    assert isinstance(data["amount"], float)
    assert data["method"] == scenario_state["payload"]["method"]


@then("a resposta deve conter os dados exatos do pagamento criado")
def assert_query_response_matches_created_payment(scenario_state):
    response = scenario_state["response"]
    actual = response.json()
    expected = scenario_state["created_payment"]
    assert actual == expected, (
        f"Os dados consultados diferem dos dados criados. "
        f"Esperado: {expected!r}; recebido: {actual!r}"
    )