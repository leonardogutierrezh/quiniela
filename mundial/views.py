from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from social.models import *
from social.forms import *
from mundial.models import *

def login_acceso(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            usuario = usuario.lower()
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    print "entre aqui"
                    print acceso
                    login(request,acceso)
                    return HttpResponseRedirect('/perfil')
                else:
                    formulario = AuthenticationForm()
                    error_log = "you are not allow in my kitchen"
                    return render_to_response('login.html',{'formulario':formulario,'error_log':error_log}, context_instance=RequestContext(request))
            else:
                formulario = AuthenticationForm()
                error_log = "incorret username or password"
                return render_to_response('login.html',{'formulario':formulario,'error_log':error_log}, context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    no_login = 1
    return render_to_response('login.html',{'formulario':formulario, 'no_login': no_login}, context_instance=RequestContext(request))

def registrarse(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        formulario_email = EmailForm(request.POST)
        if formulario.is_valid() and formulario_email.is_valid():
            usuario = formulario.save()
            usuario.email = formulario_email.cleaned_data['email']
            usuario.first_name = formulario_email.cleaned_data['nombre']
            usuario.last_name = formulario_email.cleaned_data['apellido']
            usuario.save()
            usuario.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,usuario)
            return HttpResponseRedirect('/perfil')
    else:
        formulario = UserCreationForm()
        formulario_email = EmailForm()
    no_login = 1
    return render_to_response('mundial/registrarse.html', {'no_login': no_login,'formulario': formulario, 'formulario_email': formulario_email}, context_instance=RequestContext(request))

@login_required(login_url='/')
def perfil(request):
    usuario = request.user
    lista = []
    invitaciones = Invitacion.objects.filter(correo=usuario.email)
    torneo_admin = Torneo.objects.filter(administrador= request.user)
    torneos = Torneo.objects.filter(miembros__id = request.user.id )
    puntajes = Puntaje.objects.order_by('-puntaje')[:10]
    partidos = Partido.objects.exclude(ganador='N').order_by('-fecha')[:4]
    proximos = Partido.objects.filter(ganador='N').order_by('fecha')[:4]
    return render_to_response('mundial/perfil.html', {'torneos':torneos, 'torneos_admin': torneo_admin,
                                                      'usuario':usuario, 'invitaciones': invitaciones,
                                                      'puntajes': puntajes, 'partidos': partidos, 'proximos': proximos }, context_instance=RequestContext(request))


def logout_views(request):
    logout(request)
    return HttpResponseRedirect('/')

def inicio(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            print "entre al valid"
            usuario = request.POST['username']
            clave = request.POST['password']
            usuario = usuario.lower()
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                print "acceso"
                if acceso.is_active:
                    print "entre aqui"
                    print acceso
                    login(request,acceso)
                    return HttpResponseRedirect('/perfil')
                else:
                    formulario = AuthenticationForm()
                    return render_to_response('login.html',{'formulario':formulario,'error_log':error_log}, context_instance=RequestContext(request))
            else:
                formulario = AuthenticationForm()
                error_log = "incorret username or password"
                return render_to_response('login.html',{'formulario':formulario,'error_log':error_log}, context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
        formulario_email = EmailForm()

    no_login = 1
    return render_to_response('mundial/index.html', { 'no_login': no_login,
                                                     'formulario': formulario}, context_instance=RequestContext(request))

def clasificacion(request):
    grupos = Grupo.objects.all()
    lista = []
    for grupo in grupos:
        miembros = Equipo.objects.filter(grupo=grupo).order_by('-puntos','golesF')
        tupla = (grupo,miembros)
        lista.append(tupla)
    return render_to_response('mundial/clasificacion.html', {'grupos': lista}, context_instance=RequestContext(request))