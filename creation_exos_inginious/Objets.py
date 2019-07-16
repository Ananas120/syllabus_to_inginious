# -*-config:utf-8 -* 
import yaml

CHAR_INTERDITS = {"`_":"`"}
def print_dict(dico, indentation=0):
    for key, value in dico.items():
        phrase = ""
        for i in range(indentation):
            phrase += "\t"
        if type(value) == dict:
            phrase += key + " : "
            print(phrase, key, ":")
            print_dict(value, indentation+1)
        else:
            print(phrase, key, ":", value)
    return ""
            
def load_yaml(filename):
    with open(filename, "r") as fichier:
        dico = yaml.load(fichier)
    return dico

def dico_to_yaml(dico, filename):
    with open(filename, "w") as fichier:
        yaml.dump(dico, fichier, allow_unicode=True)

def format_string(phrase, dico={}, remove_indent=False, get_indent=False):
    phrase_format = ""
    nb_indent = 0
    for lettre in phrase:
        if lettre == ' ' and phrase_format == "":
            nb_indent += 1
            if remove_indent:
                continue
            else:
                phrase_format += lettre
        else:
            phrase_format += lettre
    for lettre, remplacement in CHAR_INTERDITS.items():
        phrase_format = phrase_format.replace(lettre, remplacement)
    for lettre, remplacement in dico.items():
        phrase_format = phrase_format.replace(lettre, remplacement)
    if get_indent:
        return phrase_format, nb_indent
    return phrase_format

class QCM:
    def __init__(self, **kwargs):
        self.questions = []
        self.dico = self.build_default_qcm_format(kwargs)
        
    def build_default_qcm_format(self, kwargs, filename="default_format.yaml"):
        dico = load_yaml(filename)
        for key, value in kwargs.items():
            dico[key] = value
        return dico
    
    def __str__(self):
        return self.toString(self.dico)
    
    def toString(self, dico, indentation=0):
        texte = ""
        for key, value in dico.items():
            for i in range(indentation):
                texte += "    "
            if key == 'problems':
                texte += str(key) + ":\n"
                for i, qst in enumerate(self.questions):
                    texte += qst.toString(None, indentation+1, i)
            elif type(value) == dict:
                if len(value) > 0:
                    texte += str(key) + ":\n"
                    texte += self.toString(value, indentation+1)
                else:
                    texte += str(key) + ": {}\n"
            elif type(value) == list:
                texte += key + ": |\n"
                code = False
                for phrase in value:
                    if ".. code-block::" in phrase:
                        texte += "\n"
                    format_phrase = format_string(phrase)
                    if format_phrase != '':
                        for j in range(indentation+1):
                            texte += "    "
                        if code:
                            texte += "   "
                        texte += format_phrase + "\n"
                    if ".. code-block::" in phrase:
                        code = True
                        texte += "\n"
            else:
                texte += str(key) + ": " + str(value) + "\n"
        return texte
        
    def append_question(self, question):
        self.questions.append(question)
        
    def clear_question(self):
        self.questions = []
        
    def save(self, filename, mode='w'):
        with open(filename, mode, encoding='utf-8') as fichier:
            fichier.write(self.toString(self.dico))
    
    def to_txt(self, with_multiple_choice=True, with_choice_explication=True):
        texte = "\n\n"
        for qst in self.questions:
            if not with_multiple_choice and qst.dico["multiple"]:
                texte += qst.to_txt(with_choice_explication)
        return texte
    
    def save_txt(self, filename, mode='w', **kwargs):
        with open(filename, mode, encoding='utf-8') as fichier:
            fichier.write(self.to_txt(**kwargs))
        
