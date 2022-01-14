import json
import sys
import copy
import re
import random

# load data
sources = ["yes123", "104", "1111", "hiwork"]
data = []
test_data = []
for s in sources:
    infile = open("jobs_{0}.json".format(s))
    temp = json.load(infile)['jobs']
    data += temp

# preprocessing
city_list = ['南投縣', '台中市', '台南市', '台北市', '台東縣', '嘉義縣', '基隆市', '宜蘭縣', '屏東縣', '彰化縣',
             '新北市', '新竹縣', '桃園市', '澎湖縣', '花蓮縣', '苗栗縣', '金門縣', '雲林縣', '高雄市']
major_lookup = {
    '電機': ['電子', '機械'],
    '電子': ['電子'],
    '工程': ['工程'],
    '資訊': ['資訊'],
    '管理': ['管理'],
    '機械': ['機械'],
    '通訊': ['通訊'],
    '維護': ['維護'],
    '數學': ['數學'],
    '電算機': ['電子', '資訊', '機械', '工程'],
    '化學': ['化學'],
    '通信': ['通訊'],
    '光電': ['光電'],
    '理工': ['數學', '物理', '化學', '工程'],
    '材料': ['材料'],
    '工業': ['工業'],
    '資工': ['資訊', '工程'],
    '設計': ['設計'],
    '生物': ['醫藥'],
    '統計': ['數學'],
    '軟體': ['資訊', '工程'],
    '物理': ['物理'],
    '自然科學': ['物理', '化學'],
    '航太': ['航太'],
    '藥學': ['醫藥'],
    '商業': ['商業'],
    '食品': ['食品'],
    '醫藥': ['醫藥'],
    '網路': ['資訊', '工程'],
    '會計': ['商業'],
    '金融': ['商業'],
    '貿易': ['商業'],
    '行銷': ['商業'],
    '經濟': ['商業'],
    '醫務': ['醫藥'],
    '生醫': ['醫藥']
}
certificate_lookup = {
    'scjp': 'SCJP',
    'db相關': 'DB相關',
    '勞安': '勞安相關',
    '化工': '化學相關',
    '化學': '化學相關',
    '電機': '電機相關',
    '電子': '電子相關',
    'mcsa': 'MCSA',
    'msca': 'MCSA',
    'rhc': 'RHC',
    'ccna': 'CCNA',
    'ceh': "CEH",
    'cisco': 'CCNA',
    '微軟系統管理': 'MCSA',
    'java': 'SCJP',
    'pmp': 'PMP'
}
# 程式語言/library/framework
coding_lookup = {
    '.net': '.NET',
    'activex': 'ActiveX',
    'ajax': 'AJAX',
    'asp': 'ASP',
    'c#': 'C#',
    'c++': 'C++',
    'cgi': 'CGI',
    'css': 'CSS',
    'delphi': 'Delphi',
    'dhtml': 'DHTML',
    'directx': 'DirectX',
    'html': 'HTML',
    'java script': 'javascript',
    'javascript': 'javascript',
    'jquery': 'jQuery',
    'jsp': 'JSP',
    'lotusscript': 'LotusScript',
    'matlab': 'matlab',
    'vb': 'Visual Basic',
    'objective-c': 'Objective-C',
    'php': 'PHP',
    'python': "Python",
    'rpg': 'RPG',
    'ruby': 'Ruby',
    'shell script': 'ShellScript',
    'selenium': 'Selenium',
    'spring': 'Spring',
    'struts': 'Struts',
    'sql': 'SQL',
    'sqr': 'SQR',
    'tcl': 'Tcl',
    'vrml': 'VRML',
    'xhtml': 'XHTML',
    'xml': 'XML'
}
# 軟體/os/其他技能
software_lookup = {
    'abaqus': 'Abaqus',
    'access': 'Microsoft Office',
    'adobe acrobat': 'Adobe Acrobat',
    'aix': 'IBM AIX',
    'android': 'Android',
    'cisco': 'Cisco',
    'data guard': 'Oracle Data Guard',
    'dbase': 'dBase',
    'dos': 'DOS',
    'eclipse': 'Eclipse',
    'excel': 'Microsoft Office',
    'ghost': 'Ghost',
    'git': 'Git',
    'hibernate': 'Hibernate',
    'internet explorer': 'IE',
    'ios': 'iOS',
    'juniper': 'Juniper',
    'labview': 'LabVIEW',
    'linux': 'Linux',
    'mac os': 'MacOS',
    'mongodb': 'MongoDB',
    'ms sql': 'MSSQL',
    'mssql': 'MSSQL',
    'musql': 'MySQL',
    'office': 'Microsoft Office',
    'onenote': 'Microsoft Office',
    'openoffice': 'Apache OpenOffice',
    'outlook': 'Microsoft Office',
    'plc': 'PLC',
    'postgresql': 'PostgreSQL',
    'powerpoint': "Microsoft Office",
    'redisdb': 'RedisDB',
    'sapdb': 'MaxDB',
    'solaris': 'Solaris',
    'unity': 'Unity',
    'unix': 'Linux',
    'visio': 'Microsoft Office',
    'visual studio': 'Visual Studio',
    'win ce': 'Windows CE',
    'windows': 'Windows 10',
    'windows 2000': 'Windows 2000',
    'windows 2003': 'Windows 2003',
    'windows 2008': 'Windows 2008',
    'windows 7': 'Windows 7',
    'windows 95': 'Windows 95',
    'windows 98': 'Windows 98',
    'windows nt': 'Windows nt',
    'windows vista': 'Windows Vista',
    'windows xp': 'Windows XP',
    'word': 'Microsoft Office',
    'wps': 'WPS Office'
}
edu_lookup = {
    '博士': ['博士'],
    '博士以上': ['博士'],
    '博士以上畢業': ['博士'],
    '博士限定此學歷畢業': ['博士'],
    '國小/國中': ['國小', '國中'],
    '大學': ['大學'],
    '大學以上': ['大學', '碩士', '博士'],
    '大學以上畢業': ['大學', '碩士', '博士'],
    '大學限定此學歷': ['大學'],
    '專科': ['專科'],
    '專科以上': ['專科', '大學', '碩士', '博士'],
    '專科以上畢業': ['專科', '大學', '碩士', '博士'],
    '研究所以上': ['碩士', '博士'],
    '碩士': ['碩士'],
    '碩士以上': ['碩士', '博士'],
    '碩士以上畢業': ['碩士', '博士'],
    '碩士限定此學歷': ['碩士'],
    '高中': ['高中職'],
    '高中(職)': ['高中職'],
    '高中(職)以上': ['高中職', '專科', '大學', '碩士', '博士'],
    '高中以上': ['高中職', '專科', '大學', '碩士', '博士'],
    '高中以下': ['高中職', '國中', '國小'],
    '高中職': ['高中職'],
    '高中職以上': ['高中職', '專科', '大學', '碩士', '博士'],
    '高中職以上畢業': ['高中職', '專科', '大學', '碩士', '博士'],
    '國中(含以下)': ['國中', '國小'],
    '不拘': ['國小', '國中', '高中職', '專科', '大學', '碩士', '博士']
}
# edu_lookup = {
#   '博士': '博士',
#   '博士以上': '博士',
#   '博士以上畢業': '博士',
#   '博士限定此學歷畢業': '博士',
#   '國小/國中': '國小',
#   '大學': '大學',
#   '大學以上': '大學',
#   '大學以上畢業': '大學',
#   '大學限定此學歷': '大學',
#   '專科': '專科',
#   '專科以上': '專科',
#   '專科以上畢業': '專科',
#   '研究所以上': '碩士',
#   '碩士': '碩士',
#   '碩士以上': '碩士',
#   '碩士以上畢業': '碩士',
#   '碩士限定此學歷': '碩士',
#   '高中': '高中職',
#   '高中(職)': '高中職',
#   '高中(職)以上': '高中職',
#   '高中以上': '高中職',
#   '高中以下': '國小',
#   '高中職': '高中職',
#   '高中職以上': '高中職',
#   '高中職以上畢業': '高中職',
#   '不拘': '國小'
# }
'''
cate_lookup = {
    '軟體': ['軟體'],
    'internet': ['軟體', '前後端'],
    '維護': ['維護', '操作'],
    '操作': ['操作'],
    'mis': ['軟體', 'MIS', '網路管理', '資安'],
    '網路管理': ['軟體', '網路管理'],
    '電子': ['硬體'],
    '機構': ['機構'],
    '機械': ['機構'],
    '網路程式': ['軟體', '前後端'],
    '韌體': ['軟體', '韌體'],
    '助理': ['助理'],
    '演算法': ['軟體', '演算法'],
    '系統分析': ['軟體', '系統分析'],
    '專案': ['軟體', '專案管理'],
    '主管': ['主管'],
    '通訊': ['通訊'],
    '硬體': ['硬體'],
    '電機': ['機構', '操作', '維護'],
    '資訊設備管制': ['軟體', 'MIS', '網路管理', '資安'],
    '機電': ['機構', '操作', '維護'],
    '網頁': ['軟體', '前後端'],
    '網站': ['軟體', '前後端'],
    '系統規劃分析': ['軟體', '系統分析'],
    '系統工程師': ['軟體', '系統分析'],
    '電玩程式': ['軟體', '遊戲設計'],
    '資料庫': ['軟體', '資料庫'],
    '製程': ['製程'],
    '自動': ['自動化'],
    '測試': ['測試', '操作'],
    '半導體': ['硬體'],
    #'化學': ['化學'],
    '安全': ['軟體', '資安'],
    '作業員': ['作業員'],
    #'材料研發': ['化學', '材料'],
    'mes': ['MES', '維護', '操作', '自動化'],
    'ic': ['硬體', '韌體'],
    '售後': ['FAE', '維護', '操作'],
    'fae': ['FAE', '維護', '操作'],
    '電源': ['電源'],
    #'生物科技': ['醫藥'],
    '業務': ['FAE', '維護', '操作'],
    #'醫藥': ['醫藥'],
    #'食品': ['食品'],
    '生產設備': ['機構', '操作', '維護', '自動化'],
    '生產線': ['機構', '操作', '維護', '自動化'],
    #'rf': ['RF'],
    '維修': ['維護', '操作'],
    'erp': ['ERP'],
    '光電': ['光電'],
    'cad': ['CAD'],
    '光學': ['光電'],
    'pcb': ['pcb', '硬體'],
    #'熱傳': ['熱傳', '機構'],
    '客服': ['FAE', '維護', '操作'],
    '顧問': ['FAE', '維護', '操作'],
    '電子商務': ['商務'],
    '電腦組裝': ['操作', '維護', '作業員'],
    '組裝組立': ['操作', '維護', '作業員'],
    #'工業': ['工業'],
    '客戶服務': ['FAE', '維護', '操作'],
    'bios': ['韌體'],
    '市場': ['商務'],
    '行銷': ['商務'],
    '市場調查': ['商務'],
    'app': ['軟體', 'APP'],
    '資料科學': ['資料科學'],
    '雲端': ['軟體', '雲端'],
    'ar': ['軟體', 'VR/AR'],
    'vr': ['軟體', 'VR/AR'],
    'ai': ['資料科學'],
    'ux': ['軟體', 'UI'],
    'ui': ['軟體', 'UI'],
    '數據': ['資料科學'],
    '物聯網': ['軟體', '韌體', 'IOT'],
    'iot': ['軟體', '韌體', 'IOT'],
    '人工智慧': ['資料科學'],
    'web': ['軟體', '前後端'],
    '深度學習': ['資料科學'],
    '嵌入': ['韌體'],
    'smt': ['smt', '製程'],
    '線路架設': ['線路架設'],
    '品管': ['品管'],
    #'動畫': ['動畫設計'],
    #'保全工程': ['保全工程'],
}
'''

