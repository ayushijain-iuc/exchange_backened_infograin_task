# Trading Engine Backend

A simple trading exchange backend built with FastAPI, SQLAlchemy, and SQLite that simulates order matching and trade execution.

## Features

- **User Management**: Create and retrieve users with balance tracking
- **Order Placement**: Submit buy and sell orders with automatic matching
- **Matching Engine**: Price-time priority order matching algorithm
- **Trade Recording**: Persistent storage of all executed trades
- **Order Book**: Real-time view of active buy and sell orders
- **Order Cancellation**: Cancel open orders before execution
- **Concurrency Handling**: Thread-safe order matching with locks
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Python**: 3.10+
- **Concurrency**: Thread locks for race condition prevention

## Project Structure

```
trading_engine/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database/
│   │   └── db.py              # Database configuration and session
│   ├── models/
│   │   ├── user_model.py      # User database model
│   │   ├── order_model.py     # Order database model
│   │   └── trade_model.py     # Trade database model
│   ├── schemas/
│   │   ├── user_schema.py     # User Pydantic schemas
│   │   ├── order_schema.py    # Order Pydantic schemas
│   │   └── trade_schema.py    # Trade Pydantic schemas
│   ├── services/
│   │   ├── user_service.py    # User business logic
│   │   ├── order_service.py   # Order business logic
│   │   └── matching_engine.py # Order matching algorithm
│   └── routers/
│       ├── user_router.py     # User API endpoints
│       └── order_router.py    # Order API endpoints
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd trading_engine
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### User Management

- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID

### Order Management

- `POST /orders/` - Place a new order
- `GET /orders/{order_id}` - Get order by ID
- `GET /orders/user/{user_id}` - Get all orders for a user
- `DELETE /orders/{order_id}` - Cancel an order
- `GET /orders/orderbook/{symbol}` - Get order book for a symbol

### Trade Information

- `GET /orders/trades/all` - Get all trades
- `GET /orders/trades/{symbol}` - Get trades for a specific symbol

### Health Check

- `GET /health` - Application health status

## API Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "balance": 100000.0
     }'
```

### Place a Buy Order

```bash
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "symbol": "BTC",
       "side": "BUY",
       "price": 50000.0,
       "quantity": 2
     }'
```

### Place a Sell Order

```bash
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 2,
       "symbol": "BTC",
       "side": "SELL",
       "price": 50000.0,
       "quantity": 1
     }'
```

### Get Order Book

```bash
curl "http://localhost:8000/orders/orderbook/BTC"
```

### Cancel an Order

```bash
curl -X DELETE "http://localhost:8000/orders/1"
```

## Matching Engine Logic

The matching engine follows standard exchange principles:

1. **Price Priority**: 
   - Buy orders: Higher price gets priority
   - Sell orders: Lower price gets priority

2. **Time Priority**: 
   - Orders with same price are matched by creation time (FIFO)

3. **Matching Condition**:
   - Buy order price ≥ Sell order price

4. **Order Status Updates**:
   - `OPEN` → `PARTIALLY_FILLED` → `FILLED`
   - Orders can be `CANCELLED` when still `OPEN`

## Database Schema

### Users Table
- `id`: Primary key
- `name`: User name
- `balance`: Account balance
- `created_at`: Registration timestamp

### Orders Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `symbol`: Trading symbol (e.g., "BTC")
- `side`: BUY or SELL
- `price`: Order price
- `quantity`: Order quantity
- `remaining_quantity`: Unfilled quantity
- `status`: Order status
- `created_at`: Order creation time
- `updated_at`: Last update time

### Trades Table
- `id`: Primary key
- `buy_order_id`: Foreign key to buy order
- `sell_order_id`: Foreign key to sell order
- `price`: Execution price
- `quantity`: Executed quantity
- `executed_at`: Trade execution time

## Concurrency Handling

The system implements robust concurrency handling to prevent race conditions when multiple orders are submitted simultaneously.

### Thread-Safe Order Matching

When an order is placed:

1. **Thread Lock Acquisition**: The matching engine acquires a thread lock to ensure atomic processing
2. **Database Transaction**: All operations occur within a single database transaction
3. **Order Locking**: Opposite orders are locked during matching process
4. **Atomic Execution**: Trades are executed and orders are updated atomically
5. **Lock Release**: Thread lock is released after completion

