# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import Prova, Questao, Disciplina, Curso
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.core import serializers
#from django.utils import simplejson
from django.db.models import Count


import json as simplejson


import helpers
from myforms import CriaProvaAleatoriaForm, CriaProvaVaziaForm, FiltraProvaForm, AdicionaNovaQuestaoForm
from myforms import FiltraQuestaoForm

@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required()
def index(request):

    q_faceis = len(Questao.objects.filter(dificuldade=1))
    q_medias = len(Questao.objects.filter(dificuldade=2))
    q_dificeis = len(Questao.objects.filter(dificuldade=3))

    classificada_f = 'Classificadas'
    classificada_m = 'Classificadas'
    classificada_d = 'Classificadas'

    if q_faceis == 1:
        classificada_f = 'Classificada'

    if q_medias == 1:
        classificada_m = 'Classificada'

    if q_dificeis == 1:
        classificada_d = 'Classificada'

    total = q_faceis + q_medias + q_dificeis

    questoes = Questao.objects.all()

    questoes_por_disciplina = {}

    faceis_por_disciplina = {}
    medias_por_disciplina = {}
    dificies_por_disciplina = {}

    for q in questoes:
        discs = q.disciplinas.all().order_by('nome')
        for d in discs:
            curso = Curso.objects.get(disciplina = d)
            chave = (d.nome, curso.nome)
            questoes_por_disciplina[chave] = questoes_por_disciplina.get(chave,0) + 1

            if d.nome not in faceis_por_disciplina:
                    faceis_por_disciplina[d.nome] = 0
            if d.nome not in medias_por_disciplina:
                    medias_por_disciplina[d.nome] = 0
            if d.nome not in dificies_por_disciplina:
                    dificies_por_disciplina[d.nome] = 0

            if q.dificuldade == 1:
                faceis_por_disciplina[d.nome] = faceis_por_disciplina.get(d.nome,0) + 1
            elif q.dificuldade == 2:
                medias_por_disciplina[d.nome] = medias_por_disciplina.get(d.nome,0) + 1
            elif q.dificuldade == 3:
                dificies_por_disciplina[d.nome] = dificies_por_disciplina.get(d.nome,0) + 1

    cursos = Curso.objects.all()

    data = {}
    data['user'] = request.user
    data['total'] = total
    data['faceis'] = q_faceis
    data['medias'] = q_medias
    data['dificeis'] = q_dificeis
    data['classificada_f'] = classificada_f
    data['classificada_m'] = classificada_m
    data['classificada_d'] = classificada_d
    data['disciplinas'] = questoes_por_disciplina
    data['faceis_por_d'] = faceis_por_disciplina
    data['medias_por_d'] = medias_por_disciplina
    data['dificies_por_d'] = dificies_por_disciplina

    data['cursos'] = cursos

    return render_to_response('index.html', data)

@login_required()
def prova_vazia(request):
    def errorHandle(error, data):
        form = CriaProvaVaziaForm(data)
        return render_to_response('form_prova_vazia.html', { 'error' : error, 'form' : form },
                                  context_instance=RequestContext(request))

    if request.method == 'POST':

        form = CriaProvaVaziaForm(request.POST)

        if form.is_valid():
            disciplina = Disciplina.objects.get(pk=int(form.cleaned_data["disciplina"]))
            numero_prova =  form.cleaned_data["numero_prova"]
            valor = form.cleaned_data["valor_prova"]
            data_aplicacao =  form.cleaned_data["data_aplicacao"]
            curso = form.cleaned_data["curso"]

            p = helpers.cria_prova_vazia(disciplina, numero_prova,
                                              valor, data_aplicacao,
                                              curso)

            return HttpResponseRedirect("/prova/%d" % (p.pk))
        else:
            error = u'Campos inválidos'
            return errorHandle(error, request.POST)

    else:
        form = CriaProvaVaziaForm()
        return render_to_response('form_prova_vazia.html', { 'form': form, },
                                  context_instance=RequestContext(request))

