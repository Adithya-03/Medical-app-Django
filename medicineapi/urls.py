from django.urls import path
from . import views
from .views import SearchAPIView

urlpatterns = [
    path('signupapi',views.signupapi,name='signup_api'),
    path('loginapi/', views.loginapi, name='login_api'),
    path('create_product', views.create_product, name='createproductapi'),
    path('list_products', views.list_products, name='retrieveproductapi'),
    path('<int:pk>/update_product', views.update_product, name='updateproductapi'),
    path('<int:pk>/delete_product', views.delete_product, name='deleteproductapi'),
    # path('search', views.search_product, name='searchproductapi'),
    # path('questions/',views.QuestionsAPIView.as_view(), name='questions_api')
    path('api/search/', SearchAPIView.as_view(), name='search_api')

]