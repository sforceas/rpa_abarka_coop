from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DecimalField, IntegerField, BooleanField, DateTimeField
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ForeignKey

# Create your models here.

INGREDIENT_TYPES = [
    ('fruit','Fruta'),
    ('vegetable','Verduras'),
    ('cereal','Cereales'),
    ('legume','Legumbres'),
    ('dried_fruit','Frutos secos'),
    ('meat','Carnes'),
    ('fish','Pescados y mariscos'),
    ('lactic','Lácticos'),
    ('eggs', 'Huevo y derivados'),
    ('species','Especias y condimentos'),
    ('infusions','Infusiones'),
    ('oils','Aceites y grasas vegetales'),
    ('water','Agua'),
    ('others','Otros'),
    ]

CONSERVATION_METHODS = [
    ('storage','Almacén'),
    ('nevera','Nevera'),
    ('freezer','Congelador'),
]

ALLERGENS =[
    ('spicy','Picante'),
    ('gluten','Gluten'),
    ('dried_fruits','Frutos secos'),
    ('mollusks','Moluscos'),
    ('fish','pescado'),
    ('crustacean','Crustáceos'),
    ('sesame','Sésamo'),
    ('lactosa','Lactosa'),
    ('mustard','Mostaza'),
    ('celery','Apio'),
    ('peanut','Cacahuete'),
    ('sulfit','Sulfitos'),
    ('soy','Soja'),
    ('lupins','Altramuces'),
]
class Ingredient(models.Model):
    """Ingredient model"""
    name=models.CharField(verbose_name='Nombre',max_length=80)
    description=CharField(verbose_name='Descripción',blank=True, max_length=300)

    kcal = IntegerField(verbose_name='Calorías (kcal/100g)',blank=True)
    ingredient_type = CharField(verbose_name='Tipo de ingrediente',choices=INGREDIENT_TYPES,max_length=30)
    allergens = ArrayField(
        CharField(choices=ALLERGENS,max_length=30),verbose_name='Alérgenos',blank=True)
    conservation_method=CharField(verbose_name='Conservación',choices=CONSERVATION_METHODS, max_length=30,default='No definido')
    lifetime = IntegerField(verbose_name='Vida útil (días)',blank=True)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    def __str__(self):
        """Return title."""
        return f'{self.name}'

class ConcreteIngredient(models.Model):
    """Concrete ingredient. Herits from Ingredient"""
    
    ingredient=ForeignKey(to=Ingredient ,verbose_name='Ingrediente',on_delete=CASCADE)
    provider=CharField(verbose_name='Proveedor',max_length=80) #Sustituir por Provider
    pack_kg=DecimalField(verbose_name='Kg o L por paquete',blank=True,max_digits=7,decimal_places=2)
    price_pack=DecimalField(verbose_name='Precio por paquete',blank=True,max_digits=7,decimal_places=2)
    price_kg=DecimalField(verbose_name='Precio por kg o L',blank=True,max_digits=7,decimal_places=2)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)

    def __str__(self):
        """Return title."""
        return f'{self.ingredient} de {self.provider}'