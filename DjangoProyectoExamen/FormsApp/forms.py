from django import forms
from .models import *

class New_Producto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('Nombre', 'PVP')

class New_Venta(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('idCliente',)

class New_Cliente(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('Nombre', 'tlf')

class New_LineaVenta(forms.ModelForm):

    class Meta:
        model = LineasVenta
        widgets = {
            'idVenta': forms.HiddenInput(),
        }
        fields = ('idVenta', 'idProducto', 'Cantidad')