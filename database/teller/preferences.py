from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

class CreditProfilePreferences(Base):
    __tablename__ = 'credit_profile_preferences'
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

class TravelPreferences(Base):
    __tablename__ = 'travel_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="travel_preferences")

    preferred_airlines = Column(JSON, nullable=True)
    avoid_airlines = Column(JSON, nullable=True)
    frequent_travel_destinations = Column(JSON, nullable=True)
    desired_benefits = Column(JSON, nullable=True)

class ConsumerPreferences(Base):
    __tablename__ = 'consumer_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="consumer_preferences")

    favorite_restaurants = Column(JSON, nullable=True)
    favorite_stores = Column(JSON, nullable=True)

class BusinessPreferences(Base):
    __tablename__ = 'business_preferences'
    user_id = Column(Integer, ForeignKey('preferences.user_id'), primary_key=True)
    preferences = relationship("Preferences", back_populates="business_preferences")

    business_type = Column(String, nullable=True)
    business_size = Column(String, nullable=True)
    

class Preferences(Base):
    __tablename__ = 'preferences'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship("User", back_populates="preferences")
    
    credit_profile = relationship("CreditProfilePreferences", uselist=False, back_populates="preferences")
    banks_preferences = relationship("BanksPreferences", uselist=False, back_populates="preferences")
    travel_preferences = relationship("TravelPreferences", uselist=False, back_populates="preferences")
    consumer_preferences = relationship("ConsumerPreferences", uselist=False, back_populates="preferences")
    business_preferences = relationship("BusinessPreferences", uselist=False, back_populates="preferences")