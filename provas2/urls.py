from django.conf.urls import patterns, include, url
from Provas.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^provas/', include('provas.foo.urls')),
    (r'^$', index),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', logout_view),

    (r'^prova_aleatoria/', prova_aleatoria),
    (r'^prova_vazia/', prova_vazia),
    (r'^nova_questao/', nova_questao),
    url(r'^provas/', visualizar_provas, name="visualiza_form"),
    (r'^prova/del/(?P<prova_id>\d+)/$', remove_prova),
    (r'^prova/(?P<prova_id>\d+)/$', mostra_prova),
    (r'^disciplinas/(?P<curso_id>\d+)/$', carrega_disciplinas),
    (r'^questoes/(?P<prova_id>\d+)/(?P<questao_id>[-+]?\d+)/$', mostra_questoes),
    (r'^questoes/del/(?P<prova_id>\d+)/(?P<questao_id>\d+)/$', remove_questao),
    (r'^questoes/add/(?P<prova_id>\d+)/$', adiciona_questoes),
    (r'^modifica_prova/(?P<prova_id>\d+)/(?P<questao_id>[-+]?\d+)/(?P<nova_questao_id>\d+)/(?P<questao_valor>\d+\.\d{2})$', modifica_prova),
    (r'^baixar_fonte/(?P<prova_id>\d+)/$', baixar_fonte),
    (r'^baixar_fonte_gabarito/(?P<prova_id>\d+)/$', baixar_fonte_gabarito),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^fontes/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),


    (r'^media/(.*)', 'django.views.static.serve', {'document_root' : settings.ADMIN_MEDIA_ROOT, 'show_indexes' : True}),
)

