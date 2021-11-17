from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField
from django.db.models.fields.related import ForeignKey

DELIVERY_CHOICES=[('collect','Recogida de pedido'),('selfservice','Autoservicio'),('delivery','A domicilio')]
PAYMENT_CHOICES=[('transfer','Transferencia'),('cash','Efectivo'),('card','Tarjeta'),('bizum','Bizum'),('paypal','Paypal')]

# Create your models here.
class Stakeholder(models.Model):

    name=CharField(verbose_name='Nombre *',max_length=80)
    legal_name=CharField(verbose_name='Razón social *',max_length=80,default='')
    nif=CharField(verbose_name='NIF/DNI *',max_length=30,default='')
    billing_adress=CharField(verbose_name='Dirección de facturación *',max_length=300,default='')
    phone_number=CharField(verbose_name='Teléfono de contacto *',max_length=30,default='')
    mail=CharField(verbose_name='Correo electrónico *',max_length=80,default='')

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    
    def __str__(self):
        """Return title."""
        return f'{self.name}'

class Provider(Stakeholder):
    """Provider model"""
    delivery_method=CharField(verbose_name='Método de entrega:',choices=DELIVERY_CHOICES,max_length=80)
    delivery_adress=CharField(verbose_name='Dirección de recogida/envío *',max_length=300,default='')
    payment_method=CharField(verbose_name='Método de pago *',choices=PAYMENT_CHOICES,max_length=80)
    payment_time=IntegerField(verbose_name='Período de pago (días)',default=0)

class Client(Stakeholder):
    """Client model"""
    
    delivery_adress=CharField(verbose_name='Dirección de entrega *',max_length=300,default='')
    billing_time=IntegerField(verbose_name='Período de cobro (días)',default=0)


class ContactPerson(models.Model):
    """Contact person model"""
    name=CharField(verbose_name='Nombre *',max_length=80)
    phone_number=CharField(verbose_name='Teléfono de contacto *',max_length=30,default='')
    mail=CharField(verbose_name='Correo electrónico *',max_length=80,default='')
    stakeholder=ForeignKey(to=Stakeholder,verbose_name='Ogranización',on_delete=CASCADE)