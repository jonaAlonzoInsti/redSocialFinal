from social.forms import SocialCommentForm,ShareForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from .models import SocialPost, SocialComment,Image,User
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
#para hacer busquedas en la base de datos
from django.db.models import Q
#para hacer busquedas en la base de datos
from accounts.models import Profile

#vista imagen o peta
class Image(View):
    def get(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        images = post.image.all()

        context = {
            'images':images,
        }
        return render(request, 'pages/social/images.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        images = post.image.all()

        context = {
            'images':images,
        }
        return render(request, 'pages/social/images.html', context)

#Vista del post
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        #form para los comentarios
        form = SocialCommentForm()

        comments = SocialComment.objects.filter(post=post).order_by('-created_on')
        context= {
            'post':post,
            'form': form,
            'comments':comments,
        }
        return render(request, 'pages/social/detail.html', context)
        #kwargs es un diccionario que contiene los valores de los argumentos pasados a la vista. los elementos que tiene un objeto que son los post que se han creado 
    def post(self, request, pk,*args, **kwargs):
        post = SocialPost.objects.get(pk=pk)
        #form para los comentarios
        form = SocialCommentForm(request.POST)
        comments = SocialComment.objects.filter(post=post).order_by('-created_on')
        #si el formulario es valido
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        

        context = {
            'post': post,
            #form para los comentarios
            'form': form,
            #cargamos los comentarios
            'comments':comments
        }

        return render(request, 'pages/social/detail.html', context)

#vista para editar un post
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    
    model=SocialPost
    fields=['body']
    template_name='pages/social/edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

#vista para eliminar un post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=SocialPost
    template_name='pages/social/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
      
#vista like
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_dislike = False
        #si el usuario ya ha dado dislike, se elimina el dislike
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        #si el usuario ya ha dado like, se elimina el like             
        if is_dislike:
            post.dislikes.remove(request.user)
        #se verifica si el usuario ya ha dado like
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        #si no ha dado like, se agrega el like
        if not is_like:
            post.likes.add(request.user)
        #si ya ha dado like, se elimina el like
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#vista dislike
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = SocialPost.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#vista para agregar LIKE a un comentario
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#vista para agregar DISLIKE a un comentario
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = SocialComment.objects.get(pk=pk)

        is_like = False
        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        
#vista para comentar un comentario
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post=SocialPost.objects.get(pk=post_pk)
        parent_comment = SocialComment.objects.get(pk=pk)
        form=SocialCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('social:post-detail', pk=post_pk)

#vista para eliminar un comentario
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=SocialComment
    template_name="pages/social/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

#vista para editar un comentario
class CommentEditView(UpdateView):
    model = SocialComment
    fields = ['comment']
    template_name = 'pages/social/comment_edit.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('social:post-detail', kwargs={'pk':pk})


  #compartir post  

#vista para compartir un post
class SharedPostView(View):
    def post(self, request, pk, *args, **kwargs):
        original_post = SocialPost.objects.get(pk=pk)
        form = ShareForm(request.POST)

        if form.is_valid():
            new_post = SocialPost(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

        return redirect('home')
    
#vista para buscar usuarios    
class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        #filtramos los usuarios que se muestran en la busqueda
        profile_list = Profile.objects.filter(Q(user__username__icontains=query))
        #filtramos los post que se muestran en la busqueda
        post_list = SocialPost.objects.filter(Q(body__icontains=query)).order_by('-created_on')
        #imagen usuario
       
        context = {
            'profile_list':profile_list,
            'post_list':post_list,

        }
        return render(request, 'pages/social/search.html', context)
    


#vista para ver imagenes de un usuario
class SocialPostsWithImagesView(View):
    def get(self, request, *args, **kwargs):
        # Filtrar los SocialPost que tengan al menos una imagen asociada
        posts_with_images = SocialPost.objects.filter(images__isnull=False).distinct()

        context = {
            'posts_with_images': posts_with_images,
        }
        return render(request, 'pages/social/posts_with_images.html', context)