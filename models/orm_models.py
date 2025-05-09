# sqlalchemy_orm_practice/models/orm_models.py
"""
SQLAlchemy ORM 模型定义模块

此模块包含具体的 ORM 模型类定义，用于映射到数据库表。

主要模型:
- CategoryORM: 映射到 categories 表的分类模型
- ProductORM: 映射到 products 表的产品模型，与 CategoryORM 有关联关系
"""
from sqlalchemy import String, Integer, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship  # 导入 relationship
from typing import Optional, List
from .base import AbstractBaseModel, TimestampMixin, Base  # 从同目录的 base.py 导入
from utils.print_utils import print_success  # 绝对导入

# --- 定义具体模型 ---
class CategoryORM(AbstractBaseModel, TimestampMixin):  # 继承 AbstractBaseModel 和 TimestampMixin
    """产品类型 ORM 模型"""
    __tablename__ = "categories_orm"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, unique=True, comment="类别名称"
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="类别描述"
    )

    # --- 添加关系 (见下一节) ---
    products: Mapped[List["ProductORM"]] = relationship(
        "ProductORM",  # 目标模型类名
        back_populates="category",  # 指向 ProductORM 类的 category 属性
        cascade="all, delete-orphan",  # 级联操作: 删除 CategoryORM 时同时删除关联的 ProductORM
        lazy="selectin"  # 延迟加载，仅在需要时才加载数据
    )

    def __repr__(self):
        """打印对象信息"""
        return f"<CategoryORM(id={self.id}, name='{self.name}')>"


class ProductORM(AbstractBaseModel, TimestampMixin):
    """产品 ORM 模型"""
    __tablename__ = "products_orm"

    name: Mapped[str] = mapped_column(
        String(100), index=True, comment="产品名称",
    )
    # 使用 Mapped[float] 作为 Python 类型提示，数据库类型由 Numeric 指定
    price: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=False, comment="产品价格"
    )
    # default 和 server_default 用于设置默认值，server_default 用于设置数据库默认值
    stock: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False, comment="库存数量"
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="1", nullable=False, comment="是否上架"
    )

    # --- 外键定义 ---
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("categories_orm.id", ondelete="SET NULL"),  # 关联 categories_orm 表的 id 列，删除时设置为 NULL
        nullable=True, index=True, comment="类别所属ID"
    )

    # --- 添加关系 ---
    category: Mapped[Optional["CategoryORM"]] = relationship(
        "CategoryORM", back_populates="products", lazy="joined"
    )

    def __repr__(self):
        return f"<ProductORM(id={self.id}, name='{self.name}', price={self.price})>"
print_success("具体模型 CategoryORM, ProductORM (含关系占位) 已定义 (models/orm_models.py)。")

# --- 创建表的函数 (通常在应用启动或 main 脚本中调用) ---
# def create_orm_tables(engine):
#     print_info("尝试创建所有 ORM 模型对应的表...")
#     try:
#         Base.metadata.create_all(bind=engine)
#         print_success("ORM 表已创建 (如果尚不存在)。")
#     except Exception as e:
#         print_error(f"创建 ORM 表时出错: {e}")
