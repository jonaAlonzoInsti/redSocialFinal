from django.db import models
from django.utils import timezone

#llamamos al modelo usuario que creamos, ya que lo utilizaremos para enlasar el autor de la publicacion
from django.contrib.auth import get_user_model
User = get_user_model()

#declaracion para el nombre de la carpeta donde se guardaran las imagenes
#esta es para los post
def user_directory_path(instance, filename):
	return 'users/socialposts/{0}'.format(filename)

# Esta es para los mensajes directos
# def dm_directory_path(instance, filename):
# 	return 'users/messages/{0}'.format(filename)

#Distintos post que se pueden hacer
class SocialPost(models.Model):
    #compartir post
    shared_body = models.TextField(blank=True, null=True)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    shared_on = models.DateTimeField(blank=True, null=True)

    body=models.TextField()
    #many to many para subir distintas imagenes Blank es para podamos subir solo imagenes 
    image = models.ManyToManyField('Image', blank=True)
    #fecha de creacion
    created_on = models.DateTimeField(default=timezone.now)
    #autor de la publicacion con foreign key ya que puede tener distintos post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_post_author')
    #likes y dislikes para los post many to many ya que puede tener distintos likes y dislikes
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

#comentarios que se pueden hacer
class SocialComment(models.Model):
    #cuerpo del comentario
    comment = models.TextField()
    #post al que pertenece el comentario
    created_on = models.DateTimeField(default=timezone.now)
    #IMPORTANTE las variables utilizadas para cada modelo tienen que ser distintas para que no entren en conflicto
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_comment_author')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    #relacionamos los post con los comentarios
    post = models.ForeignKey('SocialPost', on_delete=models.CASCADE)
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return SocialComment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

#Modelo de la imagen a subir
class Image(models.Model):
    #imagen a subir, direccion donde se guardara la imagen
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)