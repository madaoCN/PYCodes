#coding=utf8
# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://')
DBSession = sessionmaker(engine)
session = DBSession()

# print(session.execute("show databases").fetchall())

# print(session.execute("show tables").fetchall())

# 创建对象的基类:
Base = declarative_base()

class School(Base):
    # 表的名字:
    __tablename__ = 'school'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

def create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def insert_sh():
    #创建新User对象:
    new_user = School(id='5', name='Bob')

    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

def del_sh():
    result = session.query(School).filter(School.id > 0).delete()
    # for item in result.values():
    #     print(item)
    session.commit()

def modify():
    # 修改
    result = session.query(School).filter(School.id == "5").update({School.name: "madao"})
    print(result)
    session.commit()

def query():
    # 查询
    # 查第一行
    print(dir(session.query(School)))
    # # 查所有行
    # session.query(School.id, School.userName, School.password).all()
    # # 根据id倒序并取前两行
    # session.query(School).order_by(School.id.desc()).limit(2)


if __name__ == '__main__':
    query()
    pass