cate_lookup = {
    '軟體': ['軟體'],
    'internet': ['軟體', '前後端'],
    '維護': ['維護', '操作'],
    '操作': ['操作'],
    'mis': ['軟體', 'MIS', '網路管理', '資安'],
    '網路管理': ['軟體', '網路管理'],
    '電子': ['硬體'],
    #'機構': ['機構'],
    #'機械': ['機構'],
    '網路程式': ['軟體', '前後端'],
    '韌體': ['軟體', '韌體'],
    #'助理': ['助理'],
    '演算法': ['軟體', '演算法'],
    '系統分析': ['軟體', '系統分析'],
    '專案': ['軟體', '專案管理'],
    '主管': ['主管'],
    #'通訊': ['通訊'],
    '硬體': ['硬體'],
    #'電機': ['機構', '操作', '維護'],
    '資訊設備管制': ['軟體', 'MIS', '網路管理', '資安'],
    #'機電': ['機構', '操作', '維護'],
    '網頁': ['軟體', '前後端'],
    '網站': ['軟體', '前後端'],
    '系統規劃分析': ['軟體', '系統分析'],
    '系統工程師': ['軟體', '系統分析'],
    '電玩程式': ['軟體', '遊戲設計'],
    '資料庫': ['軟體', '資料庫'],
    #'製程': ['製程'],
    '自動': ['自動化'],
    '測試': ['測試', '操作'],
    '半導體': ['硬體'],
    #'化學': ['化學'],
    '安全': ['軟體', '資安'],
    #'作業員': ['作業員'],
    #'材料研發': ['化學', '材料'],
    #'mes': ['MES', '維護', '操作', '自動化'],
    'ic': ['硬體', '韌體'],
    '售後': ['FAE', '維護', '操作'],
    'fae': ['FAE', '維護', '操作'],
    #'電源': ['電源'],
    #'生物科技': ['醫藥'],
    '業務': ['FAE', '維護', '操作'],
    #'醫藥': ['醫藥'],
    #'食品': ['食品'],
    #'生產設備': ['機構', '操作', '維護', '自動化'],
    #'生產線': ['機構', '操作', '維護', '自動化'],
    #'rf': ['RF'],
    '維修': ['維護', '操作'],
    #'erp': ['ERP'],
    #'光電': ['光電'],
    #'cad': ['CAD'],
    #'光學': ['光電'],
    #'pcb': ['pcb', '硬體'],
    #'熱傳': ['熱傳', '機構'],
    '客服': ['FAE', '維護', '操作'],
    #'顧問': ['FAE', '維護', '操作'],
    '電子商務': ['商務'],
    '電腦組裝': ['操作', '維護', '作業員'],
    '組裝組立': ['操作', '維護', '作業員'],
    #'工業': ['工業'],
    '客戶服務': ['FAE', '維護', '操作'],
    'bios': ['韌體'],
    '市場': ['商務'],
    '行銷': ['商務'],
    '市場調查': ['商務'],
    'app': ['軟體', 'APP'],
    '資料科學': ['資料科學'],
    '雲端': ['軟體', '雲端'],
    'ar': ['軟體', 'VR/AR'],
    'vr': ['軟體', 'VR/AR'],
    'ai': ['資料科學'],
    'ux': ['軟體', 'UI'],
    'ui': ['軟體', 'UI'],
    '數據': ['資料科學'],
    #'物聯網': ['軟體', '韌體', 'IOT'],
    #'iot': ['軟體', '韌體', 'IOT'],
    '人工智慧': ['資料科學'],
    'web': ['軟體', '前後端'],
    '深度學習': ['資料科學'],
    '嵌入': ['韌體'],
    #'smt': ['smt', '製程'],
    #'線路架設': ['線路架設'],
    #'品管': ['品管'],
    #'動畫': ['動畫設計'],
    #'保全工程': ['保全工程'],
}

