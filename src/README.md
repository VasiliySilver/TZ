# TZ - Improved Architecture (DDD + TDD + Event-Driven)

## Architecture Layers

### Domain Layer
- Pure business logic
- Entities, Value Objects
- Domain Events
- Repository interfaces (abstractions)

### Application Layer
- Use Cases
- Commands (write operations)
- Queries (read operations)
- Application Services

### Infrastructure Layer
- Technical implementations
- Database (SQLAlchemy)
- Messaging (RabbitMQ + aio-pika)
- External services

### Presentation Layer
- REST API (FastAPI)
- Request/Response schemas (DTOs)
- API versioning

## Key Improvements
- ✅ Clean Architecture / DDD
- ✅ SOLID principles
- ✅ TDD approach
- ✅ Event-driven architecture
- ✅ Proper session management
- ✅ Repository pattern
- ✅ Dependency injection
