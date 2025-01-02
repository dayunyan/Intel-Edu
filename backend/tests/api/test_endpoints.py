import pytest
from datetime import datetime
from sqlalchemy import text
from app.main import app


def test_db(db):
    # 检查 'users' 表是否存在
    try:
        result = db.execute(text("SELECT 1 FROM users LIMIT 1")).fetchone()
        print("users 表存在")
    except Exception as e:
        pytest.fail(f"users 表不存在或查询失败: {e}")

    # 获取 'username' 列的内容
    try:
        result = db.execute(text("SELECT username FROM users")).fetchall()
        usernames = [row[0] for row in result]
        print("用户名列表:", usernames)

        # 验证是否包含我们期望的用户
        expected_users = ["admin", "teacher", "student01", "student02", "student03", "student04"]
        for username in expected_users:
            assert username in usernames, f"未找到用户: {username}"

    except Exception as e:
        pytest.fail(f"查询 username 列失败: {e}")


def test_student_data(headers, client):  # 增加client作为参数，接收TestClient实例夹具
    # 获取学生ID (假设 student01 的ID为3)
    student_id = 3

    # 测试创建行为记录
    behavior_data = {
        "student_id": student_id,
        "behavior_type": "attention",
        "timestamp": datetime.now().isoformat(),
        "duration": 30.5,
        "details": {"location": "home", "activity": "homework"}
    }
    response = client.post(
        "/api/v1/student-data/behaviors/",
        json=behavior_data,
        headers=headers
    )
    assert response.status_code == 200

    # 测试获取学生统计数据
    response = client.get(f"/api/v1/student-data/statistics/{student_id}", headers=headers)
    assert response.status_code == 200
    stats = response.json()
    assert "behavior_count" in stats
    assert "progress_count" in stats
    assert stats["behavior_count"] >= 2  # 初始化数据中每个学生有2条行为记录


def test_analysis(headers, client):  # 增加client作为参数，接收TestClient实例夹具
    student_id = 3  # student01 的ID

    # 测试行为分析
    response = client.get(f"/api/v1/analysis/behavior/{student_id}", headers=headers)
    assert response.status_code == 200
    behavior_analysis = response.json()
    assert "attention_rate" in behavior_analysis
    assert "participation_rate" in behavior_analysis

    # 测试知识分析
    response = client.get(f"/api/v1/analysis/knowledge/{student_id}", headers=headers)
    assert response.status_code == 200
    knowledge_analysis = response.json()
    assert isinstance(knowledge_analysis, list)
    assert len(knowledge_analysis) > 0
    assert "subject" in knowledge_analysis[0]
    assert "average_score" in knowledge_analysis[0]

    # 测试学习报告
    response = client.get(f"/api/v1/analysis/report/{student_id}", headers=headers)
    assert response.status_code == 200
    report = response.json()
    assert "overall_evaluation" in report
    assert "suggestions" in report
    assert isinstance(report["suggestions"], list)


def test_curriculum_data(headers, client):  # 增加client作为参数，接收TestClient实例夹具
    # 测试获取所有学科
    response = client.get("/api/v1/curriculum/subjects", headers=headers)
    assert response.status_code == 200
    subjects = response.json()
    assert len(subjects) >= 3  # 初始化数据中有3个学科

    # 测试获取特定学科的章节
    subject_id = 1  # 数学的ID
    response = client.get(f"/api/v1/curriculum/subjects/{subject_id}/chapters", headers=headers)
    assert response.status_code == 200
    chapters = response.json()
    assert len(chapters) >= 2  # 每个学科有2个章节