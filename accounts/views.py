from accounts.forms import EditProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from accounts.models import Profile,Image
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
User = get_user_model()
from django.template import loader
from django.http import HttpResponse


User = get_user_model()

class UserProfileView(View):
    def get(self, request, username,*args, **kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        #acccedemos por medio del atributo del modelo a los seguidores followers
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False
		
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)


        template = loader.get_template('users/detail.html')
 
        context = {
            'profile':profile,
            'number_of_followers':number_of_followers,
            'is_following': is_following,
      }

        return HttpResponse(template.render(context, request))

    def post(self, request, username,*args, **kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)

        context={
            'user':user,
            'profile':profile
        }

        return render(request, 'users/detail.html', context)


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)

    if request.method == 'POST':
        form=EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')

            profile.picture = form.cleaned_data.get('picture')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.birthday = form.cleaned_data.get('birthday')
            profile.bio = form.cleaned_data.get('bio')

            profile.save()
            user_basic_info.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form=EditProfileForm(instance=profile)

    context={
        'form':form,
    }

    return render(request, 'users/edit.html', context)

#agregar seguidores
class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
          #obtenemos el perfil
		profile = Profile.objects.get(pk=pk)
            #agregamos el seguidor
		profile.followers.add(request.user)
          #mensaje de confirmacion
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Followed'
        )
		return redirect('users:profile', username=request.user.username)


class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
          #
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Unfollowed'
        )
		return redirect('users:profile', username=request.user.username)

#listar seguidores
class ListFollowersView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        #obtenemos el perfil
        profile = Profile.objects.get(pk=pk)
        #obtenemos TODOS los seguidores
        followers = profile.followers.all()
        #contexto a enviar
        context = {
            'profile': profile,
            'followers': followers
        }
        #retornamos la lista de seguidores en nuestro elemento html
        return render(request, 'pages/social/followers_list.html', context)
    
class UserPhotosView(View, LoginRequiredMixin):
    model = Image
    template_name = 'path_to_your_template/user_photos.html'
    context_object_name = 'images'

    def get_queryset(self):
        # Obtenemos el id del usuario desde la URL
        user_id = self.kwargs['pk']
        # Filtramos las imágenes del usuario con ese id
        queryset = Image.objects.filter(user_id=user_id)
        return queryset
    

def user_images(request, user_id):
    user_images = Image.objects.filter(user_id=user_id)
    return render(request, 'imagenesUser.html', {'user_images': user_images})