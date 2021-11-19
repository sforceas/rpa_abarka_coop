from typing import Text
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import BooleanField, CharField, DateTimeField, DecimalField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from products.models import Extra, Menu
from stakeholders.models import Client
from workers.models import Worker

ORDER_TYPES=[('catering','Catering'),('festival','Festival'),('wedding','Boda')]
# Create your models here.

TASK_TYPES=[('production','Producción'),('camarera','Camarera'),('transport','Transporte')]

class Order(models.Model):

    name=CharField(verbose_name='Nombre *',max_length=80)
    description=CharField(verbose_name='Detalles del evento',max_length=600,blank=True,default='')
    order_type=CharField(verbose_name='Tipo de pedido *',max_length=30,choices=ORDER_TYPES,default='')
    client=ForeignKey(to=Client,verbose_name='Cliente *',on_delete=PROTECT)

    start_date=DateTimeField(verbose_name='Fecha de inicio *')
    end_date=DateTimeField(verbose_name='Fecha de finalización *')
    labour_days=IntegerField(verbose_name='Días laborables * ',default=1)
    
    menu_ammount=IntegerField(verbose_name='Número de menús',default=1)
    menu_cost=DecimalField(verbose_name='Coste de menús (€)',blank=True,max_digits=7,decimal_places=2,default=0)
    worker_cost=DecimalField(verbose_name='Coste de trabajadores (€)',blank=True,max_digits=7,decimal_places=2,default=0)
    extra_cost=DecimalField(verbose_name='Coste de extras (€)',blank=True,max_digits=7,decimal_places=2,default=0)
    total_cost=DecimalField(verbose_name='Coste total (€)',blank=True,max_digits=7,decimal_places=2,default=0)

    completed_flag=BooleanField(verbose_name='Completado',default=False)
    completed_comments=TextField(verbose_name='Observaciones final de evento',blank=True)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    
    @property
    def calculate_menu_cost(self):
        menu_cost=0
        menus_in_order=list(ConcreteMenuInOrder.objects.filter(order=self))
        for menu in menus_in_order:
            menu_cost = menu_cost+menu.total_cost
        return round(menu_cost,2)
    
    @property
    def calculate_worker_cost(self):
        worker_cost=0
        workers_in_order=list(ConcreteWorkerInOrder.objects.filter(order=self))
        for worker in workers_in_order:
            worker_cost = worker_cost+worker.total_cost
        return round(worker_cost,2)
    
    
    @property
    def calculate_extra_cost(self):
        extra_cost=0
        extras_in_order=list(ConcreteExtraInOrder.objects.filter(order=self))
        for extra in extras_in_order:
            extra_cost = extra_cost+extra.total_cost
        return round(extra_cost,2)
    
    @property
    def calculate_menu_ammount(self):
        menu_ammount=0
        menus_in_order=list(ConcreteMenuInOrder.objects.filter(order=self))
        for menu in menus_in_order:
            menu_ammount = menu_ammount+menu.menu_ammount
        return round(menu_ammount,2)

    def save(self, *args, **kwargs):
        self.menu_ammount = self.calculate_menu_ammount
        self.menu_cost = self.calculate_menu_cost
        self.worker_cost = self.calculate_worker_cost
        self.extra_cost = self.calculate_extra_cost

        self.total_cost = self.menu_cost+self.extra_cost+self.worker_cost
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        """Return title."""
        return f'{self.name} at {self.start_date}'

class ConcreteMenuInOrder(models.Model):
    
    order=ForeignKey(to=Order ,verbose_name='Pedido *',on_delete=CASCADE)
    menu=ForeignKey(to=Menu ,verbose_name='Menú *',on_delete=PROTECT)
    menu_ammount=IntegerField(verbose_name='Número de menús *',blank=True,default='1')
    total_cost=DecimalField(verbose_name='Coste total (€)',blank=True,max_digits=7,decimal_places=2,default='0')

    @property
    def calculate_total_cost(self):
        return round(self.menu_ammount*self.menu.total_cost,2)
     
    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost
        super(ConcreteMenuInOrder, self).save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        """Return title."""
        return f'{self.menu} in {self.order}'

class ConcreteExtraInOrder(models.Model):

    order=ForeignKey(to=Order ,verbose_name='Pedido *',on_delete=CASCADE)
    extra=ForeignKey(to=Extra ,verbose_name='Extra *',on_delete=PROTECT)
    extra_ammount=IntegerField(verbose_name='Número de extras *',blank=True,default='1')
    total_cost=DecimalField(verbose_name='Coste total (€)',blank=True,max_digits=7,decimal_places=2,default='0')

    @property
    def calculate_total_cost(self):
        return round(self.extra_ammount*self.extra.total_cost,2)
     
    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost
        super(ConcreteExtraInOrder, self).save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        """Return title."""
        return f'{self.extra} in {self.order}'

class ConcreteWorkerInOrder(models.Model):
    
    order=ForeignKey(to=Order ,verbose_name='Pedido *',on_delete=CASCADE)
    worker=ForeignKey(to=Worker ,verbose_name='Trabajador *',on_delete=PROTECT)
    task=CharField(verbose_name='Tarea *',max_length=30,choices=TASK_TYPES,default='')

    start_date=DateTimeField(verbose_name='Fecha de inicio *')
    end_date=DateTimeField(verbose_name='Fecha de finalización *')
    hours_ammount=IntegerField(verbose_name='Número de horas *',blank=True,default='1')
    total_cost=DecimalField(verbose_name='Coste total (€)',blank=True,max_digits=7,decimal_places=2,default='0')

   #CALCULAR HORAS A PARTIR DE HORARIO 

    @property
    def calculate_total_cost(self):
        return round(self.hours_ammount*self.worker.hour_cost,2)
     
    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost
        super(ConcreteWorkerInOrder, self).save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        """Return title."""
        return f'{self.worker} en {self.order}'