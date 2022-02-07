"""DjangoProyectoExamen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FormsApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.mainpage),
    path('articulos/', views.articulos_mostrar),
    path('articulos/borrar/<int:id>', views.articulos_borrar),
    path('articulos/crear', views.articulos_crear),
    path('articulos/modificar/<int:id>', views.articulos_cambiar),
    path('articulos/destacados', views.articulos_destacados),
    path('clientes/', views.clientes_mostrar),
    path('clientes/borrar/<int:id>', views.clientes_borrar),
    path('clientes/crear/', views.clientes_crear),
    path('clientes/modificar/<int:id>', views.clientes_cambiar),
    path('ventas/', views.ventas_mostrar),
    path('ventas/borrar/<int:id>', views.ventas_borrar),
    path('ventas/crear', views.ventas_crear),
    path('ventas/modificar/<int:id>', views.ventas_cambiar),
    path('ventas/lineasventas/<int:id>', views.lineasventas),
    path('ventas/lineasventas/crear/<int:id>', views.lineasventas_crear),
    path('ventas/lineasventas/borrar/<int:id>/<int:idventa>', views.lineasventas_borrar),
    path('ventas/lineasventas/modificar/<int:id>/<int:idventa>', views.lineasventas_cambiar)

]+ static(settings.STATIC_URL)
