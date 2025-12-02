"""
Advanced event handlers with real-world use cases
"""
from typing import Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def log_book_event(event_data: Dict[str, Any]) -> None:
    """Log book events to file/service"""
    logger.info(f"BOOK_EVENT: {event_data}")
    # In production: send to ELK, Datadog, etc.


async def update_search_index(event_data: Dict[str, Any]) -> None:
    """Update search index (Elasticsearch, etc.)"""
    book_id = event_data.get('book_id')
    logger.info(f"📚 Updating search index for book: {book_id}")
    # In production: update Elasticsearch, Algolia, etc.


async def send_notification(event_data: Dict[str, Any]) -> None:
    """Send notification (email, webhook, etc.)"""
    title = event_data.get('title', 'Unknown')
    logger.info(f"📧 Sending notification: New book added - {title}")
    # In production: send email, push notification, webhook, etc.


async def update_cache(event_data: Dict[str, Any]) -> None:
    """Invalidate or update cache"""
    logger.info(f"♻️  Invalidating cache for books list")
    # In production: invalidate Redis cache, CDN cache, etc.


async def track_analytics(event_data: Dict[str, Any]) -> None:
    """Track analytics event"""
    logger.info(f"📊 Tracking analytics: {event_data}")
    # In production: send to Google Analytics, Mixpanel, etc.


# Composite handler - executes multiple handlers
async def handle_book_created_composite(event_data: Dict[str, Any]) -> None:
    """Handle book.created with multiple actions"""
    await log_book_event(event_data)
    await update_search_index(event_data)
    await send_notification(event_data)
    await update_cache(event_data)
    await track_analytics(event_data)


async def handle_book_updated_composite(event_data: Dict[str, Any]) -> None:
    """Handle book.updated with multiple actions"""
    await log_book_event(event_data)
    await update_search_index(event_data)
    await update_cache(event_data)


async def handle_book_deleted_composite(event_data: Dict[str, Any]) -> None:
    """Handle book.deleted with multiple actions"""
    await log_book_event(event_data)
    await update_search_index(event_data)
    await update_cache(event_data)