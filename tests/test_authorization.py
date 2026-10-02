from pytest_bdd import given, parsers, scenarios, then, when


scenarios("features/payment_authorization.feature")


@given("que a API de pagamentos exige autenticação")
def payment_api_requires_authentication():
    pass


@when(
    parsers.parse(
        'eu envio uma requisição POST para "{path}" sem o cabeçalho "Authorization"'
    )
)
def post_without_authorization(unauthenticated_api, scenario_state, path):
    payload = {
        "user_id": 105,
        "amount": 150.75,
        "currency": "BRL",
        "method": "PIX",
    }
    scenario_state["response"] = unauthenticated_api.post(path, data=payload)


@then("o sistema deve bloquear a ação na entrada")
def assert_unauthorized_action_is_blocked(scenario_state):
    response = scenario_state["response"]
    assert response.status != 201, (
        "A API aceitou a criação do pagamento sem autenticação."
    )


@given("que a API de pagamentos exige um token Bearer válido")
def payment_api_requires_valid_bearer_token():
    pass


@when("eu envio uma requisição GET com um token inválido")
def get_with_invalid_token(invalid_token_api, scenario_state):
    scenario_state["response"] = invalid_token_api.get("/payments/nonexistent")


@then("o sistema não deve expor os dados da transação")
def assert_transaction_data_is_not_exposed(scenario_state):
    response = scenario_state["response"]
    assert response.status != 200, (
        "A API expôs dados de pagamento com credenciais inválidas."
    )


@then(parsers.parse("retornar o status code {status_code:d} ({status_text})"))
def assert_authorization_status_code(scenario_state, status_code, status_text):
    response = scenario_state["response"]
    assert response.status == status_code, (
        f"Esperado HTTP {status_code} ({status_text}), recebido HTTP "
        f"{response.status}: {response.text()}"
    )
