# API de Simulação de Pagamentos e Automação de QA para Backend

Este projeto demonstra a estruturação de uma arquitetura completa de Quality Assurance para serviços de backend. O foco principal está na validação de contratos, integridade dos dados e isolamento do ambiente.

Em vez de consumir APIs públicas, que frequentemente geram *flaky tests* devido à manipulação de dados por terceiros, este repositório contém seu próprio microsserviço de pagamentos, construído em **Python (FastAPI)**, testado automaticamente com **Pytest + Playwright** e totalmente orquestrado via **Docker**.

## Tecnologias e Decisões de Arquitetura

*   **FastAPI (Python):** Utilizado para simular o microsserviço. Oferece previsibilidade dos dados e uma documentação Swagger interativa, gerada automaticamente.
*   **Pytest + Playwright (Python):** Unificação da stack. Usar Python tanto na API quanto na automação de testes reduz a troca de contexto e simplifica o tratamento de tipos de dados complexos e regras de negócio.
*   **Docker e Docker Compose:** Isolamento total. Garante a paridade entre ambientes, permitindo que a suíte de testes seja executada da mesma forma em qualquer máquina local ou pipeline de CI/CD.
*   **Healthchecks:** A configuração do Docker Compose inclui verificações de saúde para garantir que o container de testes só comece a execução depois que a API estiver 100% pronta para receber requisições HTTP, evitando condições de corrida.

---

## Estrutura do Projeto

```text
api-automation-payments/
├── api/
│   ├── main.py                
│   └── requirements.txt       
├── tests/
│   ├── conftest.py            
│   ├── test_payments.py     
│   ├── requirements.txt       
│   └── features/
│       ├── payment_creation.feature
│       └── payment_query.feature
├── Dockerfile.tests       
├── docker-compose.yml         
└── run-tests.ps1
```

## Estratégia de Testes e Validação de Dados

A automação foi projetada com forte ênfase em **Qualidade de Dados**, aplicando técnicas formais de teste de software ao tráfego HTTP.

### 1. Separação de Responsabilidades (Clean Code)

O arquivo `conftest.py` centraliza a criação da sessão de rede (`APIRequestContext`) usando **fixtures** do Pytest. Isso garante que os arquivos de teste contenham apenas as regras de negócio, seguindo o princípio da responsabilidade única (SRP) e tornando o projeto altamente escalável caso a API precise de tokens de autenticação no futuro.

O diretório `tests/features/` documenta os critérios de aceite de cada User Story. O arquivo `payment_creation.feature` corresponde à PAY-101, enquanto `payment_query.feature` corresponde à PAY-102. Os testes automatizados em `test_payments.py` seguem a mesma ordem das User Stories para facilitar a rastreabilidade.

### 2. Caminho Feliz e Integridade Transacional (GET e POST)

A suíte garante a criação (`POST`) e a consulta (`GET`) bem-sucedidas de recursos financeiros.

- **Abordagem analítica:** O teste valida a geração correta da chave primária (`id`) e o estado inicial de negócio (`PENDING`). A validação estrita de tipo (`isinstance`) garante que o valor financeiro seja retornado como número de ponto flutuante (`float`), evitando que a perda de precisão afete integrações posteriores, como bancos de dados ou dashboards de BI.

### 3. Cenário Negativo e Particionamento de Equivalência

- **Técnica aplicada:** Uso do **Particionamento de Equivalência**. De acordo com a regra de negócio, qualquer valor financeiro menor ou igual a zero pertence à classe inválida.
- O teste envia um payload com valor negativo (`-50.00`) e verifica se o backend bloqueia a anomalia na entrada, retorna o status `400 Bad Request` e apresenta a mensagem exata de exceção definida no contrato.

## Como Executar Localmente

Como o projeto é orquestrado via Docker, não é necessário instalar dependências locais na máquina, além do próprio Docker.

1. Clone o repositório.
2. Navegue até a pasta raiz do projeto.
3. Execute o comando de orquestração ou rode o script `run-tests.ps1`:

```bash
docker-compose up --build
```

O Docker fará o download das imagens necessárias, iniciará a API na porta `8000` após validar seu estado de saúde e executará a suíte do Pytest em um container isolado.

Para acessar a documentação interativa da API, gerada automaticamente pelo Swagger, abra o navegador e acesse [`http://localhost:8000/docs`](http://localhost:8000/docs).

