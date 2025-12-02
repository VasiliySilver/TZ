import json
import asyncio
from typing import Callable, Dict, Any
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from src.infrastructure.messaging.config import rabbitmq_config


class EventConsumer:
    """
    Consumer for domain events from RabbitMQ.
    Listens to specific routing keys and processes events.
    """
    
    EXCHANGE_NAME = "domain_events"
    
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self._connection = None
        self._channel = None
        self._handlers: Dict[str, Callable] = {}
    
    def register_handler(self, routing_key: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a handler for specific routing key.
        
        Args:
            routing_key: Event routing key pattern (e.g., "book.*", "book.created")
            handler: Async function to handle the event
        """
        self._handlers[routing_key] = handler
        print(f"📝 Registered handler for: {routing_key}")
    
    async def start(self) -> None:
        """Start consuming events from RabbitMQ"""
        self._connection = await connect_robust(rabbitmq_config.url)
        self._channel = await self._connection.channel()
        
        # Set QoS - process one message at a time
        await self._channel.set_qos(prefetch_count=1)
        
        # Declare exchange
        exchange = await self._channel.declare_exchange(
            self.EXCHANGE_NAME,
            ExchangeType.TOPIC,
            durable=True
        )
        
        # Declare queue
        queue = await self._channel.declare_queue(
            self.queue_name,
            durable=True
        )
        
        # Bind queue to exchange with routing keys
        for routing_key in self._handlers.keys():
            await queue.bind(exchange, routing_key=routing_key)
            print(f"🔗 Bound queue '{self.queue_name}' to routing key: {routing_key}")
        
        # Start consuming
        await queue.consume(self._process_message)
        print(f"✅ Consumer started. Listening to queue: {self.queue_name}")
    
    async def _process_message(self, message: AbstractIncomingMessage) -> None:
        """Process incoming message"""
        async with message.process():
            try:
                event_data = json.loads(message.body.decode())
                routing_key = message.routing_key
                
                print(f"📥 Received event: {routing_key}")
                print(f"   Data: {event_data}")
                
                # Find and execute handler
                handler = self._handlers.get(routing_key)
                if handler:
                    await handler(event_data)
                else:
                    print(f"⚠️  No handler found for routing key: {routing_key}")
                    
            except Exception as e:
                print(f"❌ Error processing message: {e}")
    
    async def close(self) -> None:
        """Close connection to RabbitMQ"""
        if self._channel:
            await self._channel.close()
        if self._connection:
            await self._connection.close()
        print("🔌 Consumer connection closed")


# Example handlers
async def handle_book_created(event_data: Dict[str, Any]) -> None:
    """Handler for book.created events"""
    print(f"🎉 Book created: {event_data['title']} (ID: {event_data['book_id']})")
    # Here you can add logic like:
    # - Send email notification
    # - Update search index
    # - Log to analytics


async def handle_book_updated(event_data: Dict[str, Any]) -> None:
    """Handler for book.updated events"""
    print(f"✏️  Book updated: {event_data['book_id']}")


async def handle_book_deleted(event_data: Dict[str, Any]) -> None:
    """Handler for book.deleted events"""
    print(f"🗑️  Book deleted: {event_data['book_id']}")