__author__ = 'sachetto'

from models import Disciplina, Questao, Prova, Curso
from django.contrib import admin

class QuestaoAdmin(admin.ModelAdmin):
    list_filter = ('disciplinas',)

admin.site.register(Disciplina)
admin.site.register(Questao, QuestaoAdmin)
admin.site.register(Prova)
admin.site.register(Curso)
