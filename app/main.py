from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

# app.add_middleware()

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
    return Product.all_pks()

