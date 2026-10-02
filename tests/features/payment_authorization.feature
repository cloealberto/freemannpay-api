# language: pt

Funcionalidade: Controle de Acesso e Segurança [PAY-103]

  Como um administrador da plataforma de pagamentos
  Quero exigir um token de autorização em todas as requisições
  Para que sistemas parceiros não autenticados sejam impedidos de acessar a API

  Cenário: Requisição POST sem cabeçalho de autorização
    Dado que a API de pagamentos exige autenticação
    Quando eu envio uma requisição POST para "/payments" sem o cabeçalho "Authorization"
    Então o sistema deve bloquear a ação na entrada
    E retornar o status code 401 (Unauthorized)

  Cenário: Requisição GET com token Bearer inválido
    Dado que a API de pagamentos exige um token Bearer válido
    Quando eu envio uma requisição GET com um token inválido
    Então o sistema não deve expor os dados da transação
    E retornar o status code 401 (Unauthorized)
