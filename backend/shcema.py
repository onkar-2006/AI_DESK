from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List

# --- Delivery & Agent Info ---
class DeliveryPartnerSchema(BaseModel):
    name: str
    phone: str
    vehicle_no: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class SupportAgentSchema(BaseModel):
    name: str
    email: str
    phone: str
    model_config = ConfigDict(from_attributes=True)

# --- Chat & Message Schemas ---
class ChatMessageBase(BaseModel):
    role: str
    content: str
    sentiment: Optional[str] = None

class ChatMessageCreate(ChatMessageBase):
    session_id: str

class ChatMessageResponse(ChatMessageBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Order Info (With Delivery Partner) ---
class OrderResponse(BaseModel):
    id: int
    status: str
    total_price: float
    tracking_no: Optional[str]
    delivery_partner: Optional[DeliveryPartnerSchema] = None
    model_config = ConfigDict(from_attributes=True)

# --- Session & Support Ticket ---
class ChatSessionResponse(BaseModel):
    id: str
    thread_id: str
    summary: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SupportTicketResponse(BaseModel):
    id: int
    status: str
    priority: int
    assigned_agent: Optional[SupportAgentSchema] = None
    model_config = ConfigDict(from_attributes=True)

# --- Request for Chat ---
class UserQuery(BaseModel):
    user_id: int
    session_id: str
    query: str

