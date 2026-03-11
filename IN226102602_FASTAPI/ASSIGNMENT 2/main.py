from fastapi import FastAPI,Query
 
app = FastAPI()
 
# ══ HELPER FUNCTIONS ═══════════════════════════════════════
def find_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    return None
 
def calculate_total(product: dict, quantity: int) -> int:
    return product['price'] * quantity
 
def filter_products_logic(category=None, min_price=None,
                          max_price=None, in_stock=None):
    result = products
    if category  is not None: result = [p for p in result if p['category']==category]
    if min_price is not None: result = [p for p in result if p['price']>=min_price]
    if max_price is not None: result = [p for p in result if p['price']<=max_price]
    if in_stock  is not None: result = [p for p in result if p['in_stock']==in_stock]
    return result

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook', 'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": False},
    {"id": 7, "name": "Stapler Set", "price": 199, "category": "Stationery", "in_stock": False},
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── Endpoint 2 — Return products by filtering ──────────────────
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    min_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')):
    result = products          # start with all products
    if category:
        result = [p for p in result if p['category'] == category]
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
    if min_price:
        result = [p for p in result if p['price'] >= min_price]    
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return {'filtered_products': result, 'count': len(result)}

# ── Endpoint 3 — Return products that are available  ──────────────────
@app.get('/products/instock')
def product_instock():
    instock=[product for product in products if product['in_stock']]
    return {"in_stock_products":instock,"count":len(instock)}

# ── Endpoint 4 — Return product deals  ──────────────────
@app.get('/products/deals')
def product_deals():
    best_deal=min(products, key=lambda product:product['price'])
    premium_pick=max(products, key=lambda product:product['price'])
    return{"best_deal":best_deal,"premium_pick":premium_pick}

# ── Endpoint 5 — Return products by its category ──────────────────
@app.get('/products/category/{category_name}')
def product_by_category(category_name:str):
    result=[product for product in products 
            if product['category'].lower()==category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return {"category":category_name,"products":result,"count":len(result)}

# ── Endpoint 6 — Return products by name ──────────────────
@app.get('/products/search/{keyword}')
def search_by_name(keyword:str):
    result=[product for product in products 
            if keyword.lower() in product['name'].lower()]
    if not result:
        return {"message": "No products matched your search"}
    return {"keyword":keyword,"results":result,"count":len(result)}

# ── Endpoint 7 — Return product summary ──────────────────
@app.get('/products/summary')
def product_summary():
    total_products = len(products)
    in_stock_count = sum(p['in_stock'] for p in products)
    out_of_stock_count = total_products - in_stock_count
    most_expensive_product = max(products, key=lambda p: p['price'])
    cheapest_product = min(products, key=lambda p: p['price'])
    categories = list({p['category'] for p in products})
    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive_product["name"],
            "price": most_expensive_product["price"]
        },
        "cheapest": {
            "name": cheapest_product["name"],
            "price": cheapest_product["price"]
        },
        "categories": categories
    }

# ── Endpoint 8 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id:int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

# ── Endpoint 9 — Return Name and Price ──────────────────
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"]==product_id:
            return {"name":product["name"],"price": product["price"]}
    return {"error": "Product not found"}

# ── Endpoint 10 — Return store summary ──────────────────
@app.get('/store/summary')
def store_summary():
    store_name="Tony's Ecommerce Store"
    total_products=len(products)
    instock=sum(product['in_stock'] for product in products)
    outofstock=total_products-instock
    categories=list({product['category'] for product in products})
    return { "store_name": store_name,
            "total_products": total_products,
            "in_stock": instock,
            "out_of_stock": outofstock, 
            "categories": categories }


#  Imported pydentic
from pydantic import BaseModel, Field
from typing import Optional,List

feedback = []
orders = []
order_counter = 1

# Create model
class OrderRequest(BaseModel):
    customer_name:    str = Field(..., min_length=2, max_length=100)
    product_id:       int = Field(..., gt=0)
    quantity:         int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_length=1)

# ── Endpoint 11 — Add orders ──────────────────
@app.post('/orders')
def create_order(order: BulkOrder):
    global order_counter
    new_order = {
        "order_id": order_counter,
        "company": order.company_name,
        "items": [item.dict() for item in order.items],
        "status": "pending"
    }
    orders.append(new_order)
    order_counter += 1
    return {
        "message": "Order placed successfully",
        "order": new_order
    }

# ── Endpoint 12 — Bulk orders ──────────────────
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue
        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue
        subtotal = product["price"] * item.quantity
        grand_total += subtotal
        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })
    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# ── Endpoint 13 — Add feedback ──────────────────
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())
    return {
        "message":        "Feedback submitted successfully",
        "feedback":       data.dict(),
        "total_feedback": len(feedback),
    }

# ── Endpoint 14 — Get order  ──────────────────
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}

# ── Endpoint 15 — Patch ──────────────────
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            if order["status"] == "confirmed":
                return {"message": "Order already confirmed"}
            order["status"] = "confirmed"
            return {
                "message": "Order confirmed",
                "order": order
            }
    return {"error": "Order not found"}