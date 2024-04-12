from django.urls import path
from . import views

urlpatterns = [
    
    path('' ,views.signup_page,name = 'register'),
    path('login/',views.login_page,name ='log'),
    path('create/',views.create ,name = 'create'),
    path('data/',views.data ,name = 'data'),
    path('update/<int:id>/',views.update ,name = 'update'),
    path('delete/<int:pk>/',views.delete ,name = 'delete'),
    path('search/',views.search_view ,name ='search'),
    path('logout/', views.logout_view, name='logout'),
]
