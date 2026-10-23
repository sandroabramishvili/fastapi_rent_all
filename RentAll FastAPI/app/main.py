from fastapi import FastAPI
from app.routers import auth, cars, home, likes, rentals, users


app = FastAPI(
    title = "RentAll",
    version= "1.0.0",
    description= "The place where you can rent all the cars you want..."
)

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cars.router)
app.include_router(rentals.router)
app.include_router(likes.router)