class Question:
    def __init__(self, nom=None, name='', limit=None, multiple=False, type_task='multiple_choice', header=""):
        self.choix = []
        self.nom = nom
        self.dico = self.build_default_format()
        self.dico["name"] = name
        self.dico["limit"] = limit
        self.dico["multiple"] = multiple
        self.dico["type"] = type_task
        self.dico["header"] = header
        
    def build_default_format(self, filename="default_format_question.yaml"):
        return load_yaml(filename)
        
    def append_choix(self, choix):
        self.choix.append(choix)
        self.dico["limit"] = len(self.choix)
        if self.number_valid_choice() > 1:
            self.dico["multiple"] = True
        
    def __str__(self):
        return self.toString(self.dico)
    
    def toString(self, dico, indentation=0, num_qst=0):
        if dico is None:
            dico = self.dico
        texte = ""
        for i in range(indentation):
            texte += "    "
        #texte += format_string(self.name, dico={" ":"_", ".":"", "(":"", ")":"", "`":""}) + ":\n"
        if self.nom is None:
            texte += "qst" + str(num_qst) + ":\n"
        else:
            texte += self.nom + ":\n"
        indentation+=1
        for key, value in dico.items():
            for i in range(indentation):
                texte += "    "
                
            if key == 'choices':
                texte += str(key) + ":\n"
                for c in self.choix:
                    texte += c.toString(None, indentation)
            else:
                if type(value) == list:
                    texte += key + ": |\n"
                    code = False
                    code_indent, code_written = False, False
                    ancienne_phrase = ""
                    for phrase in value:
                        if ".. code-block::" in phrase:
                            texte += "\n"
                        format_phrase, nb_indent = format_string(phrase, remove_indent=True, get_indent=True)
                        if format_phrase == '' and ancienne_phrase == "" and code and code_written:
                            code = False
                        elif format_phrase == '':
                            texte += "\n"
                        else:
                            for j in range(indentation+1):
                                texte += "    "
                            if code:
                                code_written = True
                                texte += "   "
                                if '}' in format_phrase:
                                    code_indent = False
                                if code_indent:
                                    texte += "  "
                                if '{' in format_phrase:
                                    code_indent = True
                            texte += format_phrase + "\n"
                        if ".. code-block::" in phrase:
                            code = True
                            texte += "\n"
                        ancienne_phrase = phrase
                else:
                    texte += str(key) + ": " + str(value) + "\n"
        return texte
    
    def format_name(self):
        liste_interdits = [" ", ".", "(", ")", "`"]
        nom = ""
        for c in self.name:
            if c not in liste_interdits:
                nom += c
            elif c == " ":
                nom += "_"
        return nom
    
    def get_data(self):
        dico = self.dico
        dico["choices"] = [c.dico for c in self.choix]
        return dico
    
    def number_valid_choice(self, with_choice_explication=True):
        nb = 0
        for c in self.choix:
            if c.is_valid():
                nb+=1
        return nb
        
    def to_txt(self, with_choice_explication=True):
        texte = "Q| "
        code = False
        code_indent, code_written = False, False
        ancienne_phrase = ""
        for phrase in self.dico["header"]:
            if ".. code-block::" in phrase:
                texte += "\n"
                code = True
                ancienne_phrase = phrase
                continue
            format_phrase, nb_indent = format_string(phrase, remove_indent=True, get_indent=True)
            if format_phrase == '' and ancienne_phrase == "" and code and code_written:
                code = False
            elif format_phrase == '':
                texte += "\n"
            else:
                if code:
                    code_written = True
                    texte += "   "
                    if '}' in format_phrase:
                        code_indent = False
                    if code_indent:
                        texte += "  "
                    if '{' in format_phrase:
                        code_indent = True
                texte += format_phrase + "\n"
            ancienne_phrase = phrase
        
        for c in self.choix:
            texte += c.to_txt(with_choice_explication)
        return texte
    
class Choix:
    def __init__(self, text="", valid=False, feedback=""):
        self.dico = {}
        self.dico["text"] = text
        self.dico["valid"] = valid
        self.dico["feedback"] = feedback
        
    def __str__(self):
        return self.toString(self.dico)
    
    def toString(self, dico, indentation=0):
        if dico is None:
            dico = self.dico
        texte = ""
        for i, (key, value) in enumerate(dico.items()):
            for j in range(indentation):
                texte += "    "
            if i == 0:
                texte += "-   "
                indentation += 1
            if type(value) == list:
                texte += key + ": |\n"
                code = False
                code_indent, code_written = False, False
                ancienne_phrase = ""
                for phrase in value:
                    if ".. code-block::" in phrase:
                        texte += "\n"
                    format_phrase, nb_indent = format_string(phrase, remove_indent=True, get_indent=True)
                    if format_phrase == '' and ancienne_phrase == "" and code and code_written:
                        code = False
                    elif format_phrase == '':
                        texte += "\n"
                    else:
                        for j in range(indentation+1):
                            texte += "    "
                        if code:
                            code_written = True
                            texte += "   "
                            if '}' in format_phrase:
                                code_indent = False
                            if code_indent:
                                texte += "  "
                            if '{' in format_phrase:
                                code_indent = True
                        texte += format_phrase + "\n"
                    if ".. code-block::" in phrase:
                        code = True
                        texte += "\n"
                    ancienne_phrase = phrase
            else:
                texte += str(key) + ": " + str(value) + "\n"
        return texte
    
    def is_valid(self):
        return self.dico["valid"]
    
    def to_txt(self, with_explication):
        texte = "C| " 
        code = False
        code_indent, code_written = False, False
        ancienne_phrase = ""
        for phrase in self.dico["text"]:
            if ".. code-block::" in phrase:
                texte += "\n"
                code = True
                ancienne_phrase = phrase
                continue
            format_phrase, nb_indent = format_string(phrase, remove_indent=True, get_indent=True)
            if format_phrase == '' and ancienne_phrase == "" and code and code_written:
                code = False
            elif format_phrase == '':
                texte += "\n"
            else:
                if code:
                    code_written = True
                    texte += "   "
                    if '}' in format_phrase:
                        code_indent = False
                    if code_indent:
                        texte += "  "
                    if '{' in format_phrase:
                        code_indent = True
                texte += format_phrase + "\n"
            ancienne_phrase = phrase
        if self.dico["valid"]:
            texte += "|V\n\n"
        else:
            texte += "|F\n\n"
        if with_explication:
            texte += "CE|" + "\n".join(self.dico["feedback"])
        return texte
