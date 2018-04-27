# -*- coding: utf-8 -*-
__author__ = 'sachetto'

from models import Prova, Questao
import time, random
import codecs

CABECALHO=r"""
\documentclass{article}

%%---------------------------------------------------------------------
%% New Commands
%%---------------------------------------------------------------------
\input{cmd.tex}
\newcommand{\PathImg}{../../../img}

\newcommand{\tc}[2]{\textcolor{#1}{#2}}
\newcommand{\arrowrounded}{\ding{220}}

%--- Description environment:: \begin{descvar} \item \end{descvar}
%---   The first line of each list's item is not indented.
%---   The followings are indented by #1
\newlength{\aux}
\newlength{\auxb}
\newenvironment{descvar}[2]{
\begin{list}{#1}{\settowidth{\aux}{\LARGE #1}
                 \setlength{\auxb}{\aux}
                 \addtolength{\auxb}{4pt}
                 \partopsep 0.0in
                 \itemsep 0.0in
                 \parsep #2\baselineskip
                 \leftmargin\auxb
                 \listparindent \parindent
                 \itemindent -\auxb
                 \addtolength{\itemindent}{\labelsep}
                 \labelwidth 0.0in}}{\end{list}}

\newcommand{\thus}{.\hspace*{.1ex}\raisebox{1.2ex}{.}\hspace*{.1ex}.}

\def\setvarlen#1{%%
  \settowidth{\varlen}{#1}
}

%%---------------------------------------------------------------------
%% LaTeX Packages
%%---------------------------------------------------------------------
\usepackage{latexsym}
\usepackage{shadow}
\usepackage{pifont}
\usepackage{graphicx}
\usepackage[latin1]{inputenc}
\usepackage[brazil]{babel}
\usepackage{comment}
\usepackage{listings}
\usepackage{boxit}
\usepackage[Algoritmo]{algorithm}
\usepackage[]{algpseudocode}

%%---------------------------------------------------------------------
%% New Settings
%%---------------------------------------------------------------------
\newcommand{\mx}[1]{\makebox[\varlen]{#1}}
\def\margintype{\AFULLX}
\Margins %%
\sloppy %%


%%---------------------------------------------------------------------
\begin{document}
% \begin{scriptsize}
\MITBox
  {\thexvalue}
  {15}
  {UFSJ}
"""


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    matrix = [[0.0 for x in range(size_x)] for y in range(size_y)]

    for x in xrange(size_x):
        matrix [x][0] = x
    for y in xrange(size_y):
        matrix [0][y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1],
                    matrix[x][y-1] + 1
                )
            else:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1] + 1,
                    matrix[x][y-1] + 1
                )

    return matrix[size_x - 1][size_y - 1]


def cria_prova_vazia(disciplina, numero_prova, valor, data_aplicacao, curso):

    prova = Prova()

    prova.numero_prova = numero_prova
    prova.valor = valor
    prova.data_aplicacao = data_aplicacao
    prova.disciplina = disciplina
    prova.curso = curso
    prova.ordem_questoes = []

    prova.save()

    return prova


def cria_nova_questao(assunto, numero_prova, enunciado, disciplinas, valor, dificuldade):

    questao = Questao()
    questao.assunto = assunto
    questao.numero_prova = numero_prova
    questao.enunciado = enunciado
    questao.valor_sugerido = valor
    questao.dificuldade = dificuldade

    questao.save()

    for d in disciplinas:
        questao.disciplinas.add(d)

    return questao

