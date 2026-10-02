# API de Simulação de Pagamentos e Automação de QA para Backend

Este projeto demonstra a estruturação de uma arquitetura completa de Quality Assurance para serviços de backend. O foco principal está na validação de contratos, integridade dos dados e isolamento do ambiente.

Em vez de consumir APIs públicas, que frequentemente geram *flaky tests* devido à manipulação de dados por terceiros, este repositório contém seu próprio microsserviço de pagamentos, construído em **Python (FastAPI)**, testado automaticamente com **Pytest + Playwright** e totalmente orquestrado via **Docker**.

## Tecnologias e Decisões de Arquitetura

*   **FastAPI (Python):** Utilizado para simular o microsserviço. Oferece previsibilidade dos dados e uma documentação Swagger interativa, gerada automaticamente.
*   **Pytest + pytest-bdd + Playwright (Python):** Os cenários Gherkin em `tests/features/` são executados como testes automatizados, com chamadas HTTP reais à API via Playwright.
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
│   ├── test_authorization.py
│   ├── requirements.txt       
│   └── features/
│       ├── payment_creation.feature
│       ├── payment_query.feature
│       └── payment_authorization.feature
├── Dockerfile.tests       
├── docker-compose.yml         
└── run-tests.ps1
```

## Estratégia de Testes e Validação de Dados

A automação foi projetada com forte ênfase em **Qualidade de Dados**, aplicando técnicas formais de teste de software ao tráfego HTTP. O pytest-bdd liga cada cenário dos arquivos Gherkin a passos Python e exibe o nome do cenário durante a execução.

### 1. Separação de Responsabilidades (Clean Code)

O arquivo `conftest.py` centraliza a criação da sessão de rede (`APIRequestContext`) usando **fixtures** do Pytest. Isso garante que os arquivos de teste contenham apenas as regras de negócio, seguindo o princípio da responsabilidade única (SRP) e tornando o projeto altamente escalável caso a API precise de tokens de autenticação no futuro.

O diretório `tests/features/` contém os critérios de aceite executáveis. `test_payments.py` associa os cenários de criação (PAY-101) e consulta (PAY-102) a passos Python; `test_authorization.py` associa os cenários de autorização (PAY-103). Os testes usam as fixtures HTTP centralizadas em `conftest.py`.

### 2. Caminho Feliz e Integridade Transacional (GET e POST)

A suíte garante a criação (`POST`) e a consulta (`GET`) bem-sucedidas de recursos financeiros.

- **Abordagem analítica:** O teste valida a geração correta da chave primária (`id`) e o estado inicial de negócio (`PENDING`). A validação estrita de tipo (`isinstance`) garante que o valor financeiro seja retornado como número de ponto flutuante (`float`), evitando que a perda de precisão afete integrações posteriores, como bancos de dados ou dashboards de BI.

### 3. Cenário Negativo e Particionamento de Equivalência

- **Técnica aplicada:** Uso do **Particionamento de Equivalência**. De acordo com a regra de negócio, qualquer valor financeiro menor ou igual a zero pertence à classe inválida.
- O teste envia um payload com valor negativo (`-50.00`) e verifica se o backend bloqueia a anomalia na entrada, retorna o status `400 Bad Request` e apresenta a mensagem exata de exceção definida no contrato.

## Como Executar Localmente

Como o projeto é orquestrado via Docker, não é necessário instalar dependências locais na máquina, além do próprio Docker. O PostgreSQL também é iniciado pelo Compose, isolado do PostgreSQL instalado no Windows. A API cria a tabela `payments` automaticamente quando inicia.

1. Navegue até a pasta raiz do projeto.
2. Crie ou edite o arquivo `.env` e configure as variáveis abaixo. Não compartilhe nem versione esse arquivo:

```dotenv
PAYMENT_API_TOKEN=seu-token-local
POSTGRES_DB=freemannpay
POSTGRES_USER=freemannpay
POSTGRES_PASSWORD=uma-senha-forte-local
```

3. Execute o comando de orquestração ou rode o script `run-tests.ps1`:

```bash
docker compose up --build --abort-on-container-exit --exit-code-from tests
```

O Docker fará o download das imagens necessárias, iniciará o PostgreSQL e, após sua verificação de saúde, iniciará a API na porta `8000` e executará a suíte do Pytest em um container isolado. O banco fica acessível no host pela porta `5433`, evitando conflito com uma instalação local que já use a porta `5432`. Os dados são preservados no volume `postgres_data`, inclusive após `docker-compose down`; não use `docker-compose down -v` se quiser mantê-los.

Para executar somente os testes de autorização no PowerShell, use:

```powershell
.\run-auth-tests.ps1
```

Esse script aguarda a API ficar saudável e roda `tests/test_authorization.py`; os containers da API e do banco permanecem ativos após os testes. Para executar somente esse arquivo sem o script, use `docker compose up -d --wait api` e depois `docker compose run --build --rm --no-deps tests pytest tests/test_authorization.py -v`.

Para acessar a documentação interativa da API, gerada automaticamente pelo Swagger, abra o navegador e acesse [`http://localhost:8000/docs`](http://localhost:8000/docs).
