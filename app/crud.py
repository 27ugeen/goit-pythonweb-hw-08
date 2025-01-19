from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate
from typing import List, Optional
from datetime import date, timedelta

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact_by_id(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> bool:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return False
    db.delete(db_contact)
    db.commit()
    return True

def search_contacts(db: Session, query: str) -> List[Contact]:
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()

def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.birthday >= today,
        Contact.birthday <= next_week
    ).all()