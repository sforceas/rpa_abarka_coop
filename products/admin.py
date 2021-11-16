from django.contrib import admin

from products.models import Ingredient

# Register your models here.
# Inlime models

class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra=0
    can_delete = False
    verbose_name = 'Ingrediente'
    verbose_name_plural = 'Ingredientes'

# Register your models here.

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient admin"""
    list_display = ('name','ingredient_type','price_kg','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=('price_kg',) # Elementos editables desde admin

    search_field= ('name','description','ingredient_type')
    list_filter = ('active_flag','ingredient_type','allergens')
    readonly_fields = ('created','modified')

#inlines = [IngredientInline,]