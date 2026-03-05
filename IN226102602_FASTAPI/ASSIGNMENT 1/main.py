from fastapi import FastAPI,Query
 
app = FastAPI()
 
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
    in_stock:  bool = Query(None, description='True = in stock only')):
    result = products          # start with all products
    if category:
        result = [p for p in result if p['category'] == category]
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
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

# ── Endpoint 7 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id:int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}

# ── Endpoint 8 — Return store summary ──────────────────
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