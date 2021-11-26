from faker import Faker

from db.base import SessionLocal
from db.models.user import User


def fake_users():
    Faker.seed(0)
    fake = Faker()

    users = []
    for _ in range(50):
        users.append(User(
            name=fake.name(),
            phone=fake.phone_number(),
            e_mail=fake.ascii_company_email()
        ))

    return users


session = SessionLocal()

session.add_all(fake_users())
session.commit()

for instance in session.query(User).order_by(User.id):
    print(instance.name)
