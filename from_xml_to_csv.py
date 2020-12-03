import glob
import xml.etree.ElementTree as ET
file0 = open("C:\Python\Python38\Projects\Clinical_Trials\Sorafenib_Doxorubicine_Cytarabine-data.csv","a",encoding='utf-8')
all_files = glob.glob("Cytarabine/*")
list_lines = []
list_titles = [" "]
list_discriptions = [" "]
for file in all_files:
    tree = ET.parse(file)
    root = tree.getroot()
    
    for child in root.iter('required_header'):
        for a in child.iter("url"):
            urls = a.text

    for child in root.iter("brief_title"):
        brief_title = (child.text).replace(",", " ")
        file0.writelines("\n" + brief_title +"("+urls+")"+"\n")

    for child in root.iter('reported_events'):
        for a in child.iter("group_list"):
            for b in a.iter("title"):
                list_titles.append(b.text.replace(",",""))
            for b in a.iter("description"):
                list_discriptions.append((b.text).replace("\n"," ").replace(",","").replace("\r"," "))
    line_titles = ",".join(x for x in list_titles)
    file0.writelines(line_titles + "\n")
    list_titles = [" "]
    line_discriptions = ",".join(x for x in list_discriptions)
    file0.writelines(line_discriptions + "\n")
    list_discriptions = [" "]

    for child in root.iter("serious_events"):

        for child2 in child.iter("event"):

            for a in child2.iter("sub_title"):

                list_lines.append((a.text).replace(",", ""))
            for z in child2.iter("counts"):
                try:
                    list_lines.append(z.attrib["subjects_affected"] + "/" + z.attrib["subjects_at_risk"] + " %" + str(
                        round((int(z.attrib["subjects_affected"]) / int(z.attrib["subjects_at_risk"])) * 100, 2)))
                except KeyError:
                    pass
                except ZeroDivisionError:
                    list_lines.append("0/0 %0.0")
            lines = ",".join(x for x in list_lines)
            file0.writelines(lines + "\n")
            list_lines = []

file0.close()
