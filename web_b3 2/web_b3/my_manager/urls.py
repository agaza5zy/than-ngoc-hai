from django.contrib import admin
from django.urls import path
from courses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Các chức năng cũ
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # THÊM 2 ĐƯỜNG DẪN CHO CHATBOT
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chat-api/', views.chat_api, name='chat_api'),
]