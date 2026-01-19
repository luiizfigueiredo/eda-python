"""
Definição de todos os eventos do sistema.
Cada evento representa um fato que aconteceu no sistema.
"""
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field

from shared.models import OrderItem, Customer


class EventType(str, Enum):
    """Tipos de eventos do sistema"""
    ORDER_CREATED = "order.created"
    PAYMENT_PROCESSED = "payment.processed"
    PAYMENT_FAILED = "payment.failed"
    ORDER_SHIPPED = "order.shipped"
    SHIPPING_FAILED = "shipping.failed"


class BaseEvent(BaseModel):
    """Classe base para todos os eventos"""
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }


class OrderCreatedEvent(BaseEvent):
    """Evento: Pedido foi criado"""
    event_type: EventType = EventType.ORDER_CREATED
    order_id: str
    customer: Customer
    items: List[OrderItem]
    total_amount: Decimal


class PaymentProcessedEvent(BaseEvent):
    """Evento: Pagamento foi processado com sucesso"""
    event_type: EventType = EventType.PAYMENT_PROCESSED
    order_id: str
    payment_id: str
    amount: Decimal
    status: str = "approved"


class PaymentFailedEvent(BaseEvent):
    """Evento: Pagamento falhou"""
    event_type: EventType = EventType.PAYMENT_FAILED
    order_id: str
    reason: str


class OrderShippedEvent(BaseEvent):
    """Evento: Pedido foi enviado"""
    event_type: EventType = EventType.ORDER_SHIPPED
    order_id: str
    tracking_code: str
    estimated_delivery: datetime


class ShippingFailedEvent(BaseEvent):
    """Evento: Envio falhou"""
    event_type: EventType = EventType.SHIPPING_FAILED
    order_id: str
    reason: str
