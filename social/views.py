from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from social.models import *
from mundial.models import *
from social.forms import *
from apuesta.models import Apuesta
from django.forms.formsets import formset_factory
import time, json
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Q


@login_required(login_url='/')
def crear_torneo(request):
    invitados_forms = formset_factory(InvitacionForm, can_delete = True, extra = 0)
    if request.method == 'POST':
        formulario = TorneoForm(request.POST)
        formulario_invitados = invitados_forms(request.POST)
        if formulario_invitados.is_valid() and formulario.is_valid():
            torneo = Torneo.objects.create(nombre=formulario.cleaned_data['nombre'], administrador=request.user)
            for invitado in formulario_invitados:
                if not invitado.cleaned_data['DELETE']:
                    email = invitado.cleaned_data['email']
                    hash =str(torneo.id) + str(time.time()).split('.')[0] + email
                    if not(Invitado.objects.filter(correo=email, torneo=torneo)) and not(Invitado.objects.filter()):
                        Invitacion.objects.create(correo=email, torneo=torneo, hash=hash, estado='N')
                print invitado.cleaned_data['email']
                print invitado.cleaned_data['DELETE']
            return HttpResponseRedirect('/perfil')
        else:
            invitados_forms = formulario_invitados
    else:
        formulario = TorneoForm()
    return render_to_response('social/crear_torneo.html', {'invitados_forms': invitados_forms, 'formulario': formulario}, context_instance=RequestContext(request))

def editar_torneo(request, id_torneo):
    torneo = Torneo.objects.get(id=id_torneo)
    factory = formset_factory(InvitacionForm, can_delete = True, extra = 0)

    invitados_forms = factory(queryset=torneo.miembros.all())

    if request.method == 'POST':
        formulario = TorneoForm(request.POST)
        formulario_invitados = invitados_forms(request.POST)
        if formulario_invitados.is_valid() and formulario.is_valid():
            torneo.nombre = nombre=formulario.cleaned_data['nombre']
            torneo.administrador = request.user
            torneo.save()
            for invitado in formulario_invitados:
                if not invitado.cleaned_data['DELETE']:
                    email = invitado.cleaned_data['email']
                    hash =str(torneo.id) + str(time.time()).split('.')[0] + email
                    if not(Invitado.objects.filter(correo=email, torneo=torneo)) and not(Invitado.objects.filter()):
                        Invitacion.objects.create(correo=email, torneo=torneo, hash=hash, estado='N')
                print invitado.cleaned_data['email']
                print invitado.cleaned_data['DELETE']
            return HttpResponseRedirect('/perfil')
        else:
            invitados_forms = formulario_invitados
    else:
        formulario = TorneoForm()
    return render_to_response('social/crear_torneo.html', {'invitados_forms': invitados_forms, 'formulario': formulario}, context_instance=RequestContext(request))


def enviar_invitaciones(request):
    invitaciones = Invitacion.objects.filter(estado='N')
    for invitacion in invitaciones:
        asunto = "Invitacion de quiniela"
        mensaje = "tu amigo" + invitacion.torneo.administrador.first_name + " " +invitacion.torneo.administrador.first_name
        mensaje = mensaje + " te ha invitado a jugar una quiniela para el mundial 2014\n"
        mensaje = mensaje + "entra aqui para jugar: localhost:8000/invitacion/" + invitacion.hash + " \n"
        #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
        correo = EmailMessage(asunto, mensaje, to=[invitacion.correo])
        try:
            print "enviando"
            correo.send()
            invitacion.estado = "E"
            invitacion.save()
        except:
            pass
    return HttpResponseRedirect("/")

def invitacion(request,invitacion):
    invitacion = Invitacion.objects.get(hash=invitacion)
    if request.method == "POST":
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
            login(request,usuario)
            invitacion.torneo.miembros.add(usuario)
            invitacion.delete()
            return HttpResponseRedirect('/perfil')
    else:
        if User.objects.filter(email=invitacion.correo):
            usuario = User.objects.get(email=invitacion.correo)
            usuario.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,usuario)
            invitacion.torneo.miembros.add(usuario)
            invitacion.delete()
            return HttpResponseRedirect("/perfil")
        formulario = UserCreationForm()
        formulario_email = EmailForm(initial={'email': invitacion.correo})
    no_login = 1
    return render_to_response('social/registrarse_invitado.html', {'formulario':formulario,
                                                                   'formulario_email':formulario_email, 'no_login': no_login}, context_instance=RequestContext(request))
@login_required(login_url='/')
def mi_quiniela(request):
    grupos = Grupo.objects.all()
    lista = []
    for grupo in grupos:
        apuestas = Apuesta.objects.filter(partido__equipoL__grupo = grupo, usuario=request.user)
        tupla = (grupo,apuestas)
        lista.append(tupla)
    return render_to_response('social/mi_quiniela.html', {'grupos': lista}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_torneo(request,id_torneo):
    torneo = Torneo.objects.get(id=id_torneo)
    if Puntaje.objects.filter(usuario=torneo.administrador):
        tupla_admin = (torneo.administrador, Puntaje.objects.get(usuario=torneo.administrador).puntaje)
    else:
        tupla_admin = (torneo.administrador,0)
    lista = []
    lista.append(tupla_admin)
    participantes = torneo.miembros.all()
    for participante in participantes:
        if Puntaje.objects.filter(usuario=participante):
            tupla = (participante, Puntaje.objects.get(usuario=participante).puntaje)
        else:
            tupla = (participante,0)
        lista.append(tupla)
    ordenados = sorted(lista, key=lambda tupla: tupla[1])
    ordenados_mayor = ordenados[:: -1]
    print ordenados_mayor
    return render_to_response('social/ver_torneo.html', {'participantes':ordenados_mayor, 'torneo': torneo}, context_instance=RequestContext(request))

@login_required(login_url='/')
def email_autocomplete(request):
   term = request.GET['q']

   users = User.objects.filter(Q(first_name__contains = term) | Q(last_name__contains = term) | Q(email__contains = term) | Q(username__contains = term))

   opciones  = []
   for user in users:
       opciones.append({
           'nombre'    : user.first_name,
           'apellido'  : user.last_name,
           'email'     : user.email,
           'username'  : user.username,
       })

   return HttpResponse(json.dumps(opciones) , mimetype= 'application/json')

@login_required(login_url='/')
def rechazar_invitacion(request, id_torneo):
    Invitacion.objects.get(correo=request.user.email, torneo=Torneo.objects.get(id=id_torneo)).delete()
    return HttpResponseRedirect('/perfil')