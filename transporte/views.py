from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Viaje, Pasajero, Boleto, Ruta, Autobus
from .forms import ViajeForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

@login_required
def lista_viajes(request):
    viajes = Viaje.objects.all().order_by('fecha_salida')
    return render(request, 'transporte/lista_viajes.html', {'viajes': viajes})

@login_required
def detalle_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)
    boletos = viaje.boletos.all().order_by('numero_asiento')
    return render(request, 'transporte/detalle_viaje.html', {'viaje': viaje, 'boletos': boletos})

@login_required
def reservar_boleto(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        dpi = request.POST.get('dpi')
        correo = request.POST.get('correo')
        numero_asiento = request.POST.get('numero_asiento')

        try:
            with transaction.atomic():
                # Buscar o crear pasajero
                pasajero, created = Pasajero.objects.get_or_create(
                    dpi=dpi,
                    defaults={'nombre': nombre, 'correo': correo}
                )
                
                # Crear el boleto (esto disparará las validaciones del modelo)
                boleto = Boleto(
                    viaje=viaje,
                    pasajero=pasajero,
                    usuario=request.user,
                    numero_asiento=int(numero_asiento)
                )
                boleto.full_clean()
                boleto.save()
                
                return render(request, 'transporte/exito.html', {'boleto': boleto})
        except ValidationError as e:
            error_msg = e.messages[0] if hasattr(e, 'messages') else str(e)
            return render(request, 'transporte/detalle_viaje.html', {
                'viaje': viaje,
                'boletos': viaje.boletos.all().order_by('numero_asiento'),
                'error': error_msg
            })
        except Exception as e:
            return render(request, 'transporte/detalle_viaje.html', {
                'viaje': viaje,
                'boletos': viaje.boletos.all().order_by('numero_asiento'),
                'error': f"Ocurrió un error inesperado: {str(e)}"
            })
    
    return redirect('detalle_viaje', viaje_id=viaje_id)


def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_viajes')
    else:
        form = UserCreationForm()
    return render(request, 'transporte/registro.html', {'form': form})

@login_required
def mis_boletos(request):
    boletos = Boleto.objects.filter(usuario=request.user).order_by('-viaje__fecha_salida')
    return render(request, 'transporte/mis_boletos.html', {'boletos': boletos})

@login_required
def imprimir_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id, usuario=request.user)
    return render(request, 'transporte/ticket_impresion.html', {'boleto': boleto})

# --- Admin Views ---

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'transporte/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_buses'] = Autobus.objects.count()
        context['total_rutas'] = Ruta.objects.count()
        context['total_viajes'] = Viaje.objects.count()
        return context

class AutobusListView(AdminRequiredMixin, ListView):
    model = Autobus
    template_name = 'transporte/autobus_list.html'
    context_object_name = 'buses'

class AutobusCreateView(AdminRequiredMixin, CreateView):
    model = Autobus
    template_name = 'transporte/autobus_form.html'
    fields = ['placa', 'capacidad']
    success_url = reverse_lazy('lista_buses')

class AutobusUpdateView(AdminRequiredMixin, UpdateView):
    model = Autobus
    template_name = 'transporte/autobus_form.html'
    fields = ['placa', 'capacidad']
    success_url = reverse_lazy('lista_buses')

class AutobusDeleteView(AdminRequiredMixin, DeleteView):
    model = Autobus
    template_name = 'transporte/autobus_confirm_delete.html'
    success_url = reverse_lazy('lista_buses')

# --- Ruta Views ---
class RutaListView(AdminRequiredMixin, ListView):
    model = Ruta
    template_name = 'transporte/ruta_list.html'
    context_object_name = 'rutas'

class RutaCreateView(AdminRequiredMixin, CreateView):
    model = Ruta
    template_name = 'transporte/ruta_form.html'
    fields = ['origen', 'destino', 'precio']
    success_url = reverse_lazy('lista_rutas')

class RutaUpdateView(AdminRequiredMixin, UpdateView):
    model = Ruta
    template_name = 'transporte/ruta_form.html'
    fields = ['origen', 'destino', 'precio']
    success_url = reverse_lazy('lista_rutas')

class RutaDeleteView(AdminRequiredMixin, DeleteView):
    model = Ruta
    template_name = 'transporte/ruta_confirm_delete.html'
    success_url = reverse_lazy('lista_rutas')

# --- Viaje Views ---
class ViajeListView(AdminRequiredMixin, ListView):
    model = Viaje
    template_name = 'transporte/viaje_list.html'
    context_object_name = 'viajes'
    ordering = ['-fecha_salida']

class ViajeCreateView(AdminRequiredMixin, CreateView):
    model = Viaje
    template_name = 'transporte/viaje_form.html'
    form_class = ViajeForm
    success_url = reverse_lazy('lista_viajes_admin')

class ViajeUpdateView(AdminRequiredMixin, UpdateView):
    model = Viaje
    template_name = 'transporte/viaje_form.html'
    form_class = ViajeForm
    success_url = reverse_lazy('lista_viajes_admin')

class ViajeDeleteView(AdminRequiredMixin, DeleteView):
    model = Viaje
    template_name = 'transporte/viaje_confirm_delete.html'
    success_url = reverse_lazy('lista_viajes_admin')
