from django.db import models
from django.db.models.fields import BooleanField, CharField, DateTimeField, DecimalField
from django.db.models.fields.related import ForeignKey


WORKER_TYPES=[('partner','Socia'),('extern','Externa')]

# Create your models here.
class Worker(models.Model):

    first_name=CharField(verbose_name='Nombre *',max_length=80)
    second_name=CharField(verbose_name='Appelido *',max_length=80)
    worker_type=CharField(verbose_name='Tipo de trabajador *',max_length=20,choices=WORKER_TYPES,default='')
    driving_license_flag=BooleanField(verbose_name='Carnet de conducir',default=False)
    own_car_flag=BooleanField(verbose_name='Coche propio',default=False)

    phone_number=CharField(verbose_name='Teléfono *',max_length=20,default='')
    mail=CharField(verbose_name='Correo electrónico *',max_length=80,default='')

    hour_cost=DecimalField(verbose_name='Coste por hora (€)',blank=True,max_digits=7,decimal_places=2,default=0)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)


    def __str__(self):
        """Return title."""
        return f'{self.first_name} {self.second_name}'

