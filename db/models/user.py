from db.base import Base
import sqlalchemy as sa


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    third_name = sa.Column(sa.String(255))
    e_mail = sa.Column(sa.String(255), unique=True)
    password = sa.Column(sa.String(512))
    created_at = sa.Column(sa.DateTime(), nullable=False, server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
