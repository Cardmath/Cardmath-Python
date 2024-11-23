from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

class CreditProfilePreferences(Base):
    __tablename__ = 'credit_profile_preferences'
    __table_args__ = (
        CheckConstraint('credit_score >= 300 AND credit_score <= 850', name='check_credit_score_range'),
        CheckConstraint('salary >= 0', name='check_positive_salary'),
    )
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="credit_profile")

    credit_score = Column(Integer, nullable=True)
    salary = Column(Integer, nullable=True)
    lifestyle = Column(String, nullable=True)

class BanksPreferences(Base):
    __tablename__ = 'banks_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="banks_preferences")

    have_banks = Column(JSON, nullable=True)
    preferred_banks = Column(JSON, nullable=True)
    avoid_banks = Column(JSON, nullable=True)

class RewardsProgramsPreferences(Base):
    __tablename__ = 'rewards_programs_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="rewards_programs_preferences")

    preferred_rewards_programs = Column(JSON, nullable=True)
    avoid_rewards_programs = Column(JSON, nullable=True)
    
class ConsumerPreferences(Base):
    __tablename__ = 'consumer_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="consumer_preferences")

    favorite_grocery_stores = Column(JSON, nullable=True)
    favorite_general_goods_stores = Column(JSON, nullable=True)

class BusinessPreferences(Base):
    __tablename__ = 'business_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="business_preferences")

    business_type = Column(JSON, nullable=True)
    business_size = Column(String, nullable=True)
    

class Preferences(Base):
    __tablename__ = 'preferences'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    credit_profile = relationship("CreditProfilePreferences", uselist=False, back_populates="preferences")
    banks_preferences = relationship("BanksPreferences", uselist=False, back_populates="preferences")
    rewards_programs_preferences = relationship("RewardsProgramsPreferences", uselist=False, back_populates="preferences")
    consumer_preferences = relationship("ConsumerPreferences", uselist=False, back_populates="preferences")
    business_preferences = relationship("BusinessPreferences", uselist=False, back_populates="preferences")