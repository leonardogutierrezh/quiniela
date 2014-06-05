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


@login_required(login_url='/')
def crear_torneo(request):
    invitados_forms = formset_factory(InvitacionForm)
    if request.method == 'POST':
        formulario_invitados = invitados_forms(request.POST)
        if formulario_invitados.is_valid():
            return HttpResponseRedirect('/perfil')
        else:
            invitados_forms = formulario_invitados
    else:
        pass
    return render_to_response('social/crear_torneo.html', {'invitados_forms': invitados_forms}, context_instance=RequestContext(request))
