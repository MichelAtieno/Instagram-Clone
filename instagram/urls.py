from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^$', views.register, name='register'),
    url(r'^home/$', views.home, name='home'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^upload/$', views.image, name='upload_image'),
    url(r'^image/(?P<image_id>\d+)', views.image_comment, name='image_comment'),
    url(r'^accounts/edit', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

     