from django.urls import path
from .views import PostDeleteView, PostDetailView, PostEditView,Image,AddDislike, AddLike, CommentDeleteView, CommentEditView, CommentReplyView, AddCommentDislike, AddCommentLike,SharedPostView, UserSearchView


app_name="social"

urlpatterns = [
    #editar, ver, eliminar post
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name="post-edit"),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name="post-delete"),
    path('post/images/<int:pk>/', Image.as_view(), name="post-images"),

    #likes y dislikes
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),

    #compartir post
    path('post/<int:pk>/share', SharedPostView.as_view(), name='share-post'),

    #comentarios borra y editar
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment-delete"),
    path('post/<int:post_pk>/comment/edit/<int:pk>/', CommentEditView.as_view(), name="comment-edit"),

    #momentarios compartir,  likes y dislikes
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name="comment-like"),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name="comment-dislike"),
    path('post/<int:post_pk>/comment/<int:pk>/reply',CommentReplyView.as_view(), name='comment-reply'),


    #busqueda de usuarios  
    path('search/', UserSearchView.as_view(), name='profile-search'),

    #list followers
   


]