def find_min_cate(cate_amount):
    minimum = 1e10
    min_cate = None
    for key, value in cate_amount.items():
        if value < minimum:
            minimum = value
            min_cate = key
    return min_cate, minimum

rm_index = []
remain_cate = list(set([item for key, value in cate_lookup.items() for item in value]))
cate_amount = {item: 0 for item in remain_cate}
for i in range(len(data)):
    data[i]['companyCity'] = data[i]['companyCity'][:3]
    if data[i]['companyCity'] not in city_list:
        if data[i]['companyCity'] == '嘉義市':
            data[i]['companyCity'] = '嘉義縣'
        elif data[i]['companyCity'] == '新竹市':
            data[i]['companyCity'] = '新竹縣'
        else:
            rm_index.append(i)
            continue

    data[i]['jobCategory'].append(data[i]['jobName'])
    result_cate = set()
    for cate in data[i]['jobCategory']:
        for key, value in cate_lookup.items():
            if key in cate.lower():
                for sub_cat in value:
                    result_cate.add(sub_cat)
    data[i]['jobCategory'] = list(result_cate)
    for item in result_cate:
        cate_amount[item] += 1
    if len(result_cate) == 0:
        rm_index.append(i)
        continue

    if type(data[i]['jobSalary']) is str:
        data[i]['jobSalary'] = int(data[i]['jobSalary'])
    # if data[i]['jobSalary'] == 0:
    #   rm_index.append(i)
    #   continue

    if type(data[i]['eduLevel']) is not list:
        data[i]['eduLevel'] = data[i]['eduLevel'].split("、")
    if len(data[i]['eduLevel']) == 0 or data[i]['eduLevel'][0].strip() == '無限制':
        data[i]['eduLevel'] = ['國小']
    elif len(data[i]['eduLevel']) > 0:
        result_edu = set()
        for edu in data[i]['eduLevel']:
            l = edu_lookup[edu]
            for item in l:
                result_edu.add(item)
        data[i]['eduLevel'] = list(result_edu)

    if data[i]['workingExp'].strip() == '不拘':
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
    if len(data[i]['acceptIdentity']) == 0 or data[i]['acceptIdentity'][0].strip() == '不拘':
        data[i]['acceptIdentity'] = []
    elif len(data[i]['acceptIdentity']) > 0:
        split_list = []
        for j in range(len(data[i]['acceptIdentity'])):
            if "/" in data[i]['acceptIdentity']:
                l = data[i]['acceptIdentity'][j].split("/")
                data[i]['acceptIdentity'] += [item.strip() for item in l]
                split_list.append(j)
            else:
                data[i]['acceptIdentity'][j] = data[i]['acceptIdentity'][j].strip()
        for index in reversed(split_list):
            data[i]['acceptIdentity'].pop(index)

    if len(data[i]['acceptMajor']) == 0 or data[i]['acceptMajor'][0].strip() == '不拘':
        data[i]['acceptMajor'] = []
    elif len(data[i]['acceptMajor']) > 0:
        result_major = set()
        for major in data[i]['acceptMajor']:
            for key, value in major_lookup.items():
                if key in major:
                    for sub_cat in value:
                        result_major.add(sub_cat)
        data[i]['acceptMajor'] = list(result_major)
        if len(result_major) == 0:
            rm_index.append(i)
            continue

    if len(data[i]['language']) == 0 or data[i]['language'][0].strip() == '不拘':
        data[i]['language'] = []
    elif len(data[i]['language']) > 0:
        for j in range(len(data[i]['language'])):
            if "多益" in data[i]['language'][j]:
                data[i]['language'][j] = "TOEIC"
            elif "托福" in data[i]['language'][j]:
                data[i]['language'][j] = "TOFEL"
            elif "雅思" in data[i]['language'][j]:
                data[i]['language'][j] = "IELTS"

    if len(data[i]['codingLanguage']) == 0 or data[i]['codingLanguage'][0].strip() == '不拘':
        data[i]['codingLanguage'] = []
    elif len(data[i]['codingLanguage']) > 0:
        result_coding = set()
        for lang in data[i]['codingLanguage']:
            lang = lang.strip().lower()
            if lang in ("c", "c語言"):
                result_coding.add("C")
                continue
            if lang == "java":
                result_coding.add("Java")
                continue
            if lang in ("r", "r語言"):
                result_coding.add("R")
                continue
            if lang == "vb script":
                result_coding.add("VBScript")
                continue
            if lang == "vba":
                result_coding.add("VBA")
                continue
            if lang == "dreamweaver":
                data[i]['software'].append("dreamweaver")
                continue
            if lang == "frontpage":
                data[i]['software'].append("frontpage")
                continue
            if lang == "powerbuilder":
                data[i]['software'].append("powerbuilder")
                continue
            if "visual" in lang:
                data[i]['software'].append("visual studio")
            for key, value in coding_lookup.items():
                if key in lang:
                    result_coding.add(value)
        data[i]['codingLanguage'] = list(result_coding)

    if len(data[i]['certification']) == 0 or data[i]['certification'][0].strip() == '不拘':
        data[i]['certification'] = []
    elif len(data[i]['certification']) > 0:
        result_cer = set()
        for certificate in data[i]['certification']:
            for key, value in certificate_lookup.items():
                if key in certificate:
                    result_cer.add(value)
        data[i]['certification'] = list(result_cer)

    if len(data[i]['software']) == 0 or data[i]['software'][0].strip() == '不拘':
        data[i]['software'] = []
    elif len(data[i]['software']) > 0:
        result_software = set()
        for software in data[i]['software']:
            software = software.strip().lower()
            if software == "angular" and "Angular" not in data[i]['codingLanguage']:
                data[i]['codingLanguage'].append("Angular")
                continue
            if software == "react" and "React" not in data[i]['codingLanguage']:
                data[i]['codingLanguage'].append("React")
                continue
            if software == "vue" and "Vue" not in data[i]['codingLanguage']:
                data[i]['codingLanguage'].append("Vue")
                continue
            if software == 'app':
                if 'ios' in data[i]['software']:
                    if "Objective-C" not in data[i]['codingLanguage']:
                        data[i]['codingLanguage'].append("Objective-C")
                    if "Swift" not in data[i]['codingLanguage']:
                        data[i]['codingLanguage'].append("Swift")
                elif "Java" not in data[i]['codingLanguage']: # android or not mentioned
                    data[i]['codingLanguage'].append("Java")
                continue
            if software == "asp.net":
                if "asp" not in data[i]['codingLanguage']:
                    data[i]['codingLanguage'].append("ASP")
                if ".NET" not in data[i]['codingLanguage']:
                    data[i]['codingLanguage'].append(".NET")
                continue
            if software == "shell":
                result_software.add('Linux')
                continue
            if software == "springboot":
                if "Spring" not in data[i]['codingLanguage']:
                    data[i]['codingLanguage'].append("Spring")
                result_software.add('SpringBoot')
                continue
            if software == "struts1":
                if "Struts" not in data[i]['codingLanguage']:
                    data[i]['codingLanguage'].append("Struts")
                continue
            if software == "visual foxpro":
                if "FoxPro" not in data[i]['codingLanguage']:
                    data[i]['codingLanguage'].append("FoxPro")
                result_software.add('Visual Studio')
                continue
            if "sql" in software and "SQL" not in data[i]['codingLanguage']:
                data[i]['codingLanguage'].append("SQL")
            for key, value in software_lookup.items():
                if key in software:
                    result_software.add(value)
        data[i]['software'] = list(result_software)

    for other in data[i]['other']:
        other = other.lower()
        for key, value in coding_lookup.items():
            if key in other and value not in data[i]['codingLanguage']:
                data[i]['codingLanguage'].append(value)
        for key, value in software_lookup.items():
            if key in other and value not in data[i]['software']:
                data[i]['software'].append(value)

