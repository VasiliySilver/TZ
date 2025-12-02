"""
Script to run event consumer that listens to domain events.
Run: poetry run python scripts/run_consumer.py
"""
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure.messaging.consumer import EventConsumer
from src.infrastructure.messaging.handlers import (
    handle_book_created_composite,
    handle_book_updated_composite,
    handle_book_deleted_composite
)


async def main():
    """Run the event consumer"""
    consumer = EventConsumer(queue_name="book_events_queue")
    
    # Register composite handlers that perform multiple actions
    consumer.register_handler("book.created", handle_book_created_composite)
    consumer.register_handler("book.updated", handle_book_updated_composite)
    consumer.register_handler("book.deleted", handle_book_deleted_composite)
    
    print("🚀 Starting event consumer with composite handlers...")
    print("📡 Listening for events:")
    print("   - book.created  → log, search index, notification, cache, analytics")
    print("   - book.updated  → log, search index, cache")
    print("   - book.deleted  → log, search index, cache")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        await consumer.start()
        # Keep running
        await asyncio.Future()
    except KeyboardInterrupt:
        print("\n⚠️  Shutting down consumer...")
        await consumer.close()
        print("✅ Consumer stopped")


if __name__ == "__main__":
    asyncio.run(main())