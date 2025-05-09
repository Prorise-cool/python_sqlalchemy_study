# sqlalchemy_orm_practice/models/base.py
"""
SQLAlchemy ORM 基础模型模块

此模块定义了应用程序中所有 ORM 模型的基类和 Mixin 类。

主要组件:
- DeclarativeBase: 所有 ORM 模型的基类
- 各种可复用的 Mixin 类，如 TimestampMixin（提供时间戳功能）
"""
# -----Mapped 与 mapped_column 是做什么用的？ ----------
# Mapped[<type>] (例如 Mapped[int], Mapped[Optional[datetime]]):
# 类型注解工具：这是 SQLAlchemy 2.0 引入的，主要用于类型提示。它告诉开发者和其他工具（如静态类型检查器 Mypy）这个类属性是一个被 ORM 映射的字段，并且它在 Python 代码中的期望类型是什么。
# 提高可读性：让模型定义更清晰易懂。

# mapped_column(...) (例如 mapped_column(Integer, primary_key=True)):
# 列定义函数：这是实际用来定义数据库列属性的函数。
# 您可以在这里指定该列在数据库中的具体 SQL 类型（如 Integer, String(50), TIMESTAMP）、是否为主键 (primary_key=True)、
# 是否允许为空 (nullable=False)、默认值 (default=... 或 server_default=func.now())、索引、外键 (ForeignKey(...))、注释等。
# 它是 SQLAlchemy 2.0 中声明模型列的首选方式，用于替代旧版本中直接使用 Column(...) 的方式。

from sqlalchemy import Integer, DateTime, Boolean, TIMESTAMP, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from utils.print_utils import print_success


# --- 定义 Declarative Base ---
# DeclarativeBase 继承后会得到什么？
# 1.声明式能力：继承 DeclarativeBase 后，基类就获得了将 Python 类定义直接映射到数据库表的能力
# 2.metadata 属性：这个 Base 类会自动拥有一个名为 metadata 的 MetaData 对象。所有继承自 Base 的模型类，其表结构信息都会自动注册到这个 Base.metadata 中。
# DDL 操作基础：使得后续可以通过 Base.metadata.create_all(engine) 来自动创建所有定义的数据库表。
class Base(DeclarativeBase):
    """所有ORM 模型的基类"""
    # 可选：可以定义一个 MetaData 对象来控制 ORM 行为
    # metadata = MetaData()
    pass


# --- 定义 Mixin (用于共享字段逻辑) ---
class TimestampMixin:
    """提供时间戳功能的 Mixin 类"""
    # 使用 server_default 和 onupdate 选项，可以 利用数据库能力自动管理时间戳
    create_time: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )


# --- 定义抽象基类 (可选，用于共享 ID 等基础字段) ---
class AbstractBaseModel(Base):
    """包含 通用 ID 和 逻辑删除标记的抽象基类"""
    __abstract__ = True  # 不会创建对应的表
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="主键ID"
    )
    # Mysql 中 常用 TINYINT(1) 来存储布尔值，sqlalchemy 中可以用 Boolean 类型 他会自动映射为 TINYINT(1)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default="0", index=True, comment="逻辑删除标记")
print_success("ORM Base, Mixin, AbstractBaseModel 已定义 (models/base.py)。")