@login_required()
def nova_questao(request):
    def errorHandle(error, data):
        form = AdicionaNovaQuestaoForm(data)
        return render_to_response('form_nova_questao.html', {'error': error, 'form': form},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':

        form = AdicionaNovaQuestaoForm(request.POST)

        if form.is_valid():

            lista_disciplinas = form.cleaned_data["disciplinas"]
            assunto = form.cleaned_data["assunto"]
            enunciado = form.cleaned_data["enunciado"]
            dificuldade = form.cleaned_data["dificuldade"]
            valor = form.cleaned_data["valor_sugerido"]

            disciplinas = Disciplina.objects.filter(pk__in=lista_disciplinas)
            numero_prova = form.cleaned_data["numero_prova"]

            p = helpers.cria_nova_questao(assunto, numero_prova, enunciado,
                                         disciplinas, valor, dificuldade)

            #return HttpResponseRedirect("/prova/%d" % (p.pk))
            if('_save' in request.POST):
                return HttpResponse('<script type="text/javascript">window.close();</script>')
            elif('_addmore' in request.POST):
                return HttpResponseRedirect("/nova_questao/")
        else:
            error = u'Campos inválidos'
            return errorHandle(error, request.POST)

    else:
        form = AdicionaNovaQuestaoForm()
        return render_to_response('form_nova_questao.html', {'form': form, },
                          context_instance=RequestContext(request))

@login_required()
def prova_aleatoria(request):
    def errorHandle(error, data):
        form = CriaProvaAleatoriaForm(data)
        return render_to_response('form_prova_aleatoria.html', { 'error' : error, 'form' : form },
                                  context_instance=RequestContext(request))

    if request.method == 'POST':

        form = CriaProvaAleatoriaForm(request.POST)

        if form.is_valid():
            disciplina = Disciplina.objects.get(pk=int(form.cleaned_data["disciplina"]))
            numero_questoes = form.cleaned_data["numero_questoes"]
            questoes_faceis = form.cleaned_data["numero_faceis"]
            questoes_medias = form.cleaned_data["numero_medias"]
            questoes_dificeis = form.cleaned_data["numero_dificeis"]
            numero_prova =  form.cleaned_data["numero_prova"]
            valor = form.cleaned_data["valor_prova"]
            data_aplicacao =  form.cleaned_data["data_aplicacao"]
            curso = form.cleaned_data["curso"]

            p, msg = helpers.cria_prova_aleatoria(disciplina, numero_prova, numero_questoes,
                                   questoes_faceis, questoes_medias,
                                   questoes_dificeis, valor, data_aplicacao,
                                   curso)

            if p is None:
                return errorHandle(msg, request.POST)

            return HttpResponseRedirect("/prova/%d" % (p.pk))
        else:
            error = u'Campos inválidos'
            return errorHandle(error, request.POST)

    else:
        form = CriaProvaAleatoriaForm()
        return render_to_response('form_prova_aleatoria.html', { 'form': form, },
                                  context_instance=RequestContext(request))

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@login_required()
def mostra_prova(_, prova_id):
    try:
        print prova_id
        prova = Prova.objects.get(pk=prova_id)
        questoes = []
        count = 0

        for index in prova.ordem_questoes:
            q = prova.questoes.get(pk=int(index))
            q.valor_sugerido = prova.valores_questoes[count]
            count += 1

            questoes.append(q)


    except Prova.DoesNotExist:
        raise Http404

    return render_to_response('prova.html', {'prova': prova, 'questoes': questoes})



import json

@login_required()
def atualiza_valor_questao(request):

    if request.is_ajax():
        if request.method == 'POST':

            data = json.loads(request.body)
            id_prova = data['id_prova']
            id_questao = int(data['id_questao'])
            valor = float(data['valor_questao'])

            prova = Prova.objects.get(pk=id_prova)

            indice_questao = prova.ordem_questoes.index(unicode(id_questao))
            prova.valores_questoes[indice_questao] = valor
            try:
                prova.save()
                return HttpResponse("OK")
            except:
                return HttpResponse("ERROR")


    else:
        raise Http404



@login_required()
def mostra_questoes(request, prova_id, questao_id):
    try:
        prova = Prova.objects.get(pk=prova_id)
        todas_questoes = prova.questoes.all()

        excluir_pks = []

        for q in todas_questoes:
            excluir_pks.append(q.pk)

        if request.method == "POST":
            form = FiltraQuestaoForm(request.POST)

            if form.is_valid():
                dif = int(form.cleaned_data["dificuldade"])
                if dif == 4:
                    questoes = Questao.objects.filter(disciplinas__in=[prova.disciplina]).exclude(pk__in=excluir_pks).order_by("dificuldade")
                else:
                    questoes = Questao.objects.filter(disciplinas__in=[prova.disciplina], dificuldade=dif).exclude(pk__in=excluir_pks).order_by("dificuldade")

            data = serializers.serialize('json', questoes)
            return HttpResponse(data)

        else:
            form = FiltraQuestaoForm()
            questoes = Questao.objects.filter(disciplinas__in=[prova.disciplina]).exclude(pk__in=excluir_pks).order_by("dificuldade")

            return render_to_response('questoes.html', {'questoes': questoes,
                                                    'prova_id': prova_id,
                                                    'questao_id': questao_id,
                                                    'form': form },
                                  context_instance=RequestContext(request))


    except Prova.DoesNotExist:
        raise Http404


@login_required()
def adiciona_questoes(request, prova_id):

    return mostra_questoes(request, prova_id, -1)

@login_required()
def modifica_prova(_, prova_id, questao_id, nova_questao_id):
    try:
        prova = Prova.objects.get(pk=prova_id)
        questao_nova = Questao.objects.get(pk=nova_questao_id)

        if int(questao_id) > -1:
            questao_antiga = Questao.objects.get(pk=questao_id)
            prova.questoes.remove(questao_antiga)

            indice_questao_antiga = prova.ordem_questoes.index(questao_id)
            prova.ordem_questoes[indice_questao_antiga] = nova_questao_id
            prova.valores_questoes[indice_questao_antiga] = float(questao_nova.valor_sugerido)

        else:
            prova.num_questoes = prova.num_questoes + 1
            prova.ordem_questoes.append(nova_questao_id)
            prova.valores_questoes.append(float(questao_nova.valor_sugerido))


        prova.questoes.add(questao_nova)
        prova.save()

    except Prova.DoesNotExist:
        raise Http404

    return render_to_response('prova_modificada.html')

@login_required()
def remove_questao(_, prova_id, questao_id):
    try:
        prova = Prova.objects.get(pk=prova_id)
        questao_antiga = Questao.objects.get(pk=questao_id)
        prova.questoes.remove(questao_antiga)

        indice_questao_antiga = prova.ordem_questoes.index(questao_id)
        del prova.ordem_questoes[indice_questao_antiga]
        del prova.valores_questoes[indice_questao_antiga]

        prova.num_questoes = prova.num_questoes - 1
        prova.save()

    except Prova.DoesNotExist:
        raise Http404

    return HttpResponseRedirect("/prova/%s" % (prova_id ))

@login_required()
def remove_prova(_, prova_id):
    try:
        prova = Prova.objects.get(pk=prova_id)
        prova.delete()

    except Prova.DoesNotExist:
        raise Http404

    return HttpResponseRedirect("/provas/%s" % (prova_id ))

@login_required()
def baixar_fonte(_, prova_id):
    try:
        prova = Prova.objects.get(pk=prova_id)

        fonte_prova = helpers.gera_latex(prova, False)

        return redirect('/fontes/%s' % fonte_prova)

    except Prova.DoesNotExist:
        raise Http404
        

@login_required()
def baixar_fonte_gabarito(_, prova_id):
    try:
        prova = Prova.objects.get(pk=prova_id)

        fonte_prova = helpers.gera_latex(prova, True)

        return redirect('/fontes/%s' % fonte_prova)

    except Prova.DoesNotExist:
        raise Http404


@login_required()
def visualizar_provas(request):

    disciplina = ''
    curso = ''

    try:
        if request.method == 'POST':
            form =  FiltraProvaForm(request.POST)

            if form.is_valid():
                disciplina = form.cleaned_data["disciplina"]
                curso = form.cleaned_data["curso"]
                provas = Prova.objects.filter(disciplina=disciplina, curso=curso)
            else:
                if "curso" in form.errors:
                    if "disciplina" not in form.errors:
                        disciplina = request.POST["disciplina"]
                        d = Disciplina.objects.filter(pk=disciplina)
                        provas = Prova.objects.filter(disciplina=d)
                    else:
                        provas = Prova.objects.all()
                else:
                    curso = request.POST["curso"]
                    c = Curso.objects.filter(pk=curso)
                    provas = Prova.objects.filter(curso=c)

            data = []
            for p in provas:
                data.append({"pk":p.pk, "prova":str(p)})

            return HttpResponse(simplejson.dumps(data), mimetype='application/javascript')

        else:
            form =  FiltraProvaForm()
            provas = Prova.objects.all()
            return render_to_response('provas.html', {'provas':provas, 'form':form},
                                  context_instance=RequestContext(request))

    except Prova.DoesNotExist:
        raise Http404



@login_required()
def carrega_disciplinas(_, curso_id):

    curso = Curso.objects.get(pk=curso_id)
    disciplinas = Disciplina.objects.filter(curso=curso)
    data = serializers.serialize('json', disciplinas)
    return HttpResponse(data)

