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
    #puntaje =
    torneos = Torneo.objects.filter()
    return render_to_response('mundial/perfil.html', {'torneos':torneos, 'usuario':usuario}, context_instance=RequestContext(request))


def logout_views(request):
    logout(request)
    return HttpResponseRedirect('/')

def inicio(request):
    puntajes = Puntaje.objects.order_by('-puntaje')[:10]
    partidos = Partido.objects.exclude(ganador='N').order_by('-fecha')
    for partido in partidos:
        print partido.fecha
    no_login = 1
    return render_to_response('mundial/index.html', {'puntajes': puntajes, 'partidos': partidos, 'no_login': no_login}, context_instance=RequestContext(request))
