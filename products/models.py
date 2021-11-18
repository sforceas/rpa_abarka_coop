from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, DecimalField, IntegerField, BooleanField, DateTimeField, TimeField
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from stakeholders.models import Provider

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

RESOURCE_TYPES = [('person','Personal (hora)'),('machine','Máquina (hora)'),('transport','Transporte (hora)')]

RECIPE_TYPES = [('drink','Bebidas'),('hot_drink','Bebidas calientes'),('snacks','Snacks y entrantes'),('main','Principales'),('sauces','Salsas'),('desserts','Postres y dulces')]

MENU_TYPES = [('coffee_break','Coffee Break'),('festival','Ferias y festivales'),('wedding','Bodas'),('experiencie','Experiencia gastronómica')]

CONSERVATION_METHODS = [
    ('storage','Almacén'),
    ('nevera','Nevera'),
    ('freezer','Congelador'),
]

class Allergen(models.Model):
    """Allergens models"""
    name=CharField(verbose_name='Nombre',max_length=80,default='')
    emoji=CharField(verbose_name='Emoticono',max_length=10,blank=True,default='')

    def __str__(self):
        """Return title."""
        return f'{self.name}'

class Ingredient(models.Model):
    """Ingredient model"""
    name=CharField(verbose_name='Nombre',max_length=80)
    description=CharField(verbose_name='Descripción',max_length=300,blank=True,default='')

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
    """Concrete ingredient model"""
    
    ingredient=ForeignKey(to=Ingredient ,verbose_name='Ingrediente',on_delete=CASCADE)
    provider=ForeignKey(to=Provider,verbose_name='Proveedor *',on_delete=PROTECT)
    description=CharField(verbose_name='Descripción',max_length=300,blank=True,default='')
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
        return round(self.price_pack/self.pack_units,2)
     
    def save(self, *args, **kwargs):
        self.price_unit = self.calculate_price_per_unit
        super(ConcreteIngredient, self).save(*args, **kwargs)

    def __str__(self):
        """Return title."""
        return f'{self.ingredient} de {self.provider}'

class Resource(models.Model):
    """Resource model"""
    name=CharField(verbose_name='Nombre del recurso',max_length=80)
    description=CharField(verbose_name='Descripción',max_length=300,blank=True,default='')
    resource_type = CharField(verbose_name='Tipo de recurso',choices=RESOURCE_TYPES,max_length=30)
    price_unit=DecimalField(verbose_name='Precio por unidad',blank=True,max_digits=7,decimal_places=2,default=0)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    
    def __str__(self):
        """Return title."""
        return f'{self.name}'

class Recipe(models.Model):

    name=CharField(verbose_name='Nombre *',max_length=80)
    description=CharField(verbose_name='Descripción',max_length=300,blank=True,default='')
    recipe_type=CharField(verbose_name='Tipo de receta*',max_length=30,choices=RECIPE_TYPES,default='')
    
    min_servings=IntegerField(verbose_name='Raciones mínimas *',default=1)
    preparation_time=IntegerField(verbose_name='Tiempo de preparación (min)',blank=True)
    ingredient_cost=DecimalField(verbose_name='Coste ingredientes por ración (€)',blank=True,max_digits=7,decimal_places=2,default=0)
    resource_cost=DecimalField(verbose_name='Coste recursos por ración (€) *',blank=True,max_digits=7,decimal_places=2,default=0)#Calculado por horas y gasto de recursos
    total_cost=DecimalField(verbose_name='Coste total por ración (€)',blank=True,max_digits=7,decimal_places=2,default=0)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    
    @property
    def calculate_ingredient_cost(self):
        ingredient_cost=0
        concrete_ingredients_in_recipe=list(ConcreteIngredientInRecipe.objects.filter(recipe=self))
        for ingredient in concrete_ingredients_in_recipe:
            ingredient_cost = ingredient_cost+ingredient.cost_per_serving
        return round(ingredient_cost,2)
    
    @property
    def calculate_resource_cost(self):
        resource_cost=0
        concrete_resources_in_recipe=list(ConcreteResourceInRecipe.objects.filter(recipe=self))
        for resource in concrete_resources_in_recipe:
            resource_cost = resource_cost+resource.cost_per_serving
        return round(resource_cost,2)

    def save(self, *args, **kwargs):
        self.ingredient_cost = self.calculate_ingredient_cost
        self.resource_cost = self.calculate_resource_cost

        self.total_cost=self.ingredient_cost+self.resource_cost
        super(Recipe, self).save(*args, **kwargs)


    def __str__(self):
        """Return title."""
        return f'{self.name}'

