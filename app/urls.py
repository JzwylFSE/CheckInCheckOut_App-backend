from django.urls import path
from .views import UserView, ActivityView, ApiRootView
from . import views

urlpatterns = [
    # Home and database pages
    path('', views.home, name='home'),
    path('database/', views.database_view, name='database_view'),
    
    # Api-root
    path('api/', ApiRootView.as_view(), name='api-root'),
    path('api/users/', UserView.as_view(), name='users'),
    path('api/activities/', ActivityView.as_view(), name='activities'),

    # API Endpoints for Users
    path('api/users/', views.UserView.as_view(), name='user-list'),  # User list (GET) & create (POST)
    path('api/users/<int:user_id>/', views.UserView.as_view(), name='user-detail'),  # User detail (GET, DELETE)
    
    # Check-in and check-out for users
    path('api/check-in/', views.ActivityView.as_view(), name='check-in'),
    path('api/check-out/<int:user_id>/', views.ActivityView.as_view(), name='check-out'),
    
    # delete a user
    path('api/users/<int:user_id>/', UserView.as_view(), name='delete'),
    
    #get specific user's activity detail
    path('api/activities/<int:user_id>/', ActivityView.as_view(), name='user-activity-detail'),
 
    # Retrieve activity status of all users
    path('api/status/', views.ActivityView.as_view(), name='check-status'),  # Get activity status (GET)
]
