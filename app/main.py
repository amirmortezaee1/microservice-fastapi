# uvicorn app.main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_methods=['*'],
    allow_headers=['*'],
    )

redis = get_redis_connection(
    host="redis-15431.c300.eu-central-1-1.ec2.cloud.redislabs.com:15431",
    port=11844,
    password="U0BlY5ynLG4SP2EQ4dEAzPawO3sFWkZr",
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis 

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    products = Product.get(pk)

    return{
        'id': products.id,
        'name': products.name,
        'price': products.price,
        'quantity': products.quantity,
    }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)
