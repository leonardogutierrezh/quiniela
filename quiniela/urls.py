from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quiniela.views.home', name='home'),
    # url(r'^quiniela/', include('quiniela.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'mundial.views.login_acceso'),
    url(r'^perfil/$', 'mundial.views.perfil'),
    url(r'^registrarse/$', 'mundial.views.registrarse'),
    url(r'^crear_torneo/$', 'social.views.crear_torneo'),
)
