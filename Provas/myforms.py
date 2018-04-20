# -*- coding: utf-8 -*-

__author__ = 'sachetto'

from django import forms
from models import Disciplina, Curso, DIFICULDADES
from django.contrib.admin import widgets

#VERY UGLY HACKKKKKKKKKKKK!!!!!!!!!!!!!!
def monkey_patch(_):
    return True

class CriaProvaAleatoriaForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    disciplina = forms.ChoiceField(choices=(("","Escolha um Curso"),))
    disciplina.valid_value = monkey_patch
    numero_prova = forms.IntegerField(label='Prova', min_value=1)
    valor_prova = forms.IntegerField(label='Valor da prova', min_value=1)
    data_aplicacao = forms.DateField(label="Data da aplicação", widget=widgets.AdminDateWidget)
    numero_questoes = forms.IntegerField(label='Numero de questões', min_value=1)
    numero_faceis = forms.IntegerField(initial = 0, required=False, label='Número de questões faceis', min_value=0, )
    numero_medias = forms.IntegerField(initial = 0, required=False, label='Número de questões medias', min_value=0)
    numero_dificeis = forms.IntegerField(initial = 0, required=False, label='Número de questões dificeis', min_value=0)
    data_aplicacao = forms.DateField(label="Data da aplicação", widget=widgets.AdminDateWidget)

class CriaProvaVaziaForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    #disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all())
    disciplina = forms.ChoiceField(choices=(("","Escolha um Curso"),))
    disciplina.valid_value = monkey_patch
    numero_prova = forms.IntegerField(label='Prova', min_value=1)
    valor_prova = forms.IntegerField(label='Valor da prova', min_value=1)
    data_aplicacao = forms.DateField(label="Data da aplicação", widget=widgets.AdminDateWidget)

class FiltraProvaForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    #disciplina = forms.ModelChoiceField(label='Disc.', queryset=Disciplina.objects.all())
    disciplina = forms.ChoiceField(choices=(("","Escolha um Curso"),))
    disciplina.valid_value = monkey_patch


class FiltraQuestaoForm(forms.Form):
    choices = ((4, u"Mostrar todas"),) + DIFICULDADES
    dificuldade = forms.ChoiceField(choices=choices)

class AdicionaNovaQuestaoForm(forms.Form):
    disciplinas = forms.ModelMultipleChoiceField(label='Disciplinas', queryset=Disciplina.objects.all())
    assunto = forms.CharField(label="Assunto")
    #talvez irei tirar essa campo
    numero_prova = forms.IntegerField(label='Prova', min_value=1)
    enunciado = forms.CharField(label='Enunciado', widget=forms.Textarea)
    choices = ((4, u"Mostrar todas"),) + DIFICULDADES
    dificuldade = forms.ChoiceField(choices=choices)
    valor_sugerido = forms.DecimalField(max_digits=10, decimal_places=2)
    resposta = forms.CharField(label='Resposta', widget=forms.Textarea)
