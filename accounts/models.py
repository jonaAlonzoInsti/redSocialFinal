from django.db import models

# Creamos un perfil extendido del usuario, con los campos basicos como name, email, password, etc
# preguntar a alfonso si esto es lo de la doble tabla extendida
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from PIL import Image
#cuando creamos un usuario queremos que al mismo tiempo se cree un perfil
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
#creamos un directorio para guardar las imagenes de perfil, donde por ,medio del admin podremos verificar cada perfil
#y si el usuario no tiene una imagen de perfil se le asignara una por defecto
#instance hace referencia al usuario que se esta creandom, filename es el nombre de la imagen que se esta subiendo
def user_directory_path_profile(instance, filename):
    #creamos un directorio con el nombre del usuario y la imagen de perfil
    profile_picture_name = 'users/{0}/profile.jpg'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    #si el directorio existe lo eliminamos
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


def user_directory_path_banner(instance, filename):
    profile_picture_name = 'users/{0}/banner.jpg'.format(instance.user.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name

#opciones de verificacion de perfil de usuario y hacemos referencia en el modelo que hemos creado campo verified
VERIFICATION_OPTIONS=(
    ('unverified', 'unverified'),
    ('verified', 'verified'),
)

# Creamos un modelo de usuario extendido con los campos que necesitamos base mas id
class User(AbstractUser):
    stripe_customer_id = models.CharField(max_length=50)

#perfil user 
class Profile(models.Model):
    #relacion con el usuario con su foreign key e indicamos que si el vinculo se rempo este usuario se elimina
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(default='users/user_default_profile.png', upload_to=user_directory_path_profile)
    banner = models.ImageField(default='users/user_default_bg.jpg', upload_to=user_directory_path_banner)
    #campo de verificacion de perfil, por defecto es no identificado
    verified = models.CharField(max_length=10, choices=VERIFICATION_OPTIONS, default='unverified')

    coins = models.DecimalField(max_digits=19, decimal_places=2, default=0, blank=False)
    #many to many distintas tablas conectadas
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    date_created = models.DateField(auto_now_add=True)

    #User info
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    #con esto desde el panel de administracion podemos ver el nombre del usuario
    def __str__(self):
        return self.user.username

#notificacion de creacion de perfil
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# created profile
post_save.connect(create_user_profile, sender=User)
# save created profile
post_save.connect(save_user_profile, sender=User)
