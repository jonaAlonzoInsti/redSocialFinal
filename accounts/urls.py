from django.urls import path

from .views import UserProfileView, EditProfile,AddFollower, RemoveFollower, ListFollowersView, UserPhotosView

app_name="accounts"

urlpatterns = [
    #editar user, ver user
    path('<username>/', UserProfileView.as_view(), name="profile"),
    path('profile/edit', EditProfile, name="edit-profile"),

    #followers
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
	path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),

    #list followers
    path('profile/<int:pk>/followers/', ListFollowersView.as_view(), name='followers-list'),

    #user photos
        path('profile/<int:pk>/photos/', UserPhotosView.as_view(), name='user-photos'),



]