### Implementation Details

```python
class MatchingEngine:
    def __init__(self, db: Session):
        self.db = db
        self._lock = Lock()  # Thread lock for race condition prevention
    
    def match_order(self, new_order: Order) -> List[Trade]:
        with self._lock:  # Ensure atomic processing
            # Matching logic here
            trades = self._execute_matching(new_order)
            self.db.commit()  # Atomic database transaction
            return trades
```

### Race Condition Prevention

- **Thread Locks**: Prevent simultaneous order processing
- **Database Transactions**: Ensure data consistency
- **Atomic Operations**: Order status updates and trade creation in single transaction
- **Optimistic Locking**: Database-level concurrency control

This prevents:
- Double matching of the same order
- Inconsistent order book state
- Race conditions in trade execution

## Database Schema

The system uses three main tables with proper relationships:

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| name | String | User name |
| balance | Float | Account balance |
| created_at | DateTime | Registration timestamp |

### Orders Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| user_id | Integer | Foreign key to users.id |
| symbol | String | Trading symbol (e.g., "BTC") |
| side | Enum | BUY or SELL |
| price | Float | Order price |
| quantity | Integer | Original order quantity |
| remaining_quantity | Integer | Unfilled quantity |
| status | Enum | OPEN, PARTIALLY_FILLED, FILLED, CANCELLED |
| created_at | DateTime | Order creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Trades Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-increment |
| buy_order_id | Integer | Foreign key to orders.id (buy side) |
| sell_order_id | Integer | Foreign key to orders.id (sell side) |
| price | Float | Execution price |
| quantity | Integer | Executed quantity |
| executed_at | DateTime | Trade execution timestamp |

### Relationships
- Users → Orders (One-to-Many)
- Orders → Trades (One-to-Many, both buy and sell sides)

## Order Flow

### Simple Flow Diagram

```
Client
   ↓
FastAPI Router
   ↓
Order Service
   ↓
Matching Engine
   ↓
Trade Execution
   ↓
Database
```

### Detailed Architecture Diagram

```
        +-------------+
        |   Client    |
        +-------------+
               |
               v
        +-------------+
        |  FastAPI    |
        |   Router    |
        +-------------+
               |
               v
        +-------------+
        | Order       |
        |  Service    |
        +-------------+
               |
               v
        +-------------+
        | Matching    |
        |  Engine     |
        +-------------+
               |
               v
        +-------------+
        | Trade       |
        | Execution   |
        +-------------+
               |
               v
        +-------------+
        |  Database   |
        +-------------+
```

### Data Flow Sequence

```
1. Client → HTTP Request → FastAPI Router
2. Router → Validation → Order Service  
3. Service → Balance Check → User Validation
4. Service → Order Creation → Matching Engine
5. Engine → Order Matching → Trade Execution
6. Engine → Database Update → Order Status Update
7. Database → Response → Service → Router → Client
```

## System Architecture

The application follows clean layered architecture:

```
Client (HTTP Requests)
        │
        ▼
FastAPI Router Layer
        │
        ▼
Service Layer (Business Logic)
        │
        ▼
Matching Engine (Order Processing)
        │
        ▼
Database Layer (SQLite + SQLAlchemy)
```

### Layer Responsibilities

1. **Router Layer**: HTTP request handling, validation, response formatting
2. **Service Layer**: Business logic, data processing, orchestration
3. **Matching Engine**: Order matching algorithm, trade execution
4. **Database Layer**: Data persistence, transaction management

### Data Flow

1. HTTP request → Router → Service
2. Service → Matching Engine → Database
3. Database → Matching Engine → Service → Router → Response

## Project Structure

```
trading_engine/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database/
│   │   └── db.py              # Database configuration and session
│   ├── models/
│   │   ├── user_model.py      # User database model
│   │   ├── order_model.py     # Order database model
│   │   └── trade_model.py     # Trade database model
│   ├── schemas/
│   │   ├── user_schema.py     # User Pydantic schemas
│   │   ├── order_schema.py    # Order Pydantic schemas
│   │   └── trade_schema.py    # Trade Pydantic schemas
│   ├── services/
│   │   ├── user_service.py    # User business logic
│   │   ├── order_service.py   # Order business logic
│   │   └── matching_engine.py # Order matching algorithm
│   ├── routers/
│   │   ├── user_router.py     # User API endpoints
│   │   └── order_router.py    # Order API endpoints
│   └── utils/                 # Utility functions
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── API_DOCUMENTATION.md        # API reference
└── .gitignore                # Git ignore file
```

