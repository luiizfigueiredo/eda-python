# E-commerce com Arquitetura Orientada a Eventos

Sistema simples de e-commerce com **FastStream** e **RabbitMQ** para demonstrar conceitos de **Event-Driven Architecture (EDA)**.

## Arquitetura

O sistema atual possui 3 microserviços:

- **Order Service**: cria pedidos mock e inicia o fluxo.
- **Payment Service**: processa pagamento e decide aprovação/falha.
- **Logistics Service**: processa envio após pagamento aprovado.

## Fluxo de eventos

Fluxo canônico:

`order.created -> payment.pending -> payment.processed | payment.failed -> shipping.pending -> order.shipped | shipping.failed`

## Setup

Pré-requisitos:

- Python 3.11+
- Docker e Docker Compose
- uv

Instalação:

```bash
cp .env.example .env
uv sync --group dev
docker-compose up -d rabbitmq
docker-compose ps
```

## Execução dos serviços

Em 3 terminais separados, a partir da raiz do projeto:

Terminal 1:

```bash
uv run python services/order_service/order.py
```

Terminal 2:

```bash
uv run python services/payment_service/payment.py
```

Terminal 3:

```bash
uv run python services/logistics_service/logistic.py
```

## Validação E2E manual

Checklist rápido:

1. Confirmar que `order_service` publica pedidos periodicamente.
2. Confirmar no `payment_service` logs de `Received PaymentPending event`.
3. Em aprovação, confirmar que pagamento segue para logística.
4. Confirmar no `logistics_service` logs de `Processing shipping for order`.
5. Verificar saída final com `Shipping success` (`order.shipped`) ou `Shipping failed`.

## Testes

Rodar testes:

```bash
uv run pytest -q
```

## Observações

- RabbitMQ é o broker principal para o fluxo core.
- Redis está no `docker-compose` como opcional, mas não faz parte do pipeline principal desta demo.
