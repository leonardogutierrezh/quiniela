from django.conf.urls import patterns, include, url
from quiniela import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quiniela.views.home', name='home'),
    # url(r'^quiniela/', include('quiniela.foo.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'mundial.views.login_acceso'),
    url(r'^perfil/$', 'mundial.views.perfil'),
    url(r'^$', 'mundial.views.inicio'),
    url(r'^registrarse/$', 'mundial.views.registrarse'),
    url(r'^crear_torneo/$', 'social.views.crear_torneo'),
    url(r'^enviar_invitaciones/$', 'social.views.enviar_invitaciones'),
    url(r'^invitacion/(?P<invitacion>[\w|\W]+)/$', 'social.views.invitacion'),
    url(r'^ver_torneo/(?P<id_torneo>\d+)/$', 'social.views.ver_torneo'),
    url(r'mi_quiniela/$', 'social.views.mi_quiniela'),
    url(r'^poner_resultados/(?P<id_grupo>\d+)/$', 'apuesta.views.resultados_grupo'),
    url(r'^calcular_puntos/$', 'apuesta.views.calcular_puntos_grupos'),
    url(r'^clasificacion/$', 'mundial.views.clasificacion'),
    url(r'^logout/$', 'mundial.views.logout_views'),
    url(r'^email_autocomplete', 'social.views.email_autocomplete'),
    url(r'^rechazar/(?P<id_torneo>\d+)/$', 'social.views.rechazar_invitacion'),
    url(r'editar_torneo/(?P<id_torneo>\d+)/$', 'social.views.editar_torneo'),
    url(r'^compartir_quiniela/(?P<id_user>\d+)/$', 'social.views.compartir_quiniela'),
    url(r'^accounts/', include('allauth.urls'))
)
