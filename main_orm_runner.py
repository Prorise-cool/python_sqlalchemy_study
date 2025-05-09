"""
SQLAlchemy ORM 主运行脚本

此脚本作为项目的入口点，创建数据库表并运行各个示例模块的功能演示。

主要功能:
- 初始化数据库: 创建所有所需的表
- 运行示例: 按顺序调用各个模块的示例功能
- 演示工作流: 展示完整的 ORM 使用流程和最佳实践
"""

from sqlalchemy import func, inspect
from utils.print_utils import print_header, print_info, print_success, print_error, print_warning
from core_config import SessionLocal, orm_engine
from models.base import Base
from models.orm_models import CategoryORM, ProductORM
from crud.orm_crud_ops import OrmCrudOps

def create_tables():
    """创建数据库表"""
    print_header("创建数据库表")
    try:
        # 创建所有模型对应的表
        Base.metadata.create_all(bind=orm_engine)
        print_success("所有 ORM 表已创建 (如果尚不存在)。")
        
        # 打印创建的表信息
        inspector = inspect(orm_engine)
        tables = inspector.get_table_names()
        print_info(f"数据库中的表: {tables}")
    except Exception as e:
        print_error(f"创建表时出错: {e}")
        raise

def run_crud_examples():
    """运行 CRUD 操作示例"""
    print_header("运行 ORM CRUD 操作示例")
    
    # 使用会话上下文管理器
    with SessionLocal() as session:
        # 创建 CRUD 操作执行器
        crud_executor = OrmCrudOps(session)
        
        try:
            # 1. 创建对象
            category_id, product_id = crud_executor.create_objects()
            if not category_id or not product_id:
                print_warning("创建对象失败，跳过后续操作。")
                return
                
            # 2. 查询对象
            crud_executor.query_object()
            
            # 3. 更新对象
            crud_executor.update_object()
            
            # 4. 删除对象 (可选)
            # 取消注释下一行以执行删除操作
            # crud_executor.delete_objects()
            
            # 提交所有操作
            session.commit()
            print_success("\n所有操作已成功提交！")
            
        except Exception as e:
            print_error(f"\n执行 CRUD 操作时出错: {e}")
            session.rollback()
            print_info("所有操作已回滚。")

if __name__ == "__main__":
    # 创建表结构
    # create_tables()
    
    # 运行 CRUD 示例
    run_crud_examples()
    
    print_header("程序执行完毕")
