from utils import *

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
            print("Balise non reconnue :",ligne)
            return None
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
                if ligne == "" or balise.isEmpty() or indent != indentation_balise or tab != tab_balise:
                    balise.add_texte(ligne)
                else:
                    print("Stop balise :",ligne, indentation_balise, indent)
                    liste_retour.append(balise)
                    balise = None
        if balise is not None: liste_retour.append(balise)
        return liste_retour
    filtre = staticmethod(filtre)
        
class BaliseCode(Balise):
    def __init__(self, langage, texte=[]):
        self.langage = langage
        self.texte = texte
        
    def add_texte(self, texte):
        self.texte.append(texte)

    def toString(self, indentation, with_balise_descriptor=True):
        print(self.texte)
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

