from fastapi import FastAPI
from routes.booking_routes import router as booking_router
from routes.passenger_routes import router as passenger_router
from routes.payment_routes import router as payment_router
from routes.train_routes import router as train_router

app = FastAPI()

app.include_router(train_router)
app.include_router(passenger_router)
app.include_router(booking_router)
app.include_router(payment_router)


@app.get("/")
def root():
    return {"message": "Railway Management System API is running"}