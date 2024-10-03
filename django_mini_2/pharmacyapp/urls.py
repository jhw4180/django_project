from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import create_review, create_score, dashboard, signup_view
from .views import review_list_view, board_detail_view, BoardUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('review_create/<int:pharmacy_id>/', create_review, name='review_create'),
    path('score/delete/<int:score_id>/', views.delete_score, name='delete_score'),
    path('review_update/<int:pharmacy_id>/', BoardUpdateView.as_view(), name='review_update'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reviews/', review_list_view, name='review_list'),
    path('nearby/', views.nearby_pharmacies, name='nearby_pharmacies'),
    path('pharmacy/<int:pharmacy_id>/', views.pharmacy_detail, name='pharmacy_detail'),
    path('pharmacy/<int:pharmacy_id>/score/', views.create_score, name='create_score'),
    path('pharmacy-list/', views.pharmacy_list, name='pharmacy_list'),
]