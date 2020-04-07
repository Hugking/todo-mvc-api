"""
    a standard CRUD template of todoList
    通过 事件 来实现一套标准的 CRUD 功能，供学习
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.todoList import TodoList
from app.validators.forms import TodoListSearchForm, CreateOrUpdateTodoListForm

todoList_api = Redprint('todoList')


# 这与真实的情况是一致的，因为一般的情况下，重要的接口需要被保护，重要的消息才需要推送
@todoList_api.route('/<bid>', methods=['GET'])
def get_todoList(bid):
    todoList = TodoList.get_detail(bid)
    return jsonify(todoList)


@todoList_api.route('', methods=['GET'])
def get_todoLists():
    todoLists = TodoList.get_all()
    return jsonify(todoLists)


@todoList_api.route('/search', methods=['GET'])
def search():
    form = TodoListSearchForm().validate_for_api()
    todoLists = TodoList.search_by_keywords(form.q.data)
    return jsonify(todoLists)


@todoList_api.route('', methods=['POST'])
def create_todoList():
    form = CreateOrUpdateTodoListForm().validate_for_api()
    TodoList.new_todoList(form)
    return Success(msg='新建事件成功')


@todoList_api.route('/<bid>', methods=['PUT'])
def update_todoList(bid):
    form = CreateOrUpdateTodoListForm().validate_for_api()
    TodoList.edit_todoList(bid, form)
    return Success(msg='更新事件成功')


@todoList_api.route('/<bid>', methods=['DELETE'])
def delete_todoList(bid):
    TodoList.remove_todoList(bid)
    return Success(msg='删除事件成功')
