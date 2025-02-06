from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.Login.as_view(),name ="login"),
    path('register.html/',views.Register.as_view(),name ="register"),
    path('logout/',views.logout_user,name ="logout"),
    path('post_login_options/', views.PostLoginOptions.as_view(), name='post_login_options'),
    path('profile/', views.profile, name="profile"), 
    path('admin_panel/', views.AdminPanel.as_view(), name="admin_panel"),
]