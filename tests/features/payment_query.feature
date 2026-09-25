Funcionalidade: Consulta de Status de Transação por ID [PAY-102]

  Como um sistema parceiro ou serviço de conciliação
  Quero consultar um pagamento específico através do seu ID único
  Para que eu possa atualizar a interface do usuário com o status mais recente

  Cenário: Consulta de pagamento com sucesso via ID
    Dado que um pagamento foi criado com sucesso no sistema
    Quando eu consulto a API utilizando o ID gerado na transação
    Então o sistema deve retornar o status code 200 (OK)
    E a resposta deve conter os dados exatos do pagamento criado