# prepare testing data
i = random.randint(1, len(data) - 1)
last = i - 1
while i != last:
    if i not in rm_index:
        include = False
        if len(data[i]['codingLanguage']) > 0 and len(data[i]['software']) > 0:
            for cate in data[i]['jobCategory']:
                if cate in remain_cate:
                    include = True
                    remain_cate.remove(cate)
                    cate_amount[cate] -= 1
            if include:
                test_data.append(data[i])
                rm_index.append(i)
    i += 1
    if i == len(data):
        i = 0

for index in sorted(rm_index, reverse=True):
    data.pop(index)
'''
# balance data
standard = 0
standard_cate = None
for key, value in cate_amount.items():
    if value > standard:
        standard = value
        standard_cate = key
print("standard: {0} {1}".format(standard_cate, standard))
i = random.randint(0, len(data) - 1)
while True:
    key, value = find_min_cate(cate_amount)
    if value >= standard:
        break
    while True:
        is_target = False
        if key in data[i]['jobCategory']:
            is_target = True
        if is_target:
            new_data = copy.deepcopy(data[i])
            for cate in new_data['jobCategory']:
                if cate_amount[cate] >= standard:
                    new_data['jobCategory'].remove(cate)
                else:
                    cate_amount[cate] += 1
            data.append(new_data)
            break
        i = random.randint(0, len(data) - 1)
    i = random.randint(0, len(data) - 1)
    # print("{0} finished: {1}".format(key, value))
'''
sort = list(cate_amount.items())
sort.sort(key=lambda x: x[1], reverse=True)
for key, value in sort:
    print("{0}: {1}".format(key, value))
#'''

# to_json
print(len(data), len(test_data), len(rm_index))
with open("all.json", 'w', encoding='utf8') as outfile:
    json.dump(data + test_data, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
with open("train.json", 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
with open("test.json", 'w', encoding='utf8') as outfile:
    json.dump(test_data, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
print(remain_cate)
