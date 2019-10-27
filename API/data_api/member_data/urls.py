from django.urls import path
from .views import *

urlpatterns = [
    path('list_members', MembersListView.as_view(), name='all-members'),
    path('get_member/<slug:MemberID>', MemberView.as_view(), name='get-member'),
    path('set_member/<slug:MemberID>', MemberView.as_view(), name='set-member'),
    path('create_member', MemberView.as_view(), name='create-member'),
    path('create_episode', AddEpisode.as_view(), name='create-episode'),
    path('create_encounter', AddEncounter.as_view(), name='create-encounter'),
]