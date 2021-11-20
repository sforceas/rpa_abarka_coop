from django.urls import path, include

from django.contrib import admin

from orders import views as oders_wiews
"""
Librerias para poder visualizar imagenes o media desde el panel de administracion.
"""
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [

    path("admin/", admin.site.urls),
    path("order/",oders_wiews.list_orders, name="list_orders"),
    path("order/<int:pk>/",oders_wiews.detailed_order, name="detailed_order")

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # Configurado en settings.py para mostrar media durante desarrollo


