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
from django.forms.formsets import formset_factory
import time
from django.core.mail import EmailMessage, EmailMultiAlternatives

def resultados_grupo(request, id_grupo):
    grupo = Grupo.objects.get(id=id_grupo)
    locales = Equipo.objects.filter(grupo=grupo)
    partidos = Partido.objects.filter(equipoL__id__in=locales)
    for partido in partidos:
        print str(partido.equipoL) + " " + str(partido.equipoV)
    return render_to_response('apuesta/resultados_grupo.html', {'partidos':partidos}, context_instance=RequestContext(request))