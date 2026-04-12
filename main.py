from tokenize import Double

from fastapi import FastAPI,Path,Query
#创建 FastAPI实例
app = FastAPI()

@app.get("/")
def read_root():
	return {"message":"Hello World"}

@app.get("/hello/{name}")
async def say_hello(name:str):
	return {"message":f"Hello {name}"}

#访问 /hello 响应结果 msg：你好 FastAPI
@app.get("/hello")
async def get_hello():
	return {"msg":"你好 FastAPI"}

#访问 /user/hello 响应结果 msg:我正在学习FastAPI…
@app.get("/user/hello")
async def get_me():
	return{"msg":"我正在学FastAPI…"}

@app.get("/book/{id}")
async def get_book(id:int = Path(...,gt=0,lt=101,description="书籍id，取值范围在1-100")):
	return{"msg":f"这是第{id}本书"}

@app.get("/author/{name}")
async def get_name(name:str=Path(...,min_length=2,max_length=10)):
	return{"msg":f"这是{name}的信息"}

# @app.get("/news/{id}")
# async def get_id(id:int=Path(...,gt=0,lt=101)):
# 	return{"msg":f"这是第{id}篇新闻"}

# @app.get("/news/{name}")
# async def get_name(name:str=Path(...,min_length=2,max_length=10)):
# 	return{"msg":f"这篇新闻的题目是{name}"}

#需求 查询参数 ->分页，skip：跳过的记录数，limit：返回的记录数 10
# @app.get("/news/news_list")
# async def get_news_list(
# 	skip:int=Query(0,description="跳过的记录数",lt=100),
# 	limit:int=Query(10,description="返回的记录数")
# ):
# 	return{"skip":skip,"limit":limit}

#需求 设计接口查询图书，要求携带两个查询参数：图书分类和价格
@app.get("/book/")
async def get_book(
	type:str=Query("Python开发",min_length=5,max_length=255),
	price:int=Query(...,gt=50,lt=100)
):
	return{"type":type,"price":price}

#导入类
from pydantic import BaseModel,Field

#注册：用户名和密码 ->str 
class User(BaseModel):
	username:str=Field(default="张三",min_length=2,max_length=5,discription="用户名，长度要求2-5个字")
	password:str=Field(min_length=6,max_length=16,description="请设置密码，长度要求在6-16字符")

@app.post("/register")
async def register(user:User):
	return user

#需求：设计接口新增图书，图书信息包含：书名、作者、出版社、售价
class Book(BaseModel):
	title:str=Field(min_length=1,max_length=15)
	autor:str=Field(min_length=2,max_length=10)
	publisher:str=Field(default="人民出版社")
	price:float=Field(gt=0)

@app.post("/books")
async def add_book(book:Book):
	return {"msg":"图书添加成功","book":book}

#导入类
from fastapi.responses import HTMLResponse
# 需求：接口-> 响应HTML 代码
@app.get("/html",response_class=HTMLResponse)
async def get_html():
	return "<h1>这是一级标题</h1>"

#导入类
from fastapi.responses import FileResponse
#接口：返回一张图片内容
@app.get("/file")
async def get_file():
	path="./files/1.jpg"
	return FileResponse(path)

#需求：新闻接口-> 响应数据格式 id title content
# class News(BaseModel):
# 	id:int
# 	title:str
# 	content:str
# #导入类：from pydantic import BaseModel,Field->以便约束,必须契合News类里的每一个参数，不然会报错！
# @app.get("/news/{id}",response_model=News)
# async def get_news(id:int):
# 	return {
# 		"id":id,
# 		"title":f"这是第{id}本书",
# 		"content":"这是一本好书"
# 	}

#导入类
from fastapi import FastAPI,HTTPException

#需求：按id 查询新闻 -> 1-6
@app.get("/news/{id}")
async def get_news_id(id:int):
	id_list = [1,2,3,4,5,6]
	if id not in id_list:
		raise HTTPException(status_code=404,detail="您查找的新闻不存在！")
	return {"id":id}