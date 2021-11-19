from django.contrib import admin

from workers.models import Worker

# Register your models here.

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    """Worker admin"""
    list_display = ('first_name','second_name','worker_type','active_flag','driving_license_flag','own_car_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('first_name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin

    search_field= ('name','description','worker_type')
    list_filter = ('active_flag','driving_license_flag','own_car_flag')
    readonly_fields = ('created','modified')
