# Trading Engine API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for this demo.

---

## User Management APIs

### 1. Create User
**POST** `/users/`

Create a new user with initial balance.

**Request Body:**
```json
{
  "name": "string",
  "balance": "number"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice",
       "balance": 100000.0
     }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Alice",
  "balance": 100000.0,
  "created_at": "2026-03-11T11:22:21.123456"
}
```

---

### 2. Get All Users
**GET** `/users/`

Retrieve all users in the system.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/users/"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Alice",
    "balance": 100000.0,
    "created_at": "2026-03-11T11:22:21.123456"
  },
  {
    "id": 2,
    "name": "Bob",
    "balance": 50000.0,
    "created_at": "2026-03-11T11:22:25.789012"
  }
]
```

---

### 3. Get User by ID
**GET** `/users/{user_id}`

Retrieve a specific user by their ID.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/users/1"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Alice",
  "balance": 100000.0,
  "created_at": "2026-03-11T11:22:21.123456"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "User not found"
}
```

---

## Order Management APIs

### 4. Create Order
**POST** `/orders/`

Place a new buy or sell order.

**Request Body:**
```json
{
  "user_id": "integer",
  "symbol": "string",
  "side": "BUY|SELL",
  "price": "number",
  "quantity": "integer"
}
```

**Example - Buy Order:**
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

**Example - Sell Order:**
```bash
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 2,
       "symbol": "BTC",
       "side": "SELL",
       "price": 49500.0,
       "quantity": 1
     }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "BTC",
  "side": "BUY",
  "price": 50000.0,
  "quantity": 2,
  "remaining_quantity": 1,
  "status": "PARTIALLY_FILLED",
  "created_at": "2026-03-11T11:22:51.123456",
  "updated_at": "2026-03-11T11:22:51.789012"
}
```

**Possible Status Values:**
- `OPEN` - Order is active and waiting to be matched
- `PARTIALLY_FILLED` - Order has been partially executed
- `FILLED` - Order has been completely executed
- `CANCELLED` - Order has been cancelled by user

---

### 5. Get Order by ID
**GET** `/orders/{order_id}`

Retrieve a specific order by its ID.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/orders/1"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "symbol": "BTC",
  "side": "BUY",
  "price": 50000.0,
  "quantity": 2,
  "remaining_quantity": 1,
  "status": "PARTIALLY_FILLED",
  "created_at": "2026-03-11T11:22:51.123456",
  "updated_at": "2026-03-11T11:22:51.789012"
}
```

---

### 6. Get User Orders
**GET** `/orders/user/{user_id}`

Retrieve all orders for a specific user.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/orders/user/1"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "symbol": "BTC",
    "side": "BUY",
    "price": 50000.0,
    "quantity": 2,
    "remaining_quantity": 1,
    "status": "PARTIALLY_FILLED",
    "created_at": "2026-03-11T11:22:51.123456",
    "updated_at": "2026-03-11T11:22:51.789012"
  },
  {
    "id": 4,
    "user_id": 1,
    "symbol": "BTC",
    "side": "BUY",
    "price": 52000.0,
    "quantity": 1,
    "remaining_quantity": 0,
    "status": "FILLED",
    "created_at": "2026-03-11T11:23:11.345678",
    "updated_at": "2026-03-11T11:23:11.901234"
  }
]
```

---

### 7. Cancel Order
**DELETE** `/orders/{order_id}`

Cancel an open order. Only orders with status `OPEN` can be cancelled.

**Request Body:** None

**Example:**
```bash
curl -X DELETE "http://localhost:8000/orders/5"
```

**Response (200 OK):**
```json
{
  "id": 5,
  "user_id": 1,
  "symbol": "BTC",
  "side": "BUY",
  "price": 51500.0,
  "quantity": 2,
  "remaining_quantity": 2,
  "status": "CANCELLED",
  "created_at": "2026-03-11T11:23:19.123456",
  "updated_at": "2026-03-11T11:23:25.789012"
}
```

**Error Responses:**
- `404 Not Found`: Order doesn't exist
- `400 Bad Request`: Order cannot be cancelled (not in OPEN status)

---

## Order Book API

### 8. Get Order Book
**GET** `/orders/orderbook/{symbol}`

