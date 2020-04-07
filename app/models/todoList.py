"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, Boolean

from app.libs.error_code import TodoListNotFound


class TodoList(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    isEditing = Column(Boolean, nullable=False, default=False)
    isActive = Column(Boolean, nullable=False, default=False)
    isChecked = Column(Boolean, nullable=False, default=False)
    value = Column(String(1000))

    @classmethod
    def get_detail(cls, bid):
        todoList = cls.query.filter_by(id=bid, delete_time=None).first()
        if todoList is None:
            raise NotFound(msg='没有找到相关列表')
        return todoList

    @classmethod
    def get_all(cls):
        todoList = cls.query.filter_by(delete_time=None).all()
        if not todoList:
            raise NotFound(msg='没有找到相关列表')
        todoList.sort(key=id, reverse=False)
        return todoList

    @classmethod
    def search_by_keywords(cls, q):
        todoList = cls.query.filter(TodoList.title.like('%' + q + '%'),
                                    TodoList.delete_time is None).all()
        if not todoList:
            raise TodoListNotFound()
        return todoList

    @classmethod
    def new_todoList(cls, form):
        todoList = TodoList.query.filter_by(value=form.value.data, delete_time=None).first()
        if todoList is not None:
            raise ParameterException(msg='该事件已存在')

        TodoList.create(
            value=form.value.data,
            isEditing=form.isEditing.data,
            isActive=form.isActive.data,
            isChecked=form.isActive.data,
            commit=True
        )
        return True

    @classmethod
    def edit_todoList(cls, bid, form):
        todoList = TodoList.query.filter_by(id=bid, delete_time=None).first()
        if todoList is None:
            raise NotFound(msg='没有找到相关数据')

        todoList.update(
            id=bid,
            value=form.value.data,
            isEditing=form.isEditing.data,
            isActive=form.isActive.data,
            isChecked=form.isActive.data,
            commit=True
        )
        return True

    @classmethod
    def remove_todoList(cls, bid):
        todoList = cls.query.filter_by(id=bid, delete_time=None).first()
        if todoList is None:
            raise NotFound(msg='没有找到相关数据')
        # 删除图书，软删除
        todoList.delete(commit=True)
        return True
