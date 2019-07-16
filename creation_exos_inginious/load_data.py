# -*-config:utf-8 -* 

import yaml
from objets_2 import *

def get_indentation(ligne):
    nb = 0
    for c in ligne:
        if c == ' ':
            nb += 1
        else:
            break
    return nb

def get_texte_from_file(filename):
    with open(filename, "r", encoding="utf-8") as fichier:
        lignes = fichier.read()
    return lignes

def get_questions_from_rst(texte):
    if "Question 1." in texte:
        return get_questions_from_rst_format1(texte, forme=1)
    else:
        return get_questions_from_rst_format2(texte, forme=2)

def split_questions(texte_document, forme):
    if forme == 1:
        return texte_document.split("Question ")
    else:
        questions = []
        lignes = texte_document.split("\n")
        texte_question = ""
        hasChoix = False
        hasName = False
        for ligne in lignes:
            if ".. positive::" in ligne or ".. negative::" in ligne:
                hasChoix = True
            if ".. question::" in ligne:
                if hasName:
                    questions += [texte_question]
                    texte_question = ""
                    hasChoix = False
                else:
                    hasName = True
            if "1." in ligne:
                questions.append(texte_question)
                texte_question = ""
            if get_indentation(ligne) == 0 and hasChoix and ligne != '':
                questions += [texte_question]
                hasChoix = False
                hasName = False
                texte_question = ligne + "\n"
            else:
                texte_question += ligne + "\n"
        return questions
    
def get_questions_from_rst_format1(texte, forme=1):
    questions = split_questions(texte, forme)
    questions_retour = []
    infos_new_question = None
    for question in questions[1:]:
        lignes = question.split("\n")
        choices = get_choices_from_rst_format1(lignes)
        infos_new_question = {'name':lignes[0][3:], 'header':[]}
        
        for ligne in lignes[2:]:
            if ".. positive::" in ligne or ".. negative::" in ligne:
                break
            if ".. question::" in ligne:
                nom = ligne.split(" ")
                if nom[-1] == '':
                    nom = nom[-2]
                else:
                    nom = nom[-1]
            elif ":nb" not in ligne:
                if len(infos_new_question["header"]) == 0 and ligne == '':
                    continue
                else:
                    infos_new_question["header"] += [ligne]
                
        if infos_new_question is not None:
            qst = Question(nom=nom, **infos_new_question)
            for choix in choices:
                qst.append_choix(choix)
            questions_retour.append(qst)
    return questions_retour

def get_questions_from_rst_format2(texte, forme=2):
    questions = split_questions(texte, forme)
    questions_retour = []
    infos_new_question = None
    for question in questions[1:]:
        lignes_question = question.split("\n")
        choices = get_choices_from_rst_format2(lignes_question)
        infos_new_question = {'name':"", 'header':[]}
        
        for ligne in lignes_question[:]:
            if ".. positive::" in ligne or ".. negative::" in ligne:
                break
            if ".. question::" in ligne:
                nom = ligne.split(" ")
                if nom[-1] == '':
                    nom = nom[-2]
                else:
                    nom = nom[-1]
                infos_new_question["name"] = nom
            elif ":nb" not in ligne:
                if len(infos_new_question["header"]) == 0 and ligne == '':
                    continue
                else:
                    infos_new_question["header"] += [ligne]
                
        if infos_new_question is not None:
            qst = Question(nom=nom, **infos_new_question)
            for choix in choices:
                qst.append_choix(choix)
            questions_retour.append(qst)
    return questions_retour

def get_choices_from_rst_format1(lignes_question):
    choix = []
    add_comment = False
    infos_new_choix = None
    for ligne in lignes_question:
        if ".. positive::" in ligne or ".. negative::" in ligne:
            if infos_new_choix is not None:
                choix.append(Choix(**infos_new_choix))
            infos_new_choix = {'text':[], 'feedback':[], 'valid':False}
            add_comment = False
        elif infos_new_choix is None:
            continue

            
        if ".. positive::" in ligne:
            infos_new_choix["valid"] = True
        elif ".. negative::" in ligne:
            infos_new_choix["valid"] = False
        elif ".. comment::" in ligne:
            add_comment = True
        elif add_comment:
            infos_new_choix["feedback"] += [ligne]
        else:
            infos_new_choix["text"] += [ligne]
    if infos_new_choix is not None:
        choix.append(Choix(**infos_new_choix))
    return choix



def get_choices_from_rst_format2(lignes_question):
    choix = []
    add_comment = False
    infos_new_choix = None
    for ligne in lignes_question:
        if ".. positive::" in ligne or ".. negative::" in ligne:
            if infos_new_choix is not None:
                choix.append(Choix(**infos_new_choix))
            infos_new_choix = {'text':[], 'feedback':[], 'valid':False}
            add_comment = False
        elif infos_new_choix is None:
            continue

            
        if ".. positive::" in ligne:
            infos_new_choix["valid"] = True
            ligne = ligne.replace(".. positive::", "")
        elif ".. negative::" in ligne:
            infos_new_choix["valid"] = False
            ligne = ligne.replace(".. negative::", "")
        elif ".. comment::" in ligne:
            add_comment = True
            ligne = ligne.replace(".. comment::", "")
        elif "..comment::" in ligne:
            add_comment = True
            ligne = ligne.replace("..comment::", "")
            
        if add_comment:
            infos_new_choix["feedback"] += [ligne]
        else:
            infos_new_choix["text"] += [ligne]
    if infos_new_choix is not None:
        choix.append(Choix(**infos_new_choix))
    return choix
    
def get_qcm_name_from_rst(texte):
    for ligne in texte.split("\n"):
        if len(ligne) > 3 and ".." not in ligne and get_indentation(ligne) == 0:
            return ligne

def get_qcm_context_from_rst(texte):
    context = []
    add_context = True
    for ligne in texte.split("\n"):
        if "1." in ligne:
            break
        if len(ligne) > 3 and ".." not in ligne and ":" not in ligne and get_indentation(ligne) == 0:
            context += [ligne]
    return context
