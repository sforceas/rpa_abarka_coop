from django.contrib import admin

from products.models import Allergen, ConcreteIngredient, ConcreteIngredientInRecipe, ConcreteRecipeInMenu, Extra, Ingredient, Menu, Recipe

# Register your models here.
# Inlime models

class ConcreteIngredientInline(admin.StackedInline):
    model = ConcreteIngredient
    extra=0
    can_delete = True
    verbose_name = 'Ingrediente concreto'
    verbose_name_plural = 'Ingredientes concretos'

class ConcreteIngredientInRecipeInline(admin.StackedInline):
    model = ConcreteIngredientInRecipe
    extra=0
    can_delete = True
    verbose_name = 'Ingrediente concreto en receta'
    verbose_name_plural = 'Ingredientes concretos en receta'

class ConcreteRecipeInMenuInLine(admin.StackedInline):
    model = ConcreteRecipeInMenu
    extra=0
    can_delete = True
    verbose_name = 'Receta'
    verbose_name_plural = 'Recetas'

# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient admin"""
    list_display = ('name','ingredient_type') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteIngredientInline]
    
    search_field= ('name','description','ingredient_type')
    list_filter = ('ingredient_type',)
    readonly_fields = ('created','modified')

@admin.register(ConcreteIngredient)
class ConcreteIngredientAdmin(admin.ModelAdmin):
    """Ingredient admin"""
    list_display = ('ingredient','provider','pack_units','price_pack','price_unit','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('ingredient','provider') # Elementos linkados al detalle
    list_editable=('price_pack',) # Elementos editables desde admin

    search_field= ('name','description','ingredient_type')
    list_filter = ('active_flag','provider','allergens')
    readonly_fields = ('price_unit','created','modified')

    def save_model(self, request, obj, form, change):
        obj.price_unit = round(obj.price_pack/obj.pack_units,2)
        super().save_model(request, obj, form, change)

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    """Allergen admin"""
    list_display = ('name',) # Campos que debe mostrar en el display de admin
    list_display_links=() # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe admin"""
    list_display = ('name','recipe_type','total_cost','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteIngredientInRecipeInline]

    search_field= ('name','description','recipe_type')
    list_filter = ('active_flag','recipe_type')
    readonly_fields = ('total_cost','created','modified')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Menu admin"""
    list_display = ('name','menu_type','total_cost','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteRecipeInMenuInLine]

    search_field= ('name','description','menu_type')
    list_filter = ('active_flag','menu_type')
    readonly_fields = ('total_cost','created','modified')

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    """Extra admin"""
    list_display = ('name','extra_type','total_cost','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin

    search_field= ('name','description','extra_type')
    list_filter = ('active_flag','extra_type')
    readonly_fields = ('total_cost','created','modified')
