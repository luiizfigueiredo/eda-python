"""
Modelos de dados compartilhados entre os serviços.
Define as estruturas de dados para itens, pedidos, etc.
"""
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """Item de um pedido"""
    product_id: str
    product_name: str
    quantity: int
    price: Decimal

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class Customer(BaseModel):
    """Dados do cliente"""
    customer_id: str
    name: str
    email: str
    address: str
