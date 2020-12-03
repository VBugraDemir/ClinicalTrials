import pickle
import re

newfile_mesh = open("mesh_dictionary.dat","rb")
mesh_dict = pickle.load(newfile_mesh)
newfile_mesh.close()

newfile_ctcae = open("CTCAEdict.dat","rb")
ctcae_dict = pickle.load(newfile_ctcae)
newfile_ctcae.close()

def cleaning(aranan):
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update(["e", "gi","nos","w","o", "anc"])
    aranan = re.sub(r'\W+', ' ',aranan).lower()
    liste = []
    for i in aranan.split():
        if i.isalpha() and i not in stop_words and len(i)>1:
            liste.append(i)
    a = " ".join(liste)
    return a
def arama(aranan):

    aranan = re.sub(r'\W+', ' ',aranan).replace(" in ", " ").replace(" GI ", " gastrointestinal ").lower()
    score = 0
    max1 = 0
    max2 = 0

    if aranan in mesh_dict:
        return (aranan, mesh_dict[aranan])

    if aranan in ctcae_dict:
        return (aranan, ctcae_dict[aranan])

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
        if all(x in i for x in aranan.split()) or all(x in aranan for x in b.split()) and (len(aranan.split()) == len(b.split()) & all(len(z) !=1 for z in b.split()) & len(b)>3):
            return (i, mesh_dict[i],"asdasd") # sepsis-urosepsis işi bozdu gibi, bak kelime sayısı katılabilir.

    for i in ctcae_dict:
        b = re.sub(r'\W+', ' ', i).lower()
        if all(x in i for x in aranan.split()) or all(x in aranan for x in b.split()) and (len(aranan.split())==len(b.split()) & all(len(z) !=1 for z in b.split())):
            return (i, ctcae_dict[i])
    aranan = cleaning(aranan)
    print(aranan)
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
    try:
        if max1 > max2:
            return (final1, code1, max1)
        else:
            return (final2, code2, max2,"asd")
    except:
        return (aranan, "UNKNOWN-check-for typo")
aranan = "non-cardiac chest pain"
print(arama(aranan))


