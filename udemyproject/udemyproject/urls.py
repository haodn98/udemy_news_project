from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from main.sitemap import MyNewsSiteMap

from rest_framework import routers
from main import views

router = routers.DefaultRouter()
router.register("mynews", views.NewsViewSet)

sitemaps = {
    'news': MyNewsSiteMap(),
}
urlpatterns = [
    path('admin/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),

    path('rest/',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),

    path('media/<str:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<str:path>', serve, {'document_root': settings.STATIC_ROOT}),

    path('', include('main.urls')),
    path('', include('news.urls')),
    path('', include('category.urls')),
    path('', include('subcategory.urls')),
    path('', include('contactform.urls')),
    path('', include('trending.urls')),
    path('', include('manager.urls')),
    path('', include('newsletter.urls')),
    path('', include('comments.urls')),
    path('', include('blacklist.urls')),
    path('', include('answers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
