from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey, Decimal, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    loyalty_tier: Mapped[str] = mapped_column(String(20), default="Standard") # Standard, Gold, VIP
    orders: Mapped[List["Order"]] = relationship(back_populates="user")


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    vehicle_no: Mapped[Optional[str]] = mapped_column(String(50))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50)) # Pending, Shipped, Delivered
    total_price: Mapped[float] = mapped_column(Decimal(10, 2))
    tracking_no: Mapped[Optional[str]] = mapped_column(String(100))
    delivery_partner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("delivery_partners.id"))
    user: Mapped["User"] = relationship(back_populates="orders")
    delivery_partner: Mapped[Optional["DeliveryPartner"]] = relationship()


class SupportAgent(Base):
    __tablename__ = "support_agents"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    is_online: Mapped[bool] = mapped_column(Boolean, default=True)


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id: Mapped[str] = mapped_column(String(50), primary_key=True) # UUID
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    thread_id: Mapped[str] = mapped_column(String(100)) # LangGraph Thread ID
    summary: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    messages: Mapped[List["ChatMessage"]] = relationship(back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("chat_sessions.id"))
    role: Mapped[str] = mapped_column(String(20)) # user, assistant
    content: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20)) # Happy, Angry
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    session: Mapped["ChatSession"] = relationship(back_populates="messages")


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("chat_sessions.id"))
    assigned_agent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("support_agents.id"))
    status: Mapped[str] = mapped_column(String(20), default="Open")
    priority: Mapped[int] = mapped_column(default=1)
    ai_brief: Mapped[str] = mapped_column(Text) # AI summary of why the human is needed
    assigned_agent: Mapped[Optional["SupportAgent"]] = relationship()