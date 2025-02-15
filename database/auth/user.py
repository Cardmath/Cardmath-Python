from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint, JSON, Table, Date, CheckConstraint, ARRAY, FLOAT
from sqlalchemy.dialects.postgresql import ENUM, ARRAY, TIMESTAMP
from sqlalchemy.orm import relationship
from creditcard.enums import Archetype, Vendors, PurchaseCategory

archetype_enum = ENUM(
    Archetype,
    name='archetypes_enum',
    metadata=Base.metadata,
    values_callable=lambda enum: [e.value for e in enum],
    create_type=True,
)

user_credit_card_association = Table(
    'user_credit_card_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('credit_card_name', String, nullable=False, primary_key=True),
    Column('credit_card_issuer', String, nullable=False, primary_key=True),
    Column('credit_card_network', String, nullable=False, primary_key=True),
    ForeignKeyConstraint(
        ['credit_card_name', 'credit_card_issuer', 'credit_card_network'],
        ['credit_cards.name', 'credit_cards.issuer', 'credit_cards.network'],
        ondelete='CASCADE'
    )
)

wallet_card_association = Table(
    'wallet_new_card_association',
    Base.metadata,
    Column('wallet_id', Integer, ForeignKey('wallets.id', ondelete='CASCADE'), primary_key=True),
    Column('credit_card_name', String, nullable=False, primary_key=True),
    Column('credit_card_issuer', String, nullable=False, primary_key=True),
    Column('credit_card_network', String, nullable=False, primary_key=True),
    Column('is_held', Boolean, default=False, nullable=False),
    ForeignKeyConstraint(
        ['credit_card_name', 'credit_card_issuer', 'credit_card_network'],
        ['credit_cards.name', 'credit_cards.issuer', 'credit_cards.network'],
        ondelete='CASCADE'
    )
)

class Onboarding(Base):
    __tablename__ = 'onboarding'
    
    id= Column(Integer, primary_key=True, index=True, autoincrement=True)
    teller_id= Column(String, unique=True, index=True)
    expires_at = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    emails = Column(JSON(String), nullable=False)
    phone_numbers = Column(JSON(String), nullable=False)
    archetype = Column(archetype_enum, nullable=False)

    user = relationship("User", back_populates="onboarding", uselist=False, lazy='joined')
    enrollment = relationship("Enrollment", uselist=False, back_populates="onboarding", lazy='joined')
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    teller_ids = Column(ARRAY(String), index=True, nullable=False)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    
    onboarding = relationship("Onboarding", back_populates="user", uselist=False)
    subscription = relationship("Subscription", back_populates="user", uselist=False, single_parent=True, cascade="all, delete-orphan", foreign_keys=[subscription_id], lazy='joined')
    enrollments = relationship("Enrollment", back_populates="user", uselist=True, cascade="all, delete-orphan")
    credit_cards = relationship("CreditCard", secondary=user_credit_card_association, back_populates="users")
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")

class UserInDB(User):
    hashed_password = Column(String, nullable=True)

class Wallet(Base):
    __tablename__ = 'wallets'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="wallets")
    name = Column(String, nullable=False)
    last_edited = Column(Date, nullable=False)
    is_custom = Column(Boolean, default=False)
    cards = relationship("CreditCard", secondary=wallet_card_association, uselist=True)

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    onboarding_id = Column(Integer, ForeignKey('onboarding.id', ondelete='CASCADE'), nullable=True)
    access_token = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    signatures = Column(JSON, nullable=False)
    last_updated = Column(TIMESTAMP, nullable=False)
    
    user = relationship("User", back_populates="enrollments", foreign_keys=[user_id])
    onboarding = relationship("Onboarding", uselist=False, foreign_keys=[onboarding_id])
    accounts = relationship("Account", back_populates="enrollment", cascade="all, delete-orphan")
        
    __table_args__ = (
        CheckConstraint(
            '(user_id IS NOT NULL OR onboarding_id IS NOT NULL)',
            name='enrollment_owner_check'
        ),
    )
    
class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(String, primary_key=True, index=True)
    enrollment_id = Column(String, ForeignKey('enrollments.id', ondelete='CASCADE'), nullable=False)
    institution_name = Column(String, nullable=False)
    institution_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    subtype = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    last_four = Column(String, nullable=False)
    last_updated = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    
    enrollment = relationship("Enrollment", back_populates="accounts")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    
    status = Column(String, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="subscription", uselist=False)