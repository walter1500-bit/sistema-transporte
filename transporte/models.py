from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Autobus(models.Model):
    placa = models.CharField(max_length=20, unique=True, verbose_name=_("Placa"))
    capacidad = models.PositiveIntegerField(verbose_name=_("Capacidad de Pasajeros"))

    def __str__(self):
        return f"{self.placa} ({self.capacidad} asientos)"

    class Meta:
        verbose_name = _("Autobús")
        verbose_name_plural = _("Autobuses")

class Pasajero(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre Completo"))
    dpi = models.CharField(max_length=13, unique=True, verbose_name=_("DPI"))
    correo = models.EmailField(verbose_name=_("Correo Electrónico"))

    def __str__(self):
        return f"{self.nombre} - {self.dpi}"

    class Meta:
        verbose_name = _("Pasajero")
        verbose_name_plural = _("Pasajeros")

class Ruta(models.Model):
    origen = models.CharField(max_length=100, verbose_name=_("Origen"))
    destino = models.CharField(max_length=100, verbose_name=_("Destino"))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))

    def __str__(self):
        return f"{self.origen} a {self.destino} (Q{self.precio})"

    class Meta:
        verbose_name = _("Ruta")
        verbose_name_plural = _("Rutas")

class Viaje(models.Model):
    autobus = models.ForeignKey(Autobus, on_delete=models.CASCADE, verbose_name=_("Autobús"))
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, verbose_name=_("Ruta"))
    fecha_salida = models.DateTimeField(verbose_name=_("Fecha y Hora de Salida"))

    def clean(self):
        # Un mismo bus no puede estar asignado a más de un viaje en la misma fecha y hora.
        overlap = Viaje.objects.filter(
            autobus=self.autobus,
            fecha_salida=self.fecha_salida
        ).exclude(pk=self.pk).exists()
        
        if overlap:
            raise ValidationError(
                _("El autobús %(autobus)s ya tiene un viaje programado para %(fecha)s."),
                params={'autobus': self.autobus.placa, 'fecha': self.fecha_salida},
            )

    def __str__(self):
        return f"{self.ruta} - {self.fecha_salida.strftime('%d/%m/%Y %H:%M')}"

    @property
    def asientos_disponibles(self):
        return self.autobus.capacidad - self.boletos.count()

    @property
    def porcentaje_ocupacion(self):
        if self.autobus.capacidad == 0:
            return 100
        return (self.boletos.count() / self.autobus.capacidad) * 100

    class Meta:
        verbose_name = _("Viaje")
        verbose_name_plural = _("Viajes")

class Boleto(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name="boletos", verbose_name=_("Viaje"))
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name=_("Pasajero"))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Usuario (Cliente)"))
    numero_asiento = models.PositiveIntegerField(verbose_name=_("Número de Asiento"))

    def clean(self):
        # No pueden existir dos boletos con el mismo número de asiento en un mismo viaje
        asiento_ocupado = Boleto.objects.filter(
            viaje=self.viaje,
            numero_asiento=self.numero_asiento
        ).exclude(pk=self.pk).exists()

        if asiento_ocupado:
            raise ValidationError(_("El asiento %(asiento)d ya está ocupado en este viaje."), params={'asiento': self.numero_asiento})

        # No se pueden vender más boletos que la capacidad del bus asignado al viaje.
        total_boletos = self.viaje.boletos.exclude(pk=self.pk).count()
        if total_boletos >= self.viaje.autobus.capacidad:
            raise ValidationError(_("El autobús para este viaje ha alcanzado su capacidad máxima (%(cap)d)."), params={'cap': self.viaje.autobus.capacidad})

        # El número de asiento no puede exceder la capacidad
        if self.numero_asiento > self.viaje.autobus.capacidad:
            raise ValidationError(_("El número de asiento %(asiento)d excede la capacidad del autobús (%(cap)d)."), params={'asiento': self.numero_asiento, 'cap': self.viaje.autobus.capacidad})

    class Meta:
        unique_together = ('viaje', 'numero_asiento')
        verbose_name = _("Boleto")
        verbose_name_plural = _("Boletos")

    def __str__(self):
        return f"Boleto {self.numero_asiento} - {self.pasajero.nombre} (Viaje: {self.viaje})"
