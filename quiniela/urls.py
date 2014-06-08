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
    url(r'^registrarse/$', 'mundial.views.registrarse'),
    url(r'^crear_torneo/$', 'social.views.crear_torneo'),
    url(r'^enviar_invitaciones/$', 'social.views.enviar_invitaciones'),
    url(r'^invitacion/(?P<invitacion>[\w|\W]+)/$', 'social.views.invitacion'),
    url(r'^ver_torneo/(?P<id_torneo>\d+)/$', 'social.views.ver_torneo'),
    url(r'mi_quiniela/$', 'social.views.mi_quiniela'),
    url(r'^poner_resultados/(?P<id_grupo>\d+)/$', 'apuesta.views.resultados_grupo'),
    url(r'^calcular_puntos/$', 'apuesta.views.calcular_puntos_grupos'),
    url(r'^logout/$', 'mundial.views.logout_views'),
)
