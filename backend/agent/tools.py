from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models import Order, SupportAgent, DeliveryPartner
from ..database import AsyncSessionLocal



async def get_order_status_tool(order_id: int):
    """Fetches order status and delivery partner contact info."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.delivery_partner))
            .filter(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        
        if not order:
            return "Order not found."
        
        status_msg = f"Order #{order.id} is currently {order.status}."
        if order.delivery_partner:
            status_msg += (f" Your delivery partner is {order.delivery_partner.name}. "
                          f"Contact: {order.delivery_partner.phone}")
        return status_msg



async def request_human_agent_tool():
    """Finds an online human agent and returns their contact info."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SupportAgent).filter(SupportAgent.is_online == True).limit(1)
        )
        agent = result.scalar_one_or_none()
        
        if agent:
            return {
                "name": agent.name,
                "email": agent.email,
                "phone": agent.phone,
                "msg": "I am transferring you to a human agent now."
            }
        return "All our agents are currently busy, but I've raised a high-priority ticket for you."

