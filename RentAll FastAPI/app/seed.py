"""Filling the database with dummy data for development.

Run from the project folder:
    python -m app.seed            # only works on an empty database
    python -m app.seed --reset    # deletes ALL existing rows first

Every user's password is: password123
"""
import random
import sys
from datetime import datetime, timedelta

from sqlalchemy import delete, func, select

from app.database import SessionLocal
from app.models import Car, CarImage, Like, Rental, User
from app.security import hash_password

random.seed(42)

PASSWORD = "password123"

USERS = [
    ("Giorgi", "Beridze", "591299899", "giorgi@example.com"),
    ("Nino", "Kapanadze", "592111222", "nino@example.com"),
    ("Luka", "Maisuradze", "593333444", "luka@example.com"),
    ("Mariam", "Gelashvili", "595555666", "mariam@example.com"),
    ("Davit", "Lomidze", "597777888", "davit@example.com"),
    ("Ana", "Tsiklauri", "598999000", "ana@example.com"),
]

CARS = [
    ("Mercedes", "E320", 2015, 90, 4, "automatic", "Tbilisi", 80),
    ("Toyota", "Prius", 2012, 45, 4, "automatic", "Tbilisi", 45),
    ("Toyota", "Camry", 2018, 80, 4, "automatic", "Batumi", 60),
    ("Toyota", "Sienna", 2004, 70, 7, "automatic", "Batumi", 75),
    ("Honda", "Fit", 2010, 35, 4, "tiptronic", "Kutaisi", 40),
    ("Hyundai", "Elantra", 2017, 55, 4, "automatic", "Tbilisi", 50),
    ("Hyundai", "H-1", 2008, 85, 8, "manual", "Batumi", 75),
    ("BMW", "X5", 2016, 150, 5, "tiptronic", "Tbilisi", 85),
    ("BMW", "320i", 1999, 40, 4, "manual", "Rustavi", 63),
    ("Mitsubishi", "Delica", 1997, 60, 6, "manual", "Kutaisi", 65),
    ("Lexus", "RX 350", 2019, 140, 5, "automatic", "Tbilisi", 72),
    ("Ford", "Transit", 2011, 95, 9, "manual", "Zugdidi", 80),
    ("Kia", "Sportage", 2020, 75, 5, "automatic", "Batumi", 62),
    ("Volkswagen", "Golf", 2003, 30, 4, "manual", "Rustavi", 55),
    ("Subaru", "Forester", 2014, 65, 5, "tiptronic", "Kutaisi", 60),
    ("Mercedes", "Vito", 2005, 80, 6, "manual", "Zugdidi", 75),
]


def clear_all(db) -> None:
    for model in (Rental, Like, CarImage, Car, User):
        db.execute(delete(model))
    db.commit()


def seed(db) -> None:
    hashed = hash_password(PASSWORD)
    users = [
        User(first_name=f, last_name=l, phone=p, email=e, hashed_password=hashed)
        for f, l, p, e in USERS
    ]
    db.add_all(users)

    cars = []
    for brand, model, year, price, capacity, transmission, city, tank in CARS:
        cars.append(Car(
            brand=brand, model=model, release_year=year, price_per_day=price,
            capacity=capacity, transmission=transmission, city=city,
            fuel_tank_capacity=tank,
            owner=random.choice(users),
        ))
    db.add_all(cars)

    for user in users:
        others = [c for c in cars if c.owner is not user]
        for car in random.sample(others, random.randint(2, 6)):
            db.add(Like(user=user, car=car))

    now = datetime.now()
    for _ in range(14):
        renter = random.choice(users)
        car = random.choice([c for c in cars if c.owner is not renter])
        days = random.randint(1, 10)
        rented_at = now - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))

        db.add(Rental(
            user=renter, car=car, days=days,
            total_price=days * car.price_per_day,
            created_at=rented_at,
        ))

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        if "--reset" in sys.argv:
            clear_all(db)
            print("Deleted all existing rows.")
        elif db.scalar(select(func.count(User.id))):
            print("The database already has data. Run with --reset to wipe it and seed again.")
            return

        seed(db)

        for model in (User, Car, Like, Rental):
            print(f"{model.__tablename__:<8} {db.scalar(select(func.count()).select_from(model))}")
        print(f"\nLog in with any phone number below and the password: {PASSWORD}")
        for first, last, phone, _ in USERS:
            print(f"  {phone}  {first} {last}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