### Modular Architecture Benefits

- **Separation of Concerns**: Each layer has specific responsibility
- **Maintainability**: Easy to modify individual components
- **Testability**: Components can be tested independently
- **Scalability**: Easy to add new features or modify existing ones

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd trading_engine
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Verification

1. **Check health endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test basic functionality**:
   ```bash
   # Create a user
   curl -X POST "http://localhost:8000/users/" \
        -H "Content-Type: application/json" \
        -d '{"name": "Test User", "balance": 10000.0}'
   ```

### Development Setup

For development with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag automatically restarts the server when code changes are detected.

## Order Validation Rules

### Balance Validation

Buy orders require sufficient user balance to prevent overspending.

**Required Balance Calculation:**
```
required_balance = order_price × order_quantity
```

**Example:**
- Order: BUY 2 BTC at ₹50,000 each
- Required Balance: ₹50,000 × 2 = ₹100,000
- User must have ≥ ₹100,000 balance to place this order

**Implementation:**
```python
if order.side == OrderSide.BUY:
    required_balance = order.price * order.quantity
    if user.balance < required_balance:
        raise ValueError("Insufficient balance for buy order")
```

### Self-Matching Prevention

Users cannot match against their own orders to prevent self-trading.

**Rule:**
- A user's buy order cannot match with their own sell orders
- This prevents price manipulation and self-trading risks

**Implementation:**
```python
# In matching engine
if buy_order.user_id == sell_order.user_id:
    continue  # Skip self-matching
```

## Edge Cases Handled

The system properly handles various edge cases to ensure robust operation:

### Order Processing Edge Cases
- **Partial Order Fills**: Orders can be partially filled, remaining quantity stays open
- **Order Cancellation**: Open orders can be cancelled before execution
- **Price Priority Matching**: Higher buy prices and lower sell prices get priority
- **Time Priority Matching**: Earlier orders at same price get priority
- **Race Condition Prevention**: Thread locks prevent simultaneous order conflicts

### Validation Edge Cases
- **Invalid User ID**: Validates user exists before order placement
- **Insufficient Balance**: Prevents buy orders exceeding user balance
- **Invalid Order Parameters**: Validates price > 0 and quantity > 0
- **Self-Matching Prevention**: Users cannot trade with themselves

### Data Consistency Edge Cases
- **Concurrent Order Processing**: Database transactions ensure atomicity
- **Order Status Updates**: Status changes are atomic and consistent
- **Trade Recording**: All trades are recorded with proper references

## Future Improvements

Potential enhancements to scale the system for production use:

### Performance & Scalability
- **Redis Order Book Caching**: Cache order book for faster reads
- **PostgreSQL Migration**: Replace SQLite for better concurrency
- **Database Connection Pooling**: Improve database performance
- **Horizontal Scaling**: Multiple matching engine instances

### Real-time Features
- **WebSocket Live Updates**: Real-time order book and trade updates
- **Kafka Trade Streaming**: Event-driven architecture for trade events
- **Live Market Data**: Real-time price feeds and charts

### Advanced Trading Features
- **Order Types**: Limit, market, stop-loss orders
- **Multiple Symbol Support**: Cross-symbol trading pairs
- **User Portfolio Tracking**: Real-time portfolio valuation
- **Trade History Analytics**: Advanced reporting and insights

### Infrastructure & Monitoring
- **Distributed Matching Engine**: Multiple engine instances with load balancing
- **Circuit Breakers**: Prevent system overload during high volatility
- **Comprehensive Logging**: Structured logging with ELK stack
- **Health Monitoring**: Prometheus metrics and Grafana dashboards

### Security & Compliance
- **API Rate Limiting**: Prevent abuse and ensure fair usage
- **User Authentication**: JWT-based authentication system
- **Audit Logging**: Complete audit trail for compliance
- **Data Encryption**: Encrypt sensitive user data

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database

The application uses SQLite by default. The database file (`trading_engine.db`) is created automatically when the application starts.

## License

This project is open source and available under the MIT License.
