from django.urls import path,include
from .views import  TodoDetail, TodoGetUpdDelGen, TodoListCreate, TodoListCreateGen, todo_detail,home, todoListCreate, TodoList,TodoModelView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('todo',TodoModelView)

urlpatterns = [
  path('',home),
  #path('todolist/',todoList),
  path('todocreate/',todoListCreate),
  path('todocreateC/',TodoList.as_view()),
  path('todocreateCG/',TodoListCreate.as_view()),
  path('todocreateGen/',TodoListCreateGen.as_view()),
  #path('todos/',todoListCreate),
  path('todos/<int:pk>',todo_detail),
  path('todosC/<int:pk>',TodoDetail.as_view()),
  path('todosGen/<int:pk>',TodoGetUpdDelGen.as_view()),
  #path('todoupdate/<int:pk>',todo_update),
  #path('tododelete/<int:pk>',todo_delete),
  path('',include(router.urls))
  
]
