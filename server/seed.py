import random
from faker import Faker
from config import app, db, bcrypt
from models import User

fake = Faker()

# Function to generate a random gender
def generate_gender():
    genders = ["male", "female"]
    return random.choice(genders)

# Create a Flask application context
with app.app_context():

    # Create and insert 10 users
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}"
        password = fake.password(length=10)  # Generate a random password
        gender = generate_gender()

        # Create a new user instance
        new_user = User(username=username)

        # Set the password using the setter method
        new_user.password_hash = password

        db.session.add(new_user)

    # Commit the changes to the database
    db.session.commit()

print("Database seeded with 10 users.")
