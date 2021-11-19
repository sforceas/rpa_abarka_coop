from django.contrib import admin

from orders.models import ConcreteExtraInOrder, ConcreteMenuInOrder, Order

class ConcreteMenuInOrderInline(admin.StackedInline):
    model = ConcreteMenuInOrder
    extra=0
    can_delete = True
    verbose_name = 'Menú'
    verbose_name_plural = 'Menús'

class ConcreteExtraInOrderInline(admin.StackedInline):
    model = ConcreteExtraInOrder
    extra=0
    can_delete = True
    verbose_name = 'Extra'
    verbose_name_plural = 'Extras'

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ('name','order_type','start_date','total_cost','active_flag','completed_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteMenuInOrderInline,ConcreteExtraInOrderInline]

    search_field= ('name','description','order_type')
    list_filter = ('active_flag','completed_flag','order_type')
    readonly_fields = ('created','modified')

