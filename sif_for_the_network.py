import pickle
import re
from nltk.corpus import stopwords

newfile_mesh = open("mesh_dictionary.dat","rb")
mesh_dict = pickle.load(newfile_mesh)
newfile_mesh.close()

newfile_ctcae = open("CTCAEdict.dat","rb")
ctcae_dict = pickle.load(newfile_ctcae)
newfile_ctcae.close()

def cleaning(aranan):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["e", "gi","nos","w","o", "anc"])
    aranan = re.sub(r'\W+', ' ',aranan).lower()
    liste = []
    for i in aranan.split():
        if i.isalpha() and i not in stop_words and len(i)>1:  # 11.11.2020 yeni gelenlerde tek harfliler bias yaratıyordu...
            liste.append(i)
    a = " ".join(liste)
    return a

def arama(aranan):

    aranan = re.sub(r'\W+', ' ',aranan).replace(" in ", " ").replace(" GI ", " gastrointestinal ").lower()  # 11.11.2020 in ler ayrıldı
    score = 0
    max1 = 0
    max2 = 0

    if aranan in mesh_dict:
        return (aranan,mesh_dict[aranan])

    if aranan in ctcae_dict:
        return (aranan,ctcae_dict[aranan])

    if len(aranan.split()) == 2:
        aranan_reverse = aranan.split()
        aranan_reverse.reverse()
        aranan_reverse=" ".join(aranan_reverse)

        if aranan_reverse in mesh_dict:
            return (aranan_reverse, mesh_dict[aranan_reverse])
        if aranan_reverse in ctcae_dict:
            return (aranan_reverse, ctcae_dict[aranan_reverse])

    for i in mesh_dict:
        b = re.sub(r'\W+', ' ', i).lower()
        if all(x in i for x in aranan.split()) or all(x in aranan for x in b.split()) and (
                len(aranan.split()) == len(b.split()) & all(len(z) != 1 for z in b.split()) & len(b) > 3):
            return (i,mesh_dict[i])

    for i in ctcae_dict:
        b = re.sub(r'\W+', ' ', i).lower()
        if all(x in i for x in aranan.split()) or all(x in aranan for x in b.split()) and (
                len(aranan.split()) == len(b.split()) & all(len(z) != 1 for z in b.split())):
            return (i,ctcae_dict[i])

    aranan = cleaning(aranan)

    for i in mesh_dict:
        b = re.sub(r'\W+', ' ', i).lower()
        for a in aranan.split():
            if a in b:
                score += 1
                if len(b.split()) > 1 and "infection" in i and "infection" in a:
                    score += 1
        if (score / len(b.split())) * (score / len(aranan.split())) > max2:
            max2 = (score / len(b.split())) * (score / len(aranan.split()))
            score = 0
            final2 = i
            code2 = mesh_dict[i]
        else:
            score = 0


    for i in ctcae_dict:
        b = re.sub(r'\W+', ' ', i).lower()
        for a in aranan.split():
            if a in b:
                score += 1
                if len(b.split()) > 1 and "infection" in i and "infection" in a:
                    score += 1
        if (score / len(b.split())) * (score / len(aranan.split())) > max1:
            max1 = (score / len(b.split())) * (score / len(aranan.split()))
            score = 0
            final1 = i
            code1 = ctcae_dict[i]
        else:
            score = 0
    try:
        if max1 > max2:
            return (final1, code1)
        else:
            return (final2, code2)
    except:
        return ("D00","UNKNOWN-check-for-typo")

termlist = []
idlist = []
group_list = []
counter = 1

file_node_labels_csv = open("12-11-Sorafenib_Doxorubicine_Cytarabine_node_labels.csv", "w")
file_node_labels_csv.writelines("," + "attribute" + "\n")

file_clinical_trials = open("C:\Python\Python38\Projects\Clinical_Trials\Sorafenib_Doxorubicine_Cytarabine-data.csv", "r")  
file_clinical_trials.readline()

file_network_sif = open("12-11-Sorafenib_Doxorubicine_Cytarabine_network_sif.sif","w")

file_node_descriptions_csv = open("12-11-Sorafenib_Doxorubicine_Cytarabine_node_descriptions.csv", "w")
file_node_descriptions_csv.writelines("," + "title"+ "," + "descriptions" + "\n")

file_control_csv = open("12-11-Sorafenib_Doxorubicine_Cytarabine_csv_id_vs_dict_id.csv", "w")
file_control_csv.writelines("csv term in  the file" + "," + "Found dict term" + "\n")

file_int_strength_csv = open("12-11-Sorafenib_Doxorubicine_Cytarabine_edge_strength.csv", "w")
file_int_strength_csv.writelines("," + "InteractionStrength" + "\n")

while 1:
    temp = file_clinical_trials.readline()
    if temp == "":
        break
    lines = temp.strip().split(",")

    if len(lines) == 1 and "" not in lines:
        id_description = lines[0][:-45]
        id = lines[0][-12:-1]
        file_node_descriptions_csv.writelines(id+ "," + id_description+ "," + "\n")
        print(counter)
        counter += 1

    elif len(lines) > 1 and "" in lines:
        group_list.append(lines)

    elif "" not in lines:
        terms = lines
        term_in_dict = arama(terms[0])[1]
        term_name = arama(terms[0])[0].replace(",", "")
        file_control_csv.writelines(terms[0] + "," + term_name + "\n")

        if id not in idlist:
            file_node_labels_csv.writelines(id + "," + "study" + "\n")
            for n in range(1, len(terms)):
                file_network_sif.writelines(id + "-" + str(n) + " " + "part_of" + " " + id + "\n")
                file_node_labels_csv.writelines(id + "-" + str(n) + "," + "group" + "\n")

                try:
                    file_node_descriptions_csv.writelines(id + "-" + str(n) + "," + group_list[0][n] + "," + "Description: " + group_list[1][n] + "\n")
                except IndexError:
                    file_node_descriptions_csv.writelines(id + "-" + str(n) + "," + group_list[0][n] + "," + "Description: " + "No description found" + "\n")

        idlist.append(id)
        group_list = []
        if term_in_dict not in termlist:
            file_node_labels_csv.writelines(str(term_in_dict) + "," + "disease" + "\n")
            file_node_descriptions_csv.writelines(str(term_in_dict) + "," + term_name + "," + "\n")
            termlist.append(term_in_dict)

        for n in range(1,len(terms)):
            if terms[n].split()[1] != "%0.0":
                file_network_sif.writelines(id + "-" + str(n) + " " +"associated_with" + " " + str(term_in_dict) + "\n")
                file_int_strength_csv.writelines(id + "-" + str(n) + " " + "(associated_with)" + " " + str(term_in_dict) + "," + terms[n].split()[1].replace("%","") + "\n")



file_node_labels_csv.close()
file_clinical_trials.close()
file_network_sif.close()
file_node_descriptions_csv.close()
file_control_csv.close()
file_int_strength_csv.close()
