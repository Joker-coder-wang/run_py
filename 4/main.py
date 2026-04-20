from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

app=FastAPI()

# 1.创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:Wanghe1234_@localhost:3306/fastapi_test?charset=utf8"

async_engine = create_async_engine (
    ASYNC_DATABASE_URL,
    echo = True, # 可选 输出sql日志
    pool_size = 10, # 设置连接池中保持的持久连接数
    max_overflow = 20 # 设置连接池中允许创建的额外连接数
)

# 2.定义模型类：基类 + 表对应的模型类
# 基类：创建时间、更新时间；
# 书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    create_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now,comment="创建时间")

class Book(Base):
    __tablename__ = "book" # 给表 对应的模型类起个名字

    id:Mapped[int] = mapped_column(primary_key=True,comment="书籍id")
    bookname:Mapped[str] = mapped_column(String(255),comment="书名")
    auto:Mapped[str] = mapped_column(String(10),comment="作者")
    price:Mapped[float] = mapped_column(Float,comment="价格")
    publisher:Mapped[str] = mapped_column(String(255),comment="出版社")

# 3.建表：定义函数建表 -> FastAPI 启动时调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事物 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # Base 模型类的元数据创建

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)