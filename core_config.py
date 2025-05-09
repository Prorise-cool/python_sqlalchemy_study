"""
SQLAlchemy ORM 核心配置模块

此模块包含数据库连接引擎和会话的配置。
提供了创建数据库引擎和会话工厂的功能，用于整个应用程序的数据库交互。

主要组件:
- engine: 数据库连接引擎
- SessionLocal: 本地会话工厂，用于创建数据库会话
"""
from sqlalchemy import create_engine  # 数据库引擎
from sqlalchemy.orm import sessionmaker  # 会话工厂
from utils.print_utils import print_info, print_success, print_error  # 打印工具

# --- 数据库连接配置 (使用 PyMySQL) ---
# !!! 生产环境应使用更安全的方式管理密码 !!!
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "sqlalchemy_orm_db"  # 确保此数据库已创建
DB_CHARSET = "utf8mb4"
ORM_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
print_info(f"ORM 数据库连接 URL: {ORM_DATABASE_URL.replace(DB_PASSWORD, '******')}")  # 打印时隐藏密码

# --- 创建 Engine(针对 ORM) ---
orm_engine = create_engine(
    ORM_DATABASE_URL,
    echo=True,  # 打印 SQL 语句
    future=True,  # 启用 SQLAlchemy 2.0 新特性
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接池溢出时最多创建的连接数
    pool_recycle=3600,  # 连接池中连接的最大空闲时间，超过此时间的连接会被自动关闭
)
print_success("ORM 数据库引擎创建成功")

# --- 创建 SessionLocal 工厂 ---
SessionLocal = sessionmaker(
    autocommit=False,  # 自动提交
    autoflush=False,  # 推荐 - 关闭自动刷新
    bind=orm_engine,  # 绑定引擎
    expire_on_commit=True  # 会话在提交后过期
)
print_success("ORM 会话工厂创建成功")

# 使用示例 (通常在其他模块中):
# with SessionLocal() as session:
#     # ... use session ...
#     session.commit() # or session.rollback()
