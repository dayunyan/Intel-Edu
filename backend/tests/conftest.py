import os
os.environ["TESTING"] = "true"

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.models.base import Base
from app.db.init_db import init_db
from app.core.config import settings
from app.main import app
from app.deps import get_db

# 创建测试数据库引擎
test_engine = create_engine(settings.DATABASE_URL + "_test")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 覆盖依赖项
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    # Base.metadata.create_all(bind=test_engine)
    # print("Created test database tables successfully")
    
    db = TestingSessionLocal()
    try:
        # init_db(db)
        # print("Initialized test data successfully")
        
        # 验证数据是否正确插入，不使用 with db.begin()
        result = db.execute(text("SELECT username, email FROM users")).fetchall()
        print("Inserted users:", [{"username": row[0], "email": row[1]} for row in result])
        db.commit()  # 确保所有更改都已提交
        
        yield db
    finally:
        db.close()
        # Base.metadata.drop_all(bind=test_engine)
        # print("Dropped test database tables successfully")

@pytest.fixture(scope='session')
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope='session')
def headers(client):
    # 测试登录失败
    login_data_fail = {
        "username": "nonexistent",
        "password": "wrongpass"
    }
    response_fail = client.post("/api/v1/auth/token", data=login_data_fail)
    assert response_fail.status_code == 401

    # 测试登录成功，使用表单数据格式
    login_data = {
        "username": "student01",
        "password": "student123",
        "grant_type": "password"  # OAuth2 要求
    }
    response = client.post(
        "/api/v1/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=login_data
    )
    print(f"Login attempt response: {response.json() if response.status_code == 200 else response.text}")
    
    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}