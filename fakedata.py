from faker import Faker

from db.base import SessionLocal
from db.models.user import User
from hashlib import sha256

def fake_users():
    Faker.seed(0)
    fake = Faker()

    users = []
    for _ in range(50):
        users.append(User(
            first_name=fake.name(),
            last_name=fake.name(),
            third_name=fake.name(),
            e_mail=fake.ascii_company_email(),
            password=sha256(fake.name().encode('utf-8')).hexdigest()
        ))

    return users


session = SessionLocal()

session.add_all(fake_users())
session.commit()

for instance in session.query(User).order_by(User.id):
    print(instance.name)
