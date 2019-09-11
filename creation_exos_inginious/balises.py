from utils import *

_fake_balises = []

class Balise(object):
    def __init__(self, texte=[]):
        self.texte = texte
        
    def isEmpty(self):
        for p in self.texte:
            if p != '':
                return False
        return True
    
    def __str__(self):
        return self.toString(0)
    
    def toString(self, indentation=0):
        raise notImplementedError()
        
    def get_balise(ligne):
        if "code-block" in ligne:
            ligne = ligne.split(" ")
            if ligne[-1] == '': langage = ligne[-2]
            else: langage = ligne[-1]
            return BaliseCode(langage, [])
        else:
            nom_balise = ligne.split("::")[0].split("..")[1]
            nom_balise = "..{}::".format(nom_balise)
            if nom_balise not in _fake_balises:
                _fake_balises.append(nom_balise)
                print("Balise non reconnue (son contenu ne sera pas ajouté au document) : {}".format(nom_balise))
            return FakeBalise([])
    get_balise = staticmethod(get_balise)
    
    def filtre(liste_lignes):
        liste_retour = []
        balise = None
        indentation_balise, tab_balise = 0, 0
        for ligne in liste_lignes:
            if ".." in ligne and "::" in ligne:
                balise = Balise.get_balise(ligne)
                _, indentation_balise, tab_balise = format_string(ligne, get_indent=True, remove_indent=False, count_tab=True)
            elif balise is None:
                liste_retour.append(ligne)
            else:
                _, indent, tab = format_string(ligne, get_indent=True, remove_indent=False, count_tab=True)
                if balise.isEmpty() or (ligne == "" and balise.texte[-1] != "") or (indent > indentation_balise and tab >= tab_balise):
                    balise.add_texte(ligne)
                else:
                    if type(balise) is not FakeBalise:
                        liste_retour.append(balise)
                    balise = None
                    liste_retour.append(ligne)
        if balise is not None:
            if type(balise) is not FakeBalise:
                liste_retour.append(balise)
        return liste_retour
    filtre = staticmethod(filtre)
        
class FakeBalise(Balise):
    def __init__(self, texte=[]):
        self.texte = texte
        
    def add_texte(self, texte):
        self.texte.append(texte)
        
class BaliseCode(Balise):
    def __init__(self, langage, texte=[]):
        self.langage = langage
        self.texte = texte
        
    def add_texte(self, texte):
        self.texte.append(texte)

    def toString(self, indentation, with_balise_descriptor=True):
        #print(self.texte)
        if with_balise_descriptor:
            texte = "\n" + get_indent(indentation) + ".. code-block:: " + self.langage + "\n"
        else:
            texte = "\n"
        code_indent = 0
        for phrase in self.texte:
            phrase_formattee = format_string(phrase, remove_indent=True, get_indent=False)
            if phrase_formattee == '':
                if texte == "": continue
                else: 
                    texte += "\n"
                    continue
            else:
                texte += get_indent(indentation)
                texte += "   "
                if '}' in phrase_formattee:
                    code_indent -= 1
                if code_indent != 0:
                    for ind in range(code_indent):
                        texte += "  "
                if '{' in phrase_formattee:
                    code_indent += 1
            texte += phrase_formattee + "\n"
        texte += "\n"
        return texte

