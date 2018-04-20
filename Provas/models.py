# -*- coding: utf-8 -*-
from django.db import models
import time
# Create your models here.

DIFICULDADES = (
    (1, 'Fácil'),
    (2, 'Média'),
    (3, 'Difícil')
)

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


class Prova(models.Model):

    data_aplicacao = models.DateField()
    questoes = models.ManyToManyField(Questao)
    disciplina = models.ForeignKey(Disciplina)
    numero_prova = models.IntegerField()
    valor = models.IntegerField()
    curso = models.ForeignKey(Curso)

    def __unicode__(self):
        data_certa = time.strptime(str(self.data_aplicacao),"%Y-%m-%d")

        return "%s: Prova %d - %s - %d pontos" % \
               (self.disciplina, self.numero_prova,
                time.strftime("%d-%m-%Y", data_certa),
                self.valor)

