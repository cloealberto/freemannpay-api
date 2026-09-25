Funcionalidade: Criação de Transação de Pagamento [PAY-101]

  Como um sistema parceiro (Front-end/BFF)
  Quero enviar um payload com os dados financeiros do cliente
  Para que a transação seja registrada no sistema com status PENDING

  Cenário: Caminho Feliz - Processamento com sucesso
    Dado que o endpoint de criação de pagamentos está acessível
    Quando eu envio um payload válido para o método "PIX" no valor de "150.75"
    Então o sistema deve retornar o status code 201 (Created)
    E o status do pagamento deve ser registrado como "PENDING"

  Cenário: Caminho de Exceção - Rejeição de pagamento com valor negativo
    Dado a regra de negócio de que valores financeiros devem ser maiores que zero
    Quando eu envio um payload com o valor negativo de "-50.00"
    Então o sistema deve barrar a transação na entrada e retornar o status code 400 (Bad Request)