# -*- coding: utf-8 -*-
from django.db import models
import ast
import time
# Create your models here.

DIFICULDADES = (
    (1, 'Fácil'),
    (2, 'Média'),
    (3, 'Difícil')
)

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Curso(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)

class Disciplina(models.Model):
    curso = models.ForeignKey(Curso)
    nome = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.nome

class Questao(models.Model):
    assunto  = models.CharField(max_length=30)
    numero_prova = models.IntegerField()
    enunciado = models.TextField()
    dificuldade = models.IntegerField(choices=DIFICULDADES)
    disciplinas = models.ManyToManyField(Disciplina)
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    resposta = models.TextField()

    class Meta:
        verbose_name_plural = "Questões"
        ordering = ("dificuldade",)

    def __unicode__(self):
        return "Assunto: %s, Dificuldade %s, Prova: %s" % \
        (self.assunto, self.dificuldade, self.numero_prova)

        # This should touch before saving

    # def save(self, *args, **kwargs):
    #     import textwrap
    #
    #     self.enunciado = textwrap.fill(self.enunciado, 50)
    #     self.resposta = textwrap.fill(self.resposta, 50)
    #     super(Questao, self).save(*args, **kwargs)


class Prova(models.Model):

    data_aplicacao = models.DateField()
    questoes = models.ManyToManyField(Questao)
    disciplina = models.ForeignKey(Disciplina)
    numero_prova = models.IntegerField()
    valor = models.IntegerField()
    curso = models.ForeignKey(Curso)
    ordem_questoes = ListField()
    valores_questoes = ListField()
    num_questoes = models.IntegerField(default=0)


    def __unicode__(self):
        data_certa = time.strptime(str(self.data_aplicacao),"%Y-%m-%d")
        return "%s: Prova %d - %s - %d pontos" % \
               (unicode(self.disciplina), self.numero_prova,
                time.strftime("%d-%m-%Y", data_certa),
                self.valor)