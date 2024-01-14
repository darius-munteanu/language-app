from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login_view"),
    path("logout",views.logout_view,name="logout_view"),
    path("main",views.main,name="main"),
    path("update_count",views.update_count,name="update_count"),
    path("chat_thing",views.chat_thing,name="chat_thing"),
    path("microphone_input",views.microphone_input,name="microphone_input"),
    path("submit",views.submit,name="submit")
]
