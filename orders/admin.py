from django.contrib import admin

from orders.models import ConcreteExtraInOrder, ConcreteMenuInOrder, ConcreteWorkerInOrder, Order

class ConcreteMenuInOrderInline(admin.StackedInline):
    model = ConcreteMenuInOrder
    extra=0
    can_delete = True
    verbose_name = 'Menú'
    verbose_name_plural = 'Menús'
    readonly_fields = ('total_cost',)

class ConcreteExtraInOrderInline(admin.StackedInline):
    model = ConcreteExtraInOrder
    extra=0
    can_delete = True
    verbose_name = 'Extra'
    verbose_name_plural = 'Extras'
    readonly_fields = ('total_cost',)

class ConcreteWorkerInOrderInline(admin.StackedInline):
    model = ConcreteWorkerInOrder
    extra=0
    can_delete = True
    verbose_name = 'Trabajador'
    verbose_name_plural = 'Trabajadores'
    readonly_fields = ('total_cost',)

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ('name','order_type','start_date','total_cost','active_flag','planned_flag','completed_flag','feedback_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ConcreteMenuInOrderInline,ConcreteWorkerInOrderInline,ConcreteExtraInOrderInline]

    search_field= ('name','description','order_type')
    list_filter = ('active_flag','completed_flag','order_type')
    readonly_fields = ('total_cost','menu_cost','extra_cost','worker_cost','profit','profit_rate','menu_ammount','created','modified')

