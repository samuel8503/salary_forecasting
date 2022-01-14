import pandas as pd
import json
import sys
import copy
import re

def get_data_proto(
	companyName = None,
    companyCity = None,
    jobName = None,
    jobCategory = None,
    jobSalary = None,
    eduLevel = None,
    workingExp = None,
    acceptIdentity = None,
    acceptMajor = None,
    language = None,
    codingLanguage = None,
    certification = None,
    software = None,
    other = None,
    jobFullLink = None
):
	return {
        'companyName': companyName,
        'companyCity': companyCity,
        'jobName': jobName,
        'jobCategory': jobCategory,
        'jobSalary': jobSalary,
        'eduLevel': eduLevel,
        'workingExp': workingExp,
        'acceptIdentity': acceptIdentity,
        'acceptMajor': acceptMajor,
        'language': language,
        'codingLanguage': codingLanguage,
        'certification': certification,
        'software': software,
        'other': other,
        'jobFullLink': jobFullLink
    }

# load data
sources = ["hiwork", "yes123", "104", "1111"]
data = []
for s in sources:
	infile = open("jobs_{0}.json".format(s))
	temp = json.load(infile)['jobs']
	for t in temp:
		t['source'] = s
	data += temp

# preprocessing
for i in range(len(data)):
	data[i]['companyCity'] = data[i]['companyCity'][:3]

	if len(data[i]['jobCategory']) == 0:
		data[i]['jobCategory'] = '未知'
	elif len(data[i]['jobCategory']) > 0:
		for j in range(1, len(data[i]['jobCategory'])):
			data += [get_data_proto(jobCategory=data[i]['jobCategory'][j].strip())]
		data[i]['jobCategory'] = data[i]['jobCategory'][0].strip()

	if data[i]['jobSalary'] == 0:
		data[i]['jobSalary'] = None

	if type(data[i]['eduLevel']) is not list:
		data[i]['eduLevel'] = data[i]['eduLevel'].split("、")
	if len(data[i]['eduLevel']) == 0 or data[i]['eduLevel'][0] == '無限制':
		data[i]['eduLevel'] = '不拘'
	elif len(data[i]['eduLevel']) > 0:
		for j in range(1, len(data[i]['eduLevel'])):
			# if '以上' in data[i]['eduLevel'][j]:
			# 	data[i]['eduLevel'][j] = data[i]['eduLevel'][j][:-2]
			data += [get_data_proto(eduLevel=data[i]['eduLevel'][j].strip())]
		data[i]['eduLevel'] = data[i]['eduLevel'][0].strip()

	if data[i]['workingExp'] == '不拘':
		data[i]['workingExp'] = 0.0
	else:
		result = re.search(r"\d+", data[i]['workingExp'])
		try:
			if not result:
				if '半年' in data[i]['workingExp']:
					data[i]['workingExp'] = 0.5
				elif '無工作經驗可' in data[i]['workingExp']:
					data[i]['workingExp'] = 0
			else:
				data[i]['workingExp'] = float(result[0])
		except Exception as e:
			print(e, data[i]['workingExp'])
			sys.exit()

	if type(data[i]['acceptIdentity']) is not list:
		data[i]['acceptIdentity'] = data[i]['acceptIdentity'].split(",")
	if len(data[i]['acceptIdentity']) == 0:
		data[i]['acceptIdentity'] = '不拘'
	elif len(data[i]['acceptIdentity']) > 0:
		for j in range(1, len(data[i]['acceptIdentity'])):
			data += [get_data_proto(acceptIdentity=data[i]['acceptIdentity'][j].strip())]
		data[i]['acceptIdentity'] = data[i]['acceptIdentity'][0].strip()

	if len(data[i]['acceptMajor']) == 0 or data[i]['acceptMajor'][0] == '不拘':
		data[i]['acceptMajor'] = '不拘'
	elif len(data[i]['acceptMajor']) > 0:
		for j in range(1, len(data[i]['acceptMajor'])):
			data += [get_data_proto(acceptMajor=data[i]['acceptMajor'][j].strip())]
		data[i]['acceptMajor'] = data[i]['acceptMajor'][0].strip()

	if len(data[i]['language']) == 0:
		data[i]['language'] = '不拘'
	elif len(data[i]['language']) > 0:
		for j in range(1, len(data[i]['language'])):
			if "多益" in data[i]['language'][j]:
				data[i]['language'][j] = "TOEIC"
			elif "托福" in data[i]['language'][j]:
				data[i]['language'][j] = "TOFEL"
			elif "雅思" in data[i]['language'][j]:
				data[i]['language'][j] = "IELTS"
			data += [get_data_proto(language=data[i]['language'][j].strip())]
		if "多益" in data[i]['language'][0]:
			data[i]['language'] = "TOEIC"
		elif "托福" in data[i]['language'][0]:
			data[i]['language'] = "TOFEL"
		elif "雅思" in data[i]['language'][0]:
			data[i]['language'] = "IELTS"
		else:
			data[i]['language'] = data[i]['language'][0].strip()

	if len(data[i]['codingLanguage']) == 0:
		data[i]['codingLanguage'] = '不拘'
	elif len(data[i]['codingLanguage']) > 0:
		for j in range(1, len(data[i]['codingLanguage'])):
			if data[i]['codingLanguage'][j].lower() == "c語言":
				data[i]['codingLanguage'][j] = "c"
			data += [get_data_proto(codingLanguage=data[i]['codingLanguage'][j].lower().strip())]
		if data[i]['codingLanguage'][0].lower() == "c語言":
				data[i]['codingLanguage'] = "c"
		data[i]['codingLanguage'] = data[i]['codingLanguage'][0].lower().strip()

	if len(data[i]['certification']) == 0:
		data[i]['certification'] = '不拘'
	elif len(data[i]['certification']) > 0:
		for j in range(1, len(data[i]['certification'])):
			data += [get_data_proto(certification=data[i]['certification'][j].strip())]
		data[i]['certification'] = data[i]['certification'][0].strip()

	if len(data[i]['software']) == 0:
		data[i]['software'] = '不拘'
	elif len(data[i]['software']) > 0:
		for j in range(1, len(data[i]['software'])):
			data += [get_data_proto(software=data[i]['software'][j].lower().strip())]
		data[i]['software'] = data[i]['software'][0].lower().strip()

# to_csv
df = pd.DataFrame(data)
df.to_csv("jobs_hi.csv", encoding='utf-8-sig')