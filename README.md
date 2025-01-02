# 多模态教育教学辅助系统

## 项目概述

这是一个基于人工智能的教育教学辅助系统，通过多模态数据采集和分析，为教师和学生提供智能化的教学支持服务。

## 技术栈

### 前端

- Next.js 14 (React框架)
- TypeScript
- Tailwind CSS
- Ant Design
- ECharts (数据可视化)
- i18next (国际化)

### 后端

- Python 3.10+
- FastAPI (Web框架)
- SQLAlchemy (ORM)
- PostgreSQL (关系型数据库)
- Milvus (向量数据库)
- OpenAI API (大模型服务)
- YOLOv8 (目标检测)
- Whisper (语音识别)
- PaddleOCR (文字识别)

## 项目结构

```
project/
├── frontend/ # 前端项目目录
│ ├── src/
│ │ ├── app/ # 页面组件
│ │ ├── components/ # 通用组件
│ │ ├── hooks/ # 自定义Hook
│ │ ├── styles/ # 样式文件
│ │ ├── types/ # 类型定义
│ │ └── utils/ # 工具函数
│ ├── public/ # 静态资源
│ └── package.json
│
├── backend/ # 后端项目目录
│ ├── app/
│ │ ├── api/ # API路由
│ │ ├── core/ # 核心功能
│ │ ├── models/ # 数据模型
│ │ ├── services/ # 业务逻辑
│ │ └── utils/ # 工具函数
│ ├── tests/ # 测试文件
│ └── requirements.txt
│
└── docker/ # Docker配置文件
```

## 核心功能模块

### 1. 用户认证模块

- 学生登录/注册
- 教师登录/注册
- 管理员登录
- JWT认证
- 权限管理

### 2. 数据采集模块

- 视频行为识别
- 语音对话记录
- 作业批改记录
- OCR文字识别

### 3. 数据分析模块

- 学生行为分析
- 知识点掌握度分析
- 学习进度追踪
- 个性化报告生成

### 4. 可视化展示模块

- 数据大盘展示
- 个人学习报告
- 班级整体分析
- 知识点难度分析

## 开发环境搭建

### 前端开发环境

```bash
cd frontend
npm install
npm run dev
```

### 后端开发环境

```bash
cd backend
python -m venv venv
source venv/bin/activate # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API文档

API文档访问地址：http://localhost:8000/docs

## 部署说明

1. 使用Docker Compose进行容器化部署
2. 支持Nginx反向代理
3. SSL证书配置
4. 数据库备份策略

## 开发规范

1. 代码规范遵循各语言官方推荐的规范
2. Git提交信息规范
3. 测试覆盖率要求
4. 文档编写要求

## 贡献指南

1. Fork本仓库
2. 创建特性分支
3. 提交变更
4. 发起Pull Request

## 版本历史

- v0.1.0 项目初始化

## 许可证

MIT License
