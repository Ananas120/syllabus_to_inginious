from utils import *
from objets_2 import *
from load_data import *
import os

def build_qcm(filename, filename_dest=None, one_file_per_question=False, with_multiple_choice=True, with_choice_comment=True, to_txt=False):
    if os.path.isdir(filename):
        for file in os.listdir(filename):
            build_qcm(filename+"/"+file, filename_dest, one_file_per_question, with_multiple_choice, with_choice_comment, to_txt)
        return True
    elif ".rst" in filename:
        texte = get_texte_from_file(filename)
        nom = get_qcm_name_from_rst(texte)
        contexte = get_qcm_context_from_rst(texte)
        questions = get_questions_from_rst(texte)
    else:
        return False
    qcm = QCM(name=nom, context=contexte)
    if not one_file_per_question:
        for qst in questions:
            qcm.append_question(qst)
        mode = 'a'
        if filename_dest is None:
            mode = 'w'
            filename_dest = filename.split("/")
            filename_dest[-1] = "_" + filename_dest[-1].split(".")[0]
            if to_txt:
                filename_dest[-1] += ".txt"
            else:
                filename_dest[-1] += ".yaml"
            filename_dest = "/".join(filename_dest)
        if not to_txt:
            qcm.save(filename_dest, mode)
        else:
            qcm.saveTxt(filename_dest, mode, with_multiple_choice=with_multiple_choice, with_choice_comment=with_choice_comment)
        print("QCM : \"" + nom + "\" correctement créé dans",filename_dest,"!")
    else:
        for qst in questions:
            qcm.clear_question()
            qcm.append_question(qst)
            filename_dest = filename.split("/")
            filename_dest[-1] = "_" + filename_dest[-1].split(".")[0] + "_" + qst.nom 
            if to_txt:
                filename_dest[-1] += ".txt"
            else:
                filename_dest[-1] += ".yaml"
            filename_dest = "/".join(filename_dest)
            if not to_txt:
                qcm.save(filename_dest)
            else:
                qcm.saveTxt(filename_dest, with_multiple_choice=with_multiple_choice, with_choice_comment=with_choice_comment)
            print("Question : \"" + qst.nom + "\" correctement créée dans",filename_dest,"!")
    return True
    
if __name__ == '__main__':
    print(build_qcm("mcq-ex", 
                    filename_dest="quizz_systeme_informatique.txt", 
                    one_file_per_question=False, 
                    to_txt=True,
                    with_choice_comment=False,
                    with_multiple_choice=False))
    #qcm.save("Z:/Test_quentin/task.yaml")
    #print_dict(load_yaml("_qcm-1.yaml"))
    
