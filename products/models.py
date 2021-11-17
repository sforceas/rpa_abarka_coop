from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DecimalField, IntegerField, BooleanField, DateTimeField
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.
MEASURING_UNITS = [('kg','Kilogramo'),('l','Litro'),('ud','Unidad')]

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
    ('halal','Halal'),
    ('pig_meat','Cerdo'),
    ('veggie','Vegetariano'),
    ('vegan','Vegano'),
    ('spicy','Picante'),
    ('gluten','Gluten'),
    ('dried_fruits','Frutos cáscara'),
    ('mollusks','Moluscos'),
    ('fish','Pescado'),
    ('crustacean','Crustáceos'),
    ('sesame','Sésamo'),
    ('eggs','Huevos'),
    ('milk','Lácteos'),
    ('mustard','Mostaza'),
    ('celery','Apio'),
    ('peanut','Cacahuete'),
    ('sulfit','Sulfitos'),
    ('soy','Soja'),
    ('lupins','Altramuces'),
]

class Allergen(models.Model):
    """Allergens models"""
    CharField(verbose_name='Nombre',max_length=80)

    def __str__(self):
        """Return title."""
        return f'{self.name}'

class Ingredient(models.Model):
    """Ingredient model"""
    name=CharField(verbose_name='Nombre',max_length=80)
    description=CharField(verbose_name='Descripción',blank=True, max_length=300)

    kcal = IntegerField(verbose_name='Calorías (kcal/100g)',blank=True)
    ingredient_type = CharField(verbose_name='Tipo de ingrediente',choices=INGREDIENT_TYPES,max_length=30)

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
    provider=CharField(verbose_name='Proveedor *',max_length=80) #Sustituir por Provider
    description=CharField(verbose_name='Descripción del producto *',max_length=300,default='')
    reference=CharField(verbose_name='Referencia producto *',max_length=30,default='')
    
    allergens = ManyToManyField(to=Allergen,verbose_name='Alérgenos y dietas especiales *',max_length=80,blank=True)
    measuring_unit=CharField(verbose_name='Unidad de medida',max_length=5,choices=MEASURING_UNITS,default='kg') 
    pack_units=DecimalField(verbose_name=' Formato (kg,litro o uds. por paquete) *',blank=True,max_digits=7,decimal_places=2,default='1')
    price_pack=DecimalField(verbose_name='Precio (sin IVA)*',blank=True,max_digits=7,decimal_places=2)
    price_unit=DecimalField(verbose_name='Precio por unidad de medida',blank=True,max_digits=7,decimal_places=2,default=0)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)

    @property
    def calculate_price_per_unit(self):
        return round(self.price_unit/self.pack_units,2)
     
    def save(self, *args, **kwargs):
        self.price_unit = self.calculate_price_per_unit
        super(ConcreteIngredient, self).save(*args, **kwargs)

    def __str__(self):
        """Return title."""
        return f'{self.ingredient} de {self.provider}'