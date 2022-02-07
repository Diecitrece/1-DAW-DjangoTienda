from django.contrib import admin
from FormsApp import models
# Register your models here.
admin.site.register(models.Producto)
admin.site.register(models.Venta)
admin.site.register(models.LineasVenta)
admin.site.register(models.Cliente)