def cria_prova_aleatoria(disciplina, numero_prova, numero_questoes, 
                              questoes_faceis, questoes_medias, 
                              questoes_dificeis, valor, data_aplicacao, curso):


    total = questoes_dificeis + questoes_faceis + questoes_medias
    if  total > numero_questoes:
        error = u'Número inválido de questões.'
        return None, error

    p = Prova()

    p.numero_prova = numero_prova
    p.valor = valor
    p.data_aplicacao = data_aplicacao
    p.disciplina = disciplina
    p.curso = curso

    questoes = []

    p.save()

    random.seed()

    i = 0
    faceis = Questao.objects.filter(dificuldade=1, 
                                    disciplinas__in=[disciplina], 
                                    numero_prova=numero_prova)

    if len(faceis) <  questoes_faceis:
        p.delete()
        return (None,
                u"Você não possui questões suficientes de nível fácil na base de dados. \n"
                u"Questões solicitadas: %d\n Questões disponíveis: %d" % (questoes_faceis, len(faceis)) )

    while i  < questoes_faceis:
        q = random.choice(faceis)
        if q not in questoes:
            questoes.append(q)
            i = i + 1

    i = 0
    medias = Questao.objects.filter(dificuldade=2, 
                                    disciplinas__in=[disciplina], 
                                    numero_prova=numero_prova)

    if len(medias) <  questoes_medias:
        p.delete()
        return (None,
                "Você não possui questões suficientes de nível fácil na base de dados. \n"
                "Questões solicitadas: %d\n Questões disponíveis: %d" % (questoes_medias, len(medias)) )
    while i  < questoes_medias:
        q = random.choice(medias)
        if q not in questoes:
            questoes.append(q)
            i = i + 1

    i = 0
    dificeis = Questao.objects.filter(dificuldade=3, 
                                      disciplinas__in=[disciplina], 
                                      numero_prova=numero_prova)

    if len(dificeis) <  questoes_dificeis:
        p.delete()
        return (None,
                "Você não possui questões suficientes de nível difícil na base de dados. \n"
                "Questões solicitadas: %d\n Questões disponíveis: %d" % (questoes_dificeis, len(dificeis)) )

    while i  < questoes_dificeis:
        q = random.choice(dificeis)
        if q not in questoes:
            questoes.append(q)
            i = i + 1

    for q in questoes:
        p.questoes.add(q)

    return p,""

def gera_latex(prova, gabarito):

    if(gabarito):
        arquivo_prova = str(prova).replace(" ", "") + "GABARITO" + str(int(time.time())) + ".tex"
    else:
        arquivo_prova = str(prova).replace(" ", "") + str(int(time.time())) + ".tex"

    tex = codecs.open("/tmp/"+arquivo_prova, 'w', "utf-8")

    tex.write(CABECALHO)

    ano, mes, _ = str(prova.data_aplicacao).split("-")

    mes = int(mes)

    semestre = 1

    if mes > 8:
        semestre = 2

    aux = u"""{{{0:>s}}}
  {{\\textbf{{{1:d}\seqabf\ Prova }}}}
  {{ {2:>s} }}
  {{{3:d}\seqo\ Semestre de {4:>s}}}

\\noindent\\textbf{{Observações}}:
\\begin{{alphaenum}}
\parindent 0mm
\parskip 0mm
\\topsep 0mm
\partopsep 0mm
\itemindent 0mm
\itemsep 0mm
\im Faz parte da prova a interpretação das questões. Se você achar
que está faltando algum detalhe no enunciado da questão, você
deverá fazer as suposições que achar necessárias e escrever estas
suposições juntamente com as res\-pos\-tas.

\im Todas as respostas devem ser justificadas.

\im Prova individual e sem consulta com duração de 100 minutos.

\im Valor desta prova: {5:>d} pontos.

\im Não esqueça de escrever seu nome na folha de res\-pos\-tas e na folha de enunciado.

\\textsc{{Boa Sorte!}}
\end{{alphaenum}}


""".format(prova.disciplina, prova.numero_prova, prova.curso, semestre, ano, prova.valor)

    tex.write(aux)

    questao = u"\section*{\\ul{\\nextval{ª} Questão} \\textrm{\\normalsize\\textsc{(%d pontos)}}}"

    questoes = []

    for index in prova.ordem_questoes:
        questoes.append(prova.questoes.get(pk=int(index)))

    for q in questoes:
        tex.write(questao % q.valor_sugerido)
        tex.write("\n")
        enunciado = unicode(q.enunciado)
        tex.write(enunciado)
        tex.write("\n")
        if(gabarito):
            tex.write("\n")
            tex.write("RESPOSTA:")
            resposta = unicode(q.resposta)
            if (resposta != "None"):
                tex.write(resposta)
            else:
                tex.write(u"Não adicionada")
            tex.write("\n")


    tex.write("\end{document}")
    tex.close()
    return arquivo_prova