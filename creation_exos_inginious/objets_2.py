# -*-config:utf-8 -* 

import yaml
from balises import *
from utils import *

class QCMItem(object):
    def __init__(self):
        self.dico = {}
        self.questions = None
        self.choix = None
        
    def __str__(self):
        return self.toString(0)
    
    def toString(self, indentation=0, dico=None):
        if dico is None: dico = self.dico
        texte = ""
            
        for key, value in dico.items():
            texte += get_indent(indentation)
            if key == 'choices':
                texte += str(key) + ":\n"
                for c in self.choix:
                    texte += c.toString(indentation+1, None)
            elif key == 'problems':
                texte += str(key) + ":\n"
                for i, qst in enumerate(self.questions):
                    texte += qst.toString(i, indentation+1, None)
            elif type(value) is list:
                texte += str(key) + ": |\n"
                for elem in value:
                    if issubclass(type(elem), Balise):
                        texte += elem.toString(indentation+1)
                    else:
                        phrase_formattee, nb_indent = format_string(elem, remove_indent=True, get_indent=True)
                        texte += get_indent(indentation+1) + phrase_formattee + "\n"
            elif type(value) is dict:
                texte += str(key) + ":\n"
                texte += self.toString(indentation+1, value)
            elif type(value) is str:
                texte += str(key) + ": " + format_string(value, remove_indent=True, get_indent=False) + "\n"
            else:
                texte += str(key) + ": " + str(value) + "\n"
        return texte

    def toTxt(self):
        raise notImplementedError()
        
class QCM(QCMItem):
    def __init__(self, **kwargs):
        self.questions = []
        self.dico = self.build_default_qcm_format(kwargs)
        
    def build_default_qcm_format(self, kwargs, filename="default_format.yaml"):
        dico = load_yaml(filename)
        for key, value in kwargs.items():
            if type(value) is list:
                dico[key] = Balise.filtre(value)
            else:
                dico[key] = value
        return dico
        
    def append_question(self, question):
        self.questions.append(question)
        
    def clear_question(self):
        self.questions = []

    def save(self, filename, mode='w'):
        with open(filename, mode, encoding='utf-8') as fichier:
            fichier.write(self.toString(0, self.dico))

    def toTxt(self, with_multiple_choice=True, with_choice_comment=True):
        texte = "\n\n"
        for q in self.questions:
            if not with_multiple_choice and q.dico["multiple"]:
                continue
            else:
                texte += q.toTxt(with_choice_comment)
        return texte
    
    def saveTxt(self, filename, mode="w", **kwargs):
        with open(filename, mode, encoding='utf-8') as fichier:
            fichier.write(self.toTxt(**kwargs))
        
class Question(QCMItem):
    def __init__(self, nom=None, name='', header=[], limit=None, multiple=False, type_task='multiple_choice'):
        self.choix = []
        self.nom = nom
        self.dico = {}
        self.dico["name"] = name
        self.dico["header"] = header
        self.dico["limit"] = limit
        self.dico["multiple"] = multiple
        self.dico["type"] = type_task
        self.dico["choices"] = None
        for key, value in self.dico.items():
            if type(value) is list:
                self.dico[key] = Balise.filtre(value)
            else:
                self.dico[key] = value
                
    def append_choix(self, c):
        self.choix.append(c)
        nb = 0
        for ch in self.choix:
            if ch.dico["valid"]: nb += 1
        if nb > 1: self.dico["multiple"] = True
        
    def toString(self, num_qst, indentation=0, dico=None):
        texte = get_indent(indentation)
            
        if self.nom is None:
            texte += "qst" + str(num_qst) + ":\n"
        else:
            texte += self.nom + ":\n"
        indentation += 1
        
        if dico is None:
            dico = self.dico
        
        for key, value in dico.items():
            texte += get_indent(indentation)
            if key == 'choices':
                texte += str(key) + ":\n"
                for c in self.choix:
                    texte += c.toString(indentation+1, None)
            elif key == 'problems':
                texte += str(key) + ":\n"
                for i, qst in enumerate(self.questions):
                    texte += qst.toString(i, indentation+1, None)
            elif type(value) is list:
                texte += str(key) + ": |\n"
                for elem in value:
                    if issubclass(type(elem), Balise):
                        texte += elem.toString(indentation+1)
                    else:
                        phrase_formattee, nb_indent = format_string(elem, remove_indent=True, get_indent=True)
                        texte += get_indent(indentation+1) + phrase_formattee + "\n"
            elif type(value) is dict:
                texte += str(key) + ":\n"
                texte += self.toString(indentation+1, value)
            elif type(value) is str:
                texte += str(key) + ": " + format_string(value, remove_indent=True, get_indent=False) + "\n"
            else:
                texte += str(key) + ": " + str(value) + "\n"
        return texte
    
    def toTxt(self, with_choice_comment=True):
        texte = "Q| \n"
        for elem in self.dico["header"]:
            if issubclass(type(elem), Balise):
                texte += elem.toString(0, False)
            else:
                phrase_formattee, nb_indent = format_string(elem, remove_indent=True, get_indent=True)
                texte += phrase_formattee + "\n"
                
        for c in self.choix:
            texte += c.toTxt(with_choice_comment)
        texte += "\n"
            
        return texte
            
class Choix(QCMItem):
    def __init__(self, text=[], valid=False, feedback=[]):
        self.dico = {}
        self.dico["text"] = text
        self.dico["valid"] = valid
        self.dico["feedback"] = feedback
        for key, value in self.dico.items():
            if type(value) is list:
                self.dico[key] = Balise.filtre(value)
            else:
                self.dico[key] = value

    def toTxt(self, with_comment):
        texte = "C| \n"
        for elem in self.dico["text"]:
            if issubclass(type(elem), Balise):
                texte += elem.toString(0, False)
            else:
                phrase_formattee, nb_indent = format_string(elem, remove_indent=True, get_indent=True)
                texte += phrase_formattee + "\n"
        if self.dico["valid"]: texte += "|V\n"
        else: texte += "|F\n"
        
        if with_comment:
            texte += "CE| \n"
            for elem in self.dico["feedback"]:
                if issubclass(type(elem), Balise):
                    texte += elem.toString(0, False)
                else:
                    phrase_formattee, nb_indent = format_string(elem, remove_indent=True, get_indent=True)
                    texte += phrase_formattee + "\n"
        return texte
