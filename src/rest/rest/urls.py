"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import TodoListView

urlpatterns = [
    # Both spellings point to the same view. The frontend posts to `/todos`
    # without a slash; if we only had `todos/`, Django would 301 the POST and
    # the body would be lost on the redirect.
    path('todos', TodoListView.as_view(), name='todos'),
    path('todos/', TodoListView.as_view(), name='todos-slash'),
]
