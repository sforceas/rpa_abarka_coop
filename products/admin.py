from django.contrib import admin

from products.models import ConcreteIngredient, Ingredient

# Register your models here.
# Inlime models

class ConcreteIngredientInline(admin.StackedInline):
    model = ConcreteIngredient
    extra=0
    can_delete = True
    verbose_name = 'Ingrediente concreto'
    verbose_name_plural = 'Ingredientes concretos'

# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient admin"""
    list_display = ('name','ingredient_type') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteIngredientInline]
    search_field= ('name','description','ingredient_type')
    list_filter = ('ingredient_type','allergens')
    readonly_fields = ()


@admin.register(ConcreteIngredient)
class ConcreteIngredientAdmin(admin.ModelAdmin):
    """Ingredient admin"""
    list_display = ('ingredient','provider','pack_kg','price_pack','price_kg','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('ingredient','provider') # Elementos linkados al detalle
    list_editable=('price_pack',) # Elementos editables desde admin

    search_field= ('name','description','ingredient_type')
    list_filter = ('active_flag','provider')
    readonly_fields = ('created','modified')

#inlines = [IngredientInline,]