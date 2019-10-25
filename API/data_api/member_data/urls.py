from django.urls import path
from .views import *

urlpatterns = [
    path('list_members', MembersListView.as_view(), name='all-members'),
    path('get_member/<slug:MemberID>', MemberView.as_view(), name='get-a-member'),
    path('set_member/<slug:MemberID>', MemberView.as_view(), name='set-a-member'),
    path('create_member', MemberView.as_view(), name='create-a-member'),
]