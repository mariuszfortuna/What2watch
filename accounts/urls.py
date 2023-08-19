from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('userList/', views.UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),

]