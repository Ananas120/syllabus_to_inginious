
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

def format_string(phrase, dico={}, remove_indent=False, get_indent=False, count_tab=False, remove_tab=False):
    has_lettre = False
    phrase_format = ""
    nb_indent, nb_tab = 0, 0
    for lettre in phrase:
        if lettre == ' ' and not has_lettre:
            nb_indent += 1
            if remove_indent:
                continue
            else:
                phrase_format += lettre
        elif lettre == '\t' and not has_lettre:
            nb_tab += 1
            if remove_tab:
                continue
            else:
                phrase_format += lettre
        else:
            has_lettre = True
            phrase_format += lettre
    for lettre, remplacement in CHAR_INTERDITS.items():
        phrase_format = phrase_format.replace(lettre, remplacement)
    for lettre, remplacement in dico.items():
        phrase_format = phrase_format.replace(lettre, remplacement)
    if get_indent:
        if count_tab: return phrase_format, nb_indent, nb_tab
        else: return phrase_format, nb_indent
    return phrase_format

def get_indent(nombre, tabulation="    "):
    texte = ""
    for i in range(nombre):
        texte += tabulation
    return texte
