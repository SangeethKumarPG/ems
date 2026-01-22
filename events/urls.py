from django.urls import path
from . import views

urlpatterns = [
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:event_id>/book/', views.book_event, name='book_event'),
    path('our-team/', views.our_team, name='our_team'),
    path('our-story/', views.our_story, name='our_story'),
    path('contact/', views.contact, name='contact'),
    path('enquiry/', views.enquiry, name='enquiry'),
]
