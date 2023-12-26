from django import forms
from ventas.models import Cliente, Producto
#formulario de agregar cliente
class AddClienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nit', 'nombre', 'telefono', 'direccion')
        labels = {

            'nit': 'Nit cliente: ',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Telefono cliente: ',
            'direccion': 'Direccion cliente: '
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nit', 'nombre', 'telefono', 'direccion')
        labels = {
            'nit': 'Nit cliente: ',
            'nombre': 'Nombre cliente: ',
            'telefono': 'Telefono cliente: ',
            'direccion': 'Direccion cliente: '
        }
        widgets = {
            
            'nit': forms.TextInput(attrs={'type': 'text', 'id': 'nit_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion_editar'}),
        }

#formulario de agregar PRODUCTO
class AddProductoForm (forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'precio', 'stock', 'imagen')
        labels = {

            'nombre': 'Nombre producto: ',
            'descripcion': 'Descripcion producto: ',
            'precio': 'Precio producto: ',
            'stock': 'stock producto: ',
            'imagen': 'Imagen: '

        }        

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'precio', 'stock', 'imagen')
        labels = {
            'nombre': 'Nombre producto: ',
            'descripcion': 'Descripcion producto: ',
            'precio': 'Precio producto: ',
            'stock': 'Stock producto: ',
            'imagen': 'Imagen: ',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar_producto'}),
            'descripcion': forms.Textarea(attrs={'id': 'descripcion_editar_producto'}),
            'precio': forms.TextInput(attrs={'id': 'precio_editar_producto'}),
            'stock': forms.TextInput(attrs={'id': 'stock_editar_producto'}),
            'imagen': forms.ClearableFileInput(attrs={'id': 'imagen_editar_producto'}),
        }