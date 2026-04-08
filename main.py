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

@app.get("/news/{id}")
async def get_id(id:int=Path(...,gt=0,lt=101)):
	return{"msg":f"这是第{id}篇新闻"}

@app.get("/news/{name}")
async def get_name(name:str=Path(...,min_length=2,max_length=10)):
	return{"msg":f"这篇新闻的题目是{name}"}

#需求 查询参数 ->分页，skip：跳过的记录数，limit：返回的记录数 10
@app.get("/news/news_list")
async def get_news_list(
	skip:int=Query(0,description="跳过的记录数",lt=100),
	limit:int=Query(10,description="返回的记录数")
):
	return{"skip":skip,"limit":limit}