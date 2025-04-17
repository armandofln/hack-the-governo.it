from os import listdir
from os.path import join, exists, isfile
from string import Template
import datetime
import locale

img_dataset = ["img_logo", "img_in_primo_piano_0", "img_in_primo_piano_1", "img_in_primo_piano_2", "img_in_primo_piano_3", "img_focus_0", "img_focus_1", "img_focus_2", "img_da_palazzo_chigi_0", "img_da_palazzo_chigi_1", "img_da_palazzo_chigi_2", "img_galleria_0", "img_galleria_1", "img_galleria_2", "img_galleria_3", "img_galleria_4", "img_galleria_5", "img_galleria_6", "img_galleria_7", "img_dalla_presidenza_0", "img_dalla_presidenza_1", "img_dalla_presidenza_2"]
text_dataset = ["text_in_primo_piano_0", "text_in_primo_piano_1", "text_in_primo_piano_2", "text_in_primo_piano_3", "text_focus_0", "text_focus_1", "text_focus_2", "text_da_palazzo_chigi_0", "text_da_palazzo_chigi_1", "text_da_palazzo_chigi_2", "text_galleria_0", "text_galleria_1", "text_galleria_2", "text_galleria_3", "text_galleria_4", "text_galleria_5", "text_galleria_6", "text_galleria_7", "text_dalla_presidenza_0", "text_dalla_presidenza_1", "text_dalla_presidenza_2"]

def get_date():
	locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
	today = datetime.date.today()
	formatted_date = today.strftime("%d %B %Y")
	formatted_date = formatted_date.replace(today.strftime("%B"), today.strftime("%B").capitalize())
	return formatted_date

#10 Aprile 2025 §data
#§text_in_primo_piano_0_header
#§text_in_primo_piano_0_body
#§text_focus_1
#§text_galleria_0
#§text_da_palazzo_chigi_0_header
#§text_da_palazzo_chigi_0_body
#§text_dalla_presidenza_0_header
#§text_dalla_presidenza_0_body

def compute_file_list(dir):
	files = [f for f in listdir(dir) if isfile(join(dir, f))]
	return files

def find_file_in_list(file, _list):
	for e in _list:
		if e.startswith(file):
			return e
	return ""

def compute_img_dictionary(default_list, inject_list):
	dic = {}
	for key in img_dataset:
		value = find_file_in_list(key, inject_list)
		if value == "":
			value = "./default/" + find_file_in_list(key, default_list)
		else:
			value = "./inject/" + value
		dic[key] = value
	return dic

def compute_text_dictionary(default_list, inject_list):
	dic = {}
	for key in text_dataset:
		file_name = find_file_in_list(key, inject_list)
		if file_name == "":
			file_name = find_file_in_list(key, default_list)
			path = "default"
		else:
			path = "inject"
		path = join("webpage", path, file_name)
		if ("focus" in key) or ("galleria" in key):
			with open(path, 'r', encoding="utf-8") as f:
				dic[key] = f.read()
			continue
		with open(path, 'r', encoding="utf-8") as f:
			dic[key + "_header"] = f.readline()
			dic[key + "_body"] = f.read()
	return dic

def generate_html_file(dic):
	class over_template(Template):
		delimiter = '§'

	with open("template.html", "r", encoding="utf-8") as file:
		template = over_template(file.read())

	output = template.substitute(dic)

	with open(join("webpage", "index.html"), "w", encoding="utf-8") as file:
		file.write(output)


def main():
	default_list = compute_file_list(join("webpage", "default"))
	inject_list = compute_file_list(join("webpage", "inject"))
	dic = compute_img_dictionary(default_list, inject_list)
	dic.update(
		compute_text_dictionary(default_list, inject_list)
	) # add second dictionary
	dic["data"] = get_date() # add date
	generate_html_file(dic)
	print("done.")

main()