# Performance and Stress Tests with Locust

This directory contains performance and stress tests for the e-commerce microservices using Locust.

## Prerequisites

1. Install Python 3.7 or higher
2. Install Locust:
```bash
pip install locust
```

## Running the Tests

### Basic Usage

Run all tests with default settings:
```bash
locust -f locustfile.py --host=http://localhost:8080
```

### Run with UI

Access the Locust web UI:
```bash
locust -f locustfile.py --host=http://localhost:8080 --web-host=0.0.0.0 --web-port=8089
```

Then open your browser to: `http://localhost:8089`

### Run Headless (No UI)

Run tests without the web UI:
```bash
locust -f locustfile.py --host=http://localhost:8080 --headless -u 100 -r 10 -t 60s
```

Where:
- `-u 100`: 100 concurrent users
- `-r 10`: 10 users per second spawn rate
- `-t 60s`: Run for 60 seconds

### Run Specific Test Scenarios

#### High Load Stress Test
```bash
locust -f locustfile.py --host=http://localhost:8080 -u 1000 -r 50 -t 5m --class HighLoadUser
```

#### Shopping Flow Test
```bash
locust -f locustfile.py --host=http://localhost:8080 -u 50 -r 5 -t 10m --class ShoppingFlowUser
```

#### User Service Performance Test
```bash
locust -f locustfile.py --host=http://localhost:8080 -u 200 -r 20 -t 5m --class UserServicePerformanceTest
```

#### Order Service Performance Test
```bash
locust -f locustfile.py --host=http://localhost:8080 -u 200 -r 20 -t 5m --class OrderServicePerformanceTest
```

## Test Scenarios

### 1. EcommerceUser (Main User Class)
- Simulates typical e-commerce user behavior
- Includes:
  - User registration (10%)
  - Product browsing (40%)
  - Favourite management (20%)
  - Order creation (20%)
  - Payment processing (10%)

### 2. HighLoadUser
- Stress testing with rapid API calls
- Very short wait times between requests
- Tests system resilience under high load

### 3. ShoppingFlowUser
- Complete shopping flow simulation
- Sequential tasks: Register → Browse → Order → Payment

### 4. UserServicePerformanceTest
- Focused on user service endpoints
- Tests user CRUD operations

### 5. OrderServicePerformanceTest
- Focused on order service endpoints
- Tests order CRUD operations

## Test Cases Covered

### Real-World Use Cases

1. **User Registration Flow**
   - New user registration
   - Profile management

2. **Product Browsing**
   - Browse all products
   - View specific products
   - Search functionality

3. **Favourite Management**
   - Add products to favourites
   - View user favourites
   - Remove favourites

4. **Order Management**
   - Create orders
   - View order history
   - Update order status
   - Cancel orders

5. **Payment Processing**
   - Create payments
   - Process payments
   - View payment history

6. **Complete Shopping Flow**
   - End-to-end shopping experience
   - From registration to payment completion

## Performance Metrics

The tests measure:
- **Response Time**: Average, min, max response times
- **Requests per Second (RPS)**: Throughput measurement
- **Failure Rate**: Percentage of failed requests
- **User Count**: Number of concurrent users

## Expected Results

### Normal Load
- Response time < 200ms for 95% of requests
- Failure rate < 1%
- RPS > 100

### High Load
- Response time < 1s for 95% of requests
- Failure rate < 5%
- RPS > 500

### Stress Test
- System remains responsive
- Graceful degradation under extreme load
- No memory leaks or crashes

## Configuration

Update the `host` parameter in the command to point to your API Gateway:
- Development: `http://localhost:8080`
- Staging: `http://staging-api.example.com`
- Production: `http://api.example.com`

## Notes

- Ensure all microservices are running before executing tests
- Start with low user counts and gradually increase
- Monitor system resources during tests
- Review logs for errors and performance issues

