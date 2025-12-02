import json
from typing import Any, Dict
from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

from src.infrastructure.messaging.config import rabbitmq_config


class EventPublisher:
    """
    Publisher for domain events to RabbitMQ.
    Uses topic exchange for flexible routing.
    """
    
    EXCHANGE_NAME = "domain_events"
    
    def __init__(self):
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
    
    async def connect(self) -> None:
        """Establish connection to RabbitMQ"""
        if self._connection is None or self._connection.is_closed:
            self._connection = await connect_robust(rabbitmq_config.url)
            self._channel = await self._connection.channel()
            
            # Declare topic exchange
            exchange = await self._channel.declare_exchange(
                self.EXCHANGE_NAME,
                type="topic",
                durable=True
            )
            
            print(f"✅ Connected to RabbitMQ and declared exchange: {self.EXCHANGE_NAME}")
    
    async def publish(self, routing_key: str, event_data: Dict[str, Any]) -> None:
        """
        Publish an event to RabbitMQ.
        
        Args:
            routing_key: Event routing key (e.g., "book.created", "book.updated")
            event_data: Event data as dictionary
        """
        if self._channel is None:
            await self.connect()
        
        exchange = await self._channel.get_exchange(self.EXCHANGE_NAME)
        
        message_body = json.dumps(event_data, default=str)
        message = Message(
            body=message_body.encode(),
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json"
        )
        
        await exchange.publish(message, routing_key=routing_key)
        print(f"📤 Published event: {routing_key}")
    
    async def close(self) -> None:
        """Close connection to RabbitMQ"""
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        print("🔌 RabbitMQ connection closed")


# Global instance
_publisher: EventPublisher | None = None


async def get_event_publisher() -> EventPublisher:
    """Get global event publisher instance"""
    global _publisher
    if _publisher is None:
        _publisher = EventPublisher()
        await _publisher.connect()
    return _publisher