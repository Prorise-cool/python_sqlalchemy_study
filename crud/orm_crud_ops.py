# sqlalchemy_orm_practice/crud/orm_crud_ops.py
"""
SQLAlchemy ORM CRUD 操作模块

此模块演示了 SQLAlchemy ORM 的基本 CRUD（创建、读取、更新、删除）操作。

主要功能:
- 创建: 创建新的类别和产品记录
- 读取: 按 ID、条件筛选和排序查询记录
- 更新: 更新现有记录的属性
- 删除: 从数据库中删除记录
"""
from sqlalchemy import select, update, delete, func  # 导入 SQL 语句构造模块
from sqlalchemy.exc import SQLAlchemyError  # 导入 SQLAlchemy 异常处理模块
from sqlalchemy.orm import Session  # 导入 ORM 会话模块
from core_config import SessionLocal  # 导入 ORM 会话工厂
from models.orm_models import CategoryORM, ProductORM  # 导入 ORM 模型定义
from utils.print_utils import print_header, print_subheader, print_info, print_success, print_error, print_sql, \
    print_warning, \
    print_result_item
from typing import Optional


class OrmCrudOps:
    """封装 ORM  CRUD 示例的类"""

    def __init__(self, session: Session):
        """依赖注入 Session 对象"""
        self.session = session
        self.last_category_id: Optional[int] = None  # 记录最后一个插入的类别 ID
        self.last_product_id: Optional[int] = None  # 记录最后一个插入的产品 ID

    ###### 创建对象 (INSERT) ######
    def create_objects(self) -> tuple[Optional[int], Optional[int]]:
        """创建Category和Product对象并插入到数据库中"""
        print_subheader("1. 创建 ORM 对象 (INSERT)")
        try:
            with self.session.begin_nested():  # 开启事务
                # 创建 Category 对象
                category = CategoryORM(name="书籍类", description="书籍类产品...包含各类图书")
                self.session.add(category)  # 将 Category 对象添加到会话中
                self.session.flush()  # 刷新会话，以便获取新插入对象的 ID
                self.last_category_id = category.id  # 记录最后一个插入的类别 ID

                # 创建 Product 并关联
                product = ProductORM(name="Python 编程指南", price=39.99, category_id=category.id)
                self.session.add(product)  # 将 Product 对象添加到会话中
                self.session.flush()  # 刷新会话，以便获取新插入对象的 ID
                self.last_product_id = product.id  # 记录最后一个插入的产品 ID
            print_success("创建 ORM 对象成功。")
            return self.last_category_id, self.last_product_id
        except SQLAlchemyError as e:
            print_error(f"创建 ORM 对象失败: {e}")
            return None, None

    ##### 查询对象 (SELECT) #####
    def query_object(self):
        print_subheader("2. 查询 ORM 对象 (SELECT)")
        try:
            # 按 主键查询（session.get）
            print_info(f"\n使用 session.get() 查询 Category ID={self.last_category_id}:")
            category = self.session.get(CategoryORM, self.last_category_id)
            if category:
                print_success(f"查询结果: {category}")
            else:
                print_warning(f"查询结果: 未找到 ID={self.last_category_id} 的 Category 对象。")

            # 条件查询(获取第一个)
            print_info("\n条件查询 Product (name like '%Python%'):")
            stmt_find = select(ProductORM).where(ProductORM.name.like("%Python%")).limit(1)
            product = self.session.execute(stmt_find).scalars().first()
            if product:
                print_success(f"查询结果: {product}")
            else:
                print_warning("查询结果: 未找到符合条件的 Product 对象。")

        except SQLAlchemyError as e:
            print_error(f"查询失败: {e}")

    ##### 更新对象 (UPDATE) #####
    def update_object(self):
        print_subheader("3. 更新 ORM 对象 (UPDATE)")
        try:
            with self.session.begin_nested():  # 开启事务
                # 方法一: 修改对象属性
                print_info(f"\n修改 Product ID={self.last_product_id}的价格")
                product_to_update = self.session.get(ProductORM,self.last_product_id)
                if product_to_update:
                    product_to_update.price = 88.88 # 直接修改属性
                else:print_warning(f"查询结果: 未找到 ID={self.last_product_id} 的 Product 对象。")

                # 方法二： ORM 级 UPDATE语句 (批量)
                print_info("\n批量降低 '书籍类' 的库存")
                stmt_bulk_update = update(ProductORM).where(
                    ProductORM.category.has(CategoryORM.name == "书籍类")
                ).values(
                    stock = ProductORM.stock - 5 # 批量修改库存
                ).execution_options(synchronize_session="fetch") # 重要: 更新后刷新 session 中的对象
                # synchronize_session='fetch'/'evaluate'/False
                # 'fetch': 执行 UPDATE 后，SELECT 受影响行以更新 Session (最安全但可能慢)
                # 'evaluate': 尝试在 Python 中评估更新效果 (快，但可能不精确)
                # False: 不更新 Session 中的对象状态 (最快，但 Session 可能与 DB 不一致)
                result = self.session.execute(stmt_bulk_update)
                print_success(f"受影响的行数: {result.rowcount}")
            print_success("更新操作已暂存 (待外层 Commit)。")
        except SQLAlchemyError as e:print_error(f"更新失败: {e}")


    ###### 删除对象 (DELETE) ######
    def delete_objects(self):
        print_subheader("4. 删除 ORM 对象 (DELETE)")
        try:
            with self.session.begin_nested(): # 事务
                # 方法一: 删除单个对象
                print_info(f"\n删除 Product ID={self.last_product_id}:")
                product_to_del = self.session.get(ProductORM, self.last_product_id)
                if product_to_del:
                    self.session.delete(product_to_del) # 标记删除
                    print_success(f"  ID={self.last_product_id} 已标记删除。")
                else: print_warning(f"  未找到 ID={self.last_product_id}。")

                # 方法二: ORM 级 DELETE 语句 (批量)
                print_info("\n批量删除类别为 NULL 的产品:")
                stmt_bulk_del = delete(ProductORM).where(ProductORM.category_id == None)
                result = self.session.execute(stmt_bulk_del)
                print_success(f"  批量删除影响了 {result.rowcount} 行。")
            print_success("  删除操作已暂存 (待外层 Commit)。")
        except Exception as e:
            print_error(f"删除对象时出错: {e}")
            raise


# --- 在 main_orm_runner.py 中如何使用 ---
# with SessionLocal() as main_session:
#     crud_executor = OrmCrudOps(main_session)
#     try:
#         crud_executor.create_objects()
#         crud_executor.query_objects()
#         crud_executor.update_objects()
#         # crud_executor.delete_objects() # 决定是否执行删除
#         main_session.commit() # 提交所有操作
#         print_success("\n主事务已提交！")
#     except Exception as main_err:
#         print_error(f"\n主流程出错: {main_err}")
#         main_session.rollback()
#         print_info("主事务已回滚。")