Retrieve the current order book for a specific symbol.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/orders/orderbook/BTC"
```

**Response (200 OK):**
```json
{
  "symbol": "BTC",
  "buy_orders": [
    {
      "price": 51500.0,
      "quantity": 2,
      "order_count": 1
    },
    {
      "price": 51000.0,
      "quantity": 5,
      "order_count": 3
    }
  ],
  "sell_orders": [
    {
      "price": 52000.0,
      "quantity": 3,
      "order_count": 2
    },
    {
      "price": 52500.0,
      "quantity": 1,
      "order_count": 1
    }
  ]
}
```

**Order Book Structure:**
- `buy_orders`: Sorted by price descending (highest price first)
- `sell_orders`: Sorted by price ascending (lowest price first)
- `quantity`: Total quantity at that price level
- `order_count`: Number of orders at that price level

---

## Trade Information APIs

### 9. Get All Trades
**GET** `/orders/trades/all`

Retrieve all executed trades in the system.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/orders/trades/all"
```

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "buy_order_id": 4,
    "sell_order_id": 3,
    "price": 51000.0,
    "quantity": 1,
    "executed_at": "2026-03-11T11:23:11.345678"
  },
  {
    "id": 1,
    "buy_order_id": 1,
    "sell_order_id": 2,
    "price": 50000.0,
    "quantity": 1,
    "executed_at": "2026-03-11T11:22:54.123456"
  }
]
```

---

### 10. Get Trades by Symbol
**GET** `/orders/trades/{symbol}`

Retrieve all executed trades for a specific symbol.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/orders/trades/BTC"
```

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "buy_order_id": 4,
    "sell_order_id": 3,
    "price": 51000.0,
    "quantity": 1,
    "executed_at": "2026-03-11T11:23:11.345678"
  },
  {
    "id": 1,
    "buy_order_id": 1,
    "sell_order_id": 2,
    "price": 50000.0,
    "quantity": 1,
    "executed_at": "2026-03-11T11:22:54.123456"
  }
]
```

---

## System APIs

### 11. Health Check
**GET** `/health`

Check if the system is running properly.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/health"
```

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

### 12. Root Endpoint
**GET** `/`

Get basic API information.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/"
```

**Response (200 OK):**
```json
{
  "message": "Trading Engine API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

---

## API Documentation

### 13. Swagger UI
**GET** `/docs`

Interactive API documentation with testing interface.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/docs"
```

---

### 14. ReDoc
**GET** `/redoc`

Alternative API documentation interface.

**Request Body:** None

**Example:**
```bash
curl "http://localhost:8000/redoc"
```

---

## Concurrency Handling

The system implements robust concurrency handling to prevent race conditions when multiple orders are submitted simultaneously.

### Thread-Safe Order Matching

When an order is placed:

1. **Thread Lock Acquisition**: The matching engine acquires a thread lock to ensure atomic processing
2. **Database Transaction**: All operations occur within a single database transaction
3. **Order Locking**: Opposite orders are locked during matching process
4. **Atomic Execution**: Trades are executed and orders are updated atomically
5. **Lock Release**: Thread lock is released after completion

### Race Condition Prevention

- **Thread Locks**: Prevent simultaneous order processing
- **Database Transactions**: Ensure data consistency
- **Atomic Operations**: Order status updates and trade creation in single transaction
- **Optimistic Locking**: Database-level concurrency control

This prevents:
- Double matching of the same order
- Inconsistent order book state
- Race conditions in trade execution

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

## Complete Trading Flow Example

### Step 1: Create Users
```bash
# Create Alice
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "balance": 100000.0}'

# Create Bob
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Bob", "balance": 50000.0}'
```

### Step 2: Place Orders
```bash
# Alice places a buy order
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "symbol": "BTC",
       "side": "BUY",
       "price": 50000.0,
       "quantity": 2
     }'

# Bob places a sell order (will match immediately)
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 2,
       "symbol": "BTC",
       "side": "SELL",
       "price": 49500.0,
       "quantity": 1
     }'
```

### Step 3: Check Results
```bash
# Check order book
curl "http://localhost:8000/orders/orderbook/BTC"

# Check executed trades
curl "http://localhost:8000/orders/trades/all"

# Check user orders
curl "http://localhost:8000/orders/user/1"
```

### Step 4: Cancel Order (if needed)
```bash
# Cancel an open order
curl -X DELETE "http://localhost:8000/orders/5"
```

---

## Error Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data or business logic error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Data Types

### OrderSide Enum
- `BUY` - Buy order
- `SELL` - Sell order

### OrderStatus Enum
- `OPEN` - Order is active
- `PARTIALLY_FILLED` - Order partially executed
- `FILLED` - Order completely executed
- `CANCELLED` - Order cancelled by user

---

## Matching Engine Rules

1. **Price Priority**: Higher buy prices and lower sell prices get priority
2. **Time Priority**: Earlier orders at same price get priority
3. **Matching Condition**: Buy price ≥ Sell price
4. **Execution Price**: Uses the resting order's price (maker price)
