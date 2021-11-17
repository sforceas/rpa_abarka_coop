from django.contrib import admin

from stakeholders.models import Client, ContactPerson, Provider

# Inline models

class ContactPersonInline(admin.StackedInline):
    model = ContactPerson
    extra=0
    can_delete = True
    verbose_name = 'Persona de contacto'
    verbose_name_plural = 'Personas de contacto'

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Client admin"""
    list_display = ('name','nif','mail','phone_number','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ContactPersonInline]
    
    search_field= ('name','nif')
    list_filter = ()
    readonly_fields = ('created','modified')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Provider admin"""
    list_display = ('name','nif','delivery_method','payment_method','mail','phone_number','active_flag') # Campos que debe mostrar en el display de admin
    list_display_links=('name',) # Elementos linkados al detalle
    list_editable=() # Elementos editables desde admin
    inlines = [ContactPersonInline]
    
    search_field= ('name','nif')
    list_filter = ('delivery_method','payment_method')
    readonly_fields = ('created','modified')