class ConcreteIngredientInRecipe(models.Model):
    
    recipe=ForeignKey(to=Recipe ,verbose_name='Receta',on_delete=CASCADE)
    concrete_ingredient=ForeignKey(to=ConcreteIngredient ,verbose_name='Ingrediente *',on_delete=PROTECT)
    ammout_per_serving=DecimalField(verbose_name='Cantidad por ración (kg,litro o uds.) *',blank=True,max_digits=7,decimal_places=2,default='0')
    cost_per_serving=DecimalField(verbose_name='Coste por ración (€)',blank=True,max_digits=7,decimal_places=2,default='0')

    @property
    def calculate_cost_per_ingredient(self):
        return round(self.ammout_per_serving*self.concrete_ingredient.price_unit,2)
     
    def save(self, *args, **kwargs):
        self.cost_per_serving = self.calculate_cost_per_ingredient
        super(ConcreteIngredientInRecipe, self).save(*args, **kwargs)
        self.recipe.save()


    def __str__(self):
        """Return title."""
        return f'{self.concrete_ingredient} in {self.recipe}'
    
class ConcreteResourceInRecipe(models.Model):
    
    recipe=ForeignKey(to=Recipe ,verbose_name='Receta',on_delete=CASCADE)
    resource=ForeignKey(to=Resource ,verbose_name='Recurso *',on_delete=PROTECT)
    ammout_per_serving=DecimalField(verbose_name='Cantidad por ración *',blank=True,max_digits=7,decimal_places=2,default='0')
    cost_per_serving=DecimalField(verbose_name='Coste por ración (€)',blank=True,max_digits=7,decimal_places=2,default='0')

    @property
    def calculate_cost_per_resource(self):
        return round(self.ammout_per_serving*self.resource.price_unit,2)
     
    def save(self, *args, **kwargs):
        self.cost_per_serving = self.calculate_cost_per_resource
        super(ConcreteResourceInRecipe, self).save(*args, **kwargs)
        self.recipe.save()


    def __str__(self):
        """Return title."""
        return f'{self.resource} in {self.recipe}'

class Menu(models.Model):

    name=CharField(verbose_name='Nombre *',max_length=80)
    description=CharField(verbose_name='Descripción',max_length=300,blank=True,default='')
    menu_type=CharField(verbose_name='Tipo de menú *',max_length=30,choices=MENU_TYPES,default='')
    
    min_servings=IntegerField(verbose_name='Raciones mínimas *',default=1)
    preparation_time=IntegerField(verbose_name='Tiempo de preparación (min)',blank=True)
    #ingredient_cost=DecimalField(verbose_name='Coste ingredientes por ración (€)',blank=True,max_digits=7,decimal_places=2,default=0)
    #resource_cost=DecimalField(verbose_name='Coste recursos por ración (€) *',blank=True,max_digits=7,decimal_places=2,default=0)#Calculado por horas y gasto de recursos
    total_cost=DecimalField(verbose_name='Coste total por menú (€)',blank=True,max_digits=7,decimal_places=2,default=0)

    active_flag=BooleanField(verbose_name='Activo',default=True)
    created=DateTimeField(verbose_name='Creado',auto_now_add=True)
    modified=DateTimeField(verbose_name='Modificado',auto_now=True)
    
    @property
    def calculate_total_cost(self):
        total_cost=0
        recipes_in_menu=list(ConcreteRecipeInMenu.objects.filter(menu=self))
        for recipe in recipes_in_menu:
            total_cost = total_cost+recipe.cost_per_menu
        return round(total_cost,2)
    

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost
        super(Menu, self).save(*args, **kwargs)


    def __str__(self):
        """Return title."""
        return f'{self.name}'

class ConcreteRecipeInMenu(models.Model):
    
    menu=ForeignKey(to=Menu ,verbose_name='Menú *',on_delete=CASCADE)
    recipe=ForeignKey(to=Recipe ,verbose_name='Receta *',on_delete=PROTECT)
    rations_per_menu=IntegerField(verbose_name='Raciones por menú *',blank=True,default='1')
    cost_per_menu=DecimalField(verbose_name='Coste por menú (€)',blank=True,max_digits=7,decimal_places=2,default='0')

    @property
    def calculate_cost_per_menu(self):
        return round(self.rations_per_menu*self.recipe.total_cost,2)
     
    def save(self, *args, **kwargs):
        self.cost_per_menu = self.calculate_cost_per_menu
        super(ConcreteRecipeInMenu, self).save(*args, **kwargs)
        self.menu.save()


    def __str__(self):
        """Return title."""
        return f'{self.recipe} in {self.menu}'



