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
from django.forms.formsets import formset_factory
import time
from django.core.mail import EmailMessage, EmailMultiAlternatives


@login_required(login_url='/')
def crear_torneo(request):
    invitados_forms = formset_factory(InvitacionForm, can_delete = True, extra = 1)
    if request.method == 'POST':
        formulario = TorneoForm(request.POST)
        formulario_invitados = invitados_forms(request.POST)
        if formulario_invitados.is_valid() and formulario.is_valid():
            torneo = Torneo.objects.create(nombre=formulario.cleaned_data['nombre'], administrador=request.user)
            for invitado in formulario_invitados:
                if not invitado.cleaned_data['DELETE']:
                    email = invitado.cleaned_data['email']
                    hash =str(torneo.id) + str(time.time()).split('.')[0] + email
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