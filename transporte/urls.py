from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_viajes, name='lista_viajes'),
    path('viaje/<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
    path('viaje/<int:viaje_id>/reservar/', views.reservar_boleto, name='reservar_boleto'),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro_cliente, name='registro'),
    
    # Client Portal
    path('mis-boletos/', views.mis_boletos, name='mis_boletos'),
    path('boleto/<int:boleto_id>/imprimir/', views.imprimir_boleto, name='imprimir_boleto'),

    # Admin Dashboard & Autobus CRUD
    path('panel/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('panel/buses/', views.AutobusListView.as_view(), name='lista_buses'),
    path('panel/buses/nuevo/', views.AutobusCreateView.as_view(), name='crear_bus'),
    path('panel/buses/<int:pk>/editar/', views.AutobusUpdateView.as_view(), name='editar_bus'),
    path('panel/buses/<int:pk>/eliminar/', views.AutobusDeleteView.as_view(), name='eliminar_bus'),

    # Ruta CRUD
    path('panel/rutas/', views.RutaListView.as_view(), name='lista_rutas'),
    path('panel/rutas/nueva/', views.RutaCreateView.as_view(), name='crear_ruta'),
    path('panel/rutas/<int:pk>/editar/', views.RutaUpdateView.as_view(), name='editar_ruta'),
    path('panel/rutas/<int:pk>/eliminar/', views.RutaDeleteView.as_view(), name='eliminar_ruta'),

    # Viaje CRUD
    path('panel/viajes/', views.ViajeListView.as_view(), name='lista_viajes_admin'),
    path('panel/viajes/nuevo/', views.ViajeCreateView.as_view(), name='crear_viaje'),
    path('panel/viajes/<int:pk>/editar/', views.ViajeUpdateView.as_view(), name='editar_viaje'),
    path('panel/viajes/<int:pk>/eliminar/', views.ViajeDeleteView.as_view(), name='eliminar_viaje'),
]
