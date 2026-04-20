from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.sql import func

app = FastAPI() #创建一个FastAPI应用，给他起名叫app

# 1.创建异步引擎 
ASYNC_DATABASE_URL = "mysql+aiomysql://root:Wanghe1234_@localhost:3306/fastapi_test?charset=utf8"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,
    pool_size = 10,
    max_overflow = 20
)

# 2.定义模型类: 基类 + 表对应的模型类
# 基类：创建时间、更新时间
# 用户表：用户id、用户名、密码
class Base(DeclarativeBase):
    create_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="更新时间")

class User(Base):
    __tablename__="user" 
    id:Mapped[int] = mapped_column(primary_key=True,comment="用户id")
    username:Mapped[str] = mapped_column(String(255),comment="用户名")
    password:Mapped[str] = mapped_column(String(255),comment="密码")

# 3。建表：定义函数建表 ->FastAPI 启动时调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事物 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) #Base 模型类的元数据创建

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)