from django.contrib import admin
from .models import Autobus, Pasajero, Ruta, Viaje, Boleto

@admin.register(Autobus)
class AutobusAdmin(admin.ModelAdmin):
    list_display = ('placa', 'capacidad')
    search_fields = ('placa',)

@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dpi', 'correo')
    search_fields = ('nombre', 'dpi', 'correo')

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('origin_destino', 'precio')
    search_fields = ('origen', 'destino')

    @admin.display(description='Ruta')
    def origin_destino(self, obj):
        return f"{obj.origen} - {obj.destino}"

class BoletoInline(admin.TabularInline):
    model = Boleto
    extra = 1

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('ruta', 'autobus', 'fecha_salida', 'asientos_disponibles')
    list_filter = ('fecha_salida', 'ruta')
    date_hierarchy = 'fecha_salida'
    inlines = [BoletoInline]

    @admin.display(description='Asientos Libres')
    def asientos_disponibles(self, obj):
        ocupados = obj.boletos.count()
        return obj.autobus.capacidad - ocupados

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('numero_asiento', 'pasajero', 'viaje')
    search_fields = ('pasajero__nombre', 'pasajero__dpi')
    list_filter = ('viaje',)

admin.site.site_header = "Transportes Sanluiseña Express"
admin.site.site_title = "Admin Sanluiseña Express"
admin.site.index_title = "Gestión de Operaciones Diarias"
