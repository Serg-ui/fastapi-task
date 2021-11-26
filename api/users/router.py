from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import Session
from hashlib import sha256
from utils import get_db
from db.models.user import User
from api.users.schemas import CreateUserScheme, UpdateUserScheme, SearchUserScheme
from sqlalchemy import inspect

router = APIRouter()

user_attrs = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]


@router.get(path='/all')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get(path='/')
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User.id, User.first_name, User.last_name, User.e_mail).filter_by(id=user_id).one()
    except NoResultFound:
        return {'error': 'Несуществующий id'}
    return user


@router.put(path='/')
def update_user(data: UpdateUserScheme, db: Session = Depends(get_db)):
    data = data.dict()
    user_id = data['user_id']
    del data['user_id']

    try:
        user = db.query(User).filter_by(id=user_id).one()
    except NoResultFound:
        return {'error': 'Несуществующий id'}

    data = {k: v for k, v in data.items() if v}

    for key, value in data.items():
        if key in user_attrs:
            setattr(user, key, value)

    try:
        db.commit()
        return {'res': 'Данные успешно изменены'}
    except IntegrityError:
        return {'error': 'Такой email уже существует'}


@router.post(path='/')
def create_user(new_user: CreateUserScheme, db: Session = Depends(get_db)):
    new_user.password = sha256(new_user.password.encode('utf-8')).hexdigest()

    try:
        user = User(**new_user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        return {'error': 'Пользователь с таким email уже есть'}

    return {'res': f'Пользователь добавлен. id = {user.id}'}


@router.post(path='/search')
def search_users(data: SearchUserScheme, db: Session = Depends(get_db)):
    data = {k: v for k, v in data.dict().items() if v}

    if not data:
        return {}

    users = db.query(User)

    for key, value in data.items():

        if key in user_attrs:
            column = getattr(User, key)
            users = users.filter(column.like(f'%{value}%'))

    res = users.all()
    return res


@router.delete(path='/')
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(id=id).one()
        db.delete(user)
        db.commit()
    except NoResultFound:
        return {'error': 'Несуществующий id'}
    return {'res': 'Пользователь удален'}
