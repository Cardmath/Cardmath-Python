from app import app, get_db
from database.creditcard.creditcard import CreditCard 
from database.sql_alchemy_db import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from tests.database.creditcard_generate import populate_all, all_cards
from typing import List

import pytest
import shutil

source_file = "./cardmath_9_20_24.db"
destination_file = "./cardmath_9_20_24_test.db"
shutil.copy(source_file, destination_file)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///" + destination_file

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_populate():
    db : Session = TestingSessionLocal()
    try:
        cards : List[CreditCard] = populate_all(db)
        assert set(cards) == set(all_cards)
    except Exception as e:
        print(e, "Error populating test database")
        assert False
    finally:
        db.close()

TEST_USERNAME_NO_ENROLLMENT = "generic_username"
TEST_PASSWORD_NO_ENROLLMENT = "generic_password"
def test_register_and_login_user():
    response = client.post( 
        url="/register",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={"username": TEST_USERNAME_NO_ENROLLMENT, "password": TEST_PASSWORD_NO_ENROLLMENT},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"] is not None
    
    
    response = client.post(
        "/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={"username": TEST_USERNAME_NO_ENROLLMENT, "password": TEST_PASSWORD_NO_ENROLLMENT},
    )
    assert response.status_code == 200
    assert data["access_token"] is not None
    

TEST_USERNAME_WITH_ENROLLMENT = "username"
TEST_PASSWORD_WITH_ENROLLMENT = "password"
def test_get_transactions():
    response = client.post(
        "/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={"username": TEST_USERNAME_WITH_ENROLLMENT, "password": TEST_PASSWORD_WITH_ENROLLMENT},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    access_token = data["access_token"]
    
    response = client.post(
        "/get_transactions",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["number"] > 0