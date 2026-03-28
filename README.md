# E-commerce com Arquitetura Orientada a Eventos

Sistema simples de e-commerce desenvolvido com **FastStream** e **Redis Streams** para demonstrar conceitos de **Event-Driven Architecture (EDA)**.

## 🏗️ Arquitetura

O sistema é composto por 4 microserviços independentes que se comunicam através de eventos:

- **Order Service**: Gerencia criação de pedidos
- **Payment Service**: Processa pagamentos
- **Logistics Service**: Gerencia envios
- **Notification Service**: Envia notificações

## 🚀 Setup

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- uv (gerenciador de dependências)

### Instalação

1. **Clone o repositório e navegue até o diretório:**

2. **As dependências já foram instaladas com uv:**

```bash
# Caso precise reinstalar:
uv sync
```

3. **Configure as variáveis de ambiente:**

```bash
cp .env.example .env
```

4. **Inicie o Redis:**

```bash
docker-compose up -d
```

5. **Verifique se o Redis está rodando:**

```bash
docker-compose ps
```

## 📁 Estrutura do Projeto

```
ecommerce-eda/
├── docker-compose.yml          # Configuração do Redis
├── .env.example                # Exemplo de variáveis de ambiente
├── pyproject.toml              # Configuração do uv
├── shared/                     # Código compartilhado entre serviços
│   ├── events.py              # Definição de eventos
│   └── models.py              # Modelos de dados
├── services/                   # Microserviços
│   ├── order_service/
│   ├── payment_service/
│   ├── logistics_service/
│   └── notification_service/
└── scripts/                    # Scripts utilitários
```

## 🔄 Fluxo de Eventos

```
Cliente → OrderCreated → PaymentProcessed → OrderShipped → Notificações
```

## 📚 Tecnologias

- **FastStream**: Framework para event-driven applications
- **RabbitMQ**: Message broker
- **Pydantic**: Validação de dados
- **uv**: Gerenciador de dependências Python
