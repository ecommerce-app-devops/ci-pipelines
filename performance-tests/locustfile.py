"""
Locust Performance and Stress Tests for E-commerce Microservices
This file contains performance tests simulating real-world usage scenarios.
"""

from locust import HttpUser, task, between, SequentialTaskSet
import json
import random


class UserRegistrationTaskSet(SequentialTaskSet):
    """Simulates user registration flow"""
    
    def on_start(self):
        """Called when a user starts"""
        self.user_id = None
        self.user_data = {
            "firstName": f"TestUser{random.randint(1000, 9999)}",
            "lastName": "Performance",
            "email": f"test{random.randint(1000, 9999)}@example.com",
            "phone": f"{random.randint(1000000000, 9999999999)}"
        }
    
    @task
    def register_user(self):
        """Register a new user"""
        with self.client.post(
            "/api/users",
            json=self.user_data,
            catch_response=True,
            name="Register User"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.user_id = data.get("userId")
                    response.success()
                except:
                    response.failure("Invalid response format")
            else:
                response.failure(f"Status code: {response.status_code}")


class ProductBrowseTaskSet(SequentialTaskSet):
    """Simulates product browsing flow"""
    
    @task
    def browse_products(self):
        """Browse all products"""
        self.client.get("/api/products", name="Browse Products")
    
    @task
    def view_product(self):
        """View a specific product"""
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", name="View Product")


class FavouriteManagementTaskSet(SequentialTaskSet):
    """Simulates managing favourites"""
    
    def on_start(self):
        """Setup test data"""
        self.user_id = random.randint(1, 1000)
        self.product_id = random.randint(1, 100)
    
    @task
    def add_to_favourites(self):
        """Add product to favourites"""
        favourite_data = {
            "userId": self.user_id,
            "productId": self.product_id
        }
        with self.client.post(
            "/api/favourites",
            json=favourite_data,
            catch_response=True,
            name="Add to Favourites"
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task
    def view_favourites(self):
        """View user favourites"""
        self.client.get("/api/favourites", name="View Favourites")


class OrderCreationTaskSet(SequentialTaskSet):
    """Simulates order creation flow"""
    
    def on_start(self):
        """Setup test data"""
        self.cart_id = random.randint(1, 1000)
    
    @task
    def create_order(self):
        """Create a new order"""
        order_data = {
            "orderDesc": f"Performance Test Order {random.randint(1000, 9999)}",
            "orderFee": round(random.uniform(10.0, 500.0), 2),
            "cart": {
                "cartId": self.cart_id
            }
        }
        with self.client.post(
            "/api/orders",
            json=order_data,
            catch_response=True,
            name="Create Order"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.order_id = data.get("orderId")
                    response.success()
                except:
                    response.failure("Invalid response format")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task
    def view_orders(self):
        """View all orders"""
        self.client.get("/api/orders", name="View Orders")


class PaymentProcessingTaskSet(SequentialTaskSet):
    """Simulates payment processing flow"""
    
    def on_start(self):
        """Setup test data"""
        self.order_id = random.randint(1, 1000)
    
    @task
    def create_payment(self):
        """Create a payment for an order"""
        payment_data = {
            "orderDto": {
                "orderId": self.order_id
            }
        }
        with self.client.post(
            "/api/payments",
            json=payment_data,
            catch_response=True,
            name="Create Payment"
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task
    def view_payments(self):
        """View all payments"""
        self.client.get("/api/payments", name="View Payments")


class EcommerceUser(HttpUser):
    """
    Main user class that simulates a typical e-commerce user behavior
    """
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between tasks
    
    tasks = {
        UserRegistrationTaskSet: 10,  # 10% of users register
        ProductBrowseTaskSet: 40,      # 40% browse products
        FavouriteManagementTaskSet: 20,  # 20% manage favourites
        OrderCreationTaskSet: 20,      # 20% create orders
        PaymentProcessingTaskSet: 10   # 10% process payments
    }
    
    def on_start(self):
        """Called when a simulated user starts"""
        pass


class HighLoadUser(HttpUser):
    """
    High-load user class for stress testing
    Simulates rapid API calls
    """
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    @task(3)
    def browse_products(self):
        """Frequent product browsing"""
        self.client.get("/api/products", name="High Load - Browse Products")
    
    @task(2)
    def view_products(self):
        """Frequent product viewing"""
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", name="High Load - View Product")
    
    @task(1)
    def view_users(self):
        """User listing"""
        self.client.get("/api/users", name="High Load - View Users")


class ShoppingFlowUser(HttpUser):
    """
    User class that simulates complete shopping flow
    """
    wait_time = between(2, 5)
    
    def on_start(self):
        """Initialize shopping flow"""
        self.user_id = None
        self.order_id = None
    
    @task
    def complete_shopping_flow(self):
        """Complete shopping flow: register -> browse -> order -> payment"""
        # Step 1: Register user
        user_data = {
            "firstName": f"ShopUser{random.randint(1000, 9999)}",
            "lastName": "Flow",
            "email": f"shop{random.randint(1000, 9999)}@example.com",
            "phone": f"{random.randint(1000000000, 9999999999)}"
        }
        
        with self.client.post("/api/users", json=user_data, catch_response=True, name="Flow - Register") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.user_id = data.get("userId")
                except:
                    pass
        
        # Step 2: Browse products
        self.client.get("/api/products", name="Flow - Browse")
        
        # Step 3: Create order (if user was created)
        if self.user_id:
            order_data = {
                "orderDesc": "Shopping Flow Order",
                "orderFee": round(random.uniform(50.0, 300.0), 2),
                "cart": {"cartId": random.randint(1, 1000)}
            }
            with self.client.post("/api/orders", json=order_data, catch_response=True, name="Flow - Order") as response:
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.order_id = data.get("orderId")
                    except:
                        pass


# Performance test scenarios
class UserServicePerformanceTest(HttpUser):
    """Performance test focused on user service"""
    wait_time = between(0.5, 2)
    
    @task(5)
    def get_users(self):
        """Get all users"""
        self.client.get("/api/users", name="User Service - Get All")
    
    @task(3)
    def get_user_by_id(self):
        """Get user by ID"""
        user_id = random.randint(1, 1000)
        self.client.get(f"/api/users/{user_id}", name="User Service - Get By ID")
    
    @task(2)
    def create_user(self):
        """Create new user"""
        user_data = {
            "firstName": f"PerfUser{random.randint(1000, 9999)}",
            "lastName": "Test",
            "email": f"perf{random.randint(1000, 9999)}@example.com",
            "phone": f"{random.randint(1000000000, 9999999999)}"
        }
        self.client.post("/api/users", json=user_data, name="User Service - Create")


class OrderServicePerformanceTest(HttpUser):
    """Performance test focused on order service"""
    wait_time = between(0.5, 2)
    
    @task(5)
    def get_orders(self):
        """Get all orders"""
        self.client.get("/api/orders", name="Order Service - Get All")
    
    @task(3)
    def get_order_by_id(self):
        """Get order by ID"""
        order_id = random.randint(1, 1000)
        self.client.get(f"/api/orders/{order_id}", name="Order Service - Get By ID")
    
    @task(2)
    def create_order(self):
        """Create new order"""
        order_data = {
            "orderDesc": f"Perf Order {random.randint(1000, 9999)}",
            "orderFee": round(random.uniform(10.0, 500.0), 2),
            "cart": {"cartId": random.randint(1, 1000)}
        }
        self.client.post("/api/orders", json=order_data, name="Order Service - Create")


if __name__ == "__main__":
    # Run with: locust -f locustfile.py --host=http://localhost:8080
    pass

