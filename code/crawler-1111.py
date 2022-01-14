import requests
from bs4 import BeautifulSoup
import json
import string
from time import sleep
import re
import random

INTERVAL = 0.5
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    ]
# headers = {	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8'}
headers = {'User-agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"}
# { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
# URL_BASE = "https://www.1111.com.tw/"
page = 1
max_page = 150
base_url = "https://www.1111.com.tw/job-bank/job-index.asp?si=1&ss=s&d0=140200,140300,140400,140100&page="
count_data = 0
resultList = {'jobs': []}  # the data save to json
file_count = 1
keyword_major = ["電機", "電子", "資工", "通訊", "資訊工程", "工業工程", "應用數學", "理工", "資訊與設計系", "資訊科技學系",
                 "資訊科學學系", "資訊管理學系"]
keyword_language = ["多益", "TOEIC", "托福", "TOFEL", "iBT", "雅司", "IELTS"]
keyword_codingLanguage = ["Javascript", "R", "C++", "C語言", "Python", "HTML", "CSS", "SQL", "VBA", "python", "JAVA", 
                          "C#", "shell script", "Java Script", "Java", "PHP", "Visual Basic", ".net", "JavaScript", 
                          "Verilog", "Perl", "Objective-C"]
keyword_software = ["OFFICE", "EXCEL", "Labview", "PLC", "Visual Studio", "ASP.NET", "github", "Linux", "Juniper",
                    "VueJs", "AngularJS", "Git", "git", "AD", "Office", "Windows", "windows", "Server", "server",
                    "GIT", "docker", "MongoDB", "Word", "PowerPoint", "Excel", "Outlook", "jQuary", "jupyter", "Android",
                    "iOS", "OpenGL", "OpenCV", "RedisDB", "Struts1", "Spring", "Hibernate", "SpringBoot", "Eclipse", "AWS",
                     "Office", "App", "Unity", "MSSQL", "MySQL", "XCode"]
keyword_remove = ["報名", "面試", "時間", "工作待遇", "底薪", "月薪", "分紅", "業績", "補充", "條件", "面議", "吃苦耐勞",
                  "處理問題", "團隊", "合作能力", "溝通", "敏捷", "擅長工具", "積極", "責任心", "公司", "抗壓", "跨領域", "合作",
                  "書面審查", "畢業證書", "職缺", "輪值", "輪班", "加班", "未填寫", "PDF", "必要", "加分", "不拘"]
keyword_certification = ["證照"]
keywords_set = [keyword_major, keyword_language, keyword_codingLanguage, keyword_certification, keyword_software]
# something wrong with these url
keyword_pass = ["http://www.1111.com.tw/job/85235641/", "http://www.1111.com.tw/job/85230191/",
                "http://www.1111.com.tw/job/85049382/", "http://www.1111.com.tw/job/86023633/",
                "http://www.1111.com.tw/job/77113261/", "http://www.1111.com.tw/job/80240579/",
                "http://www.1111.com.tw/job/79825902/", "http://www.1111.com.tw/job/85994233/",
                "http://www.1111.com.tw/job/80273120/", "http://www.1111.com.tw/job/80273114/",
                "http://www.1111.com.tw/job/91211541/"]


def saveJson():
    global file_count
    with open("jobs_1111_" + str(file_count) + ".json", 'w', encoding='utf8') as outfile:
        json.dump(resultList, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
        # use .decode to turn it back


def crawContent(link, companyName):
    global count_data
    # init variables
    jobFullLink = "http://" + link.get('href')[2:]
    jobName = link.get('title')
    jobCategory = []
    companyCity = ""
    jobSalary = 0
    eduLevel = []
    acceptMajor = []
    acceptIdentity = []
    workingExp = ""
    certification = []
    others = []
    language = []
    codingLanguage = []
    software = []

    # print out message
    print("crawing content of: " + jobName + "\n" + jobFullLink)

    # start crawing
    sleep(INTERVAL)
    res = requests.get(jobFullLink, headers=headers, timeout=10)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html5lib')
    contentList = soup.find('div', {'class': 'floatL w65'}).find_all('ul', {'class': 'dataList'})

    # 0: 工作內容
    liList = contentList[0].findAll('li')
    pList = liList[0].findAll('p')
    for p in pList:
        others.append(p.text[:-1])

    for li in liList[1:]:
        try:
            title = li.find('div', {'class': 'listTitle'}).contents[0]
            if title == "工作地點：":
                companyCity = li.find('div', {'class': 'listContent'}).contents[0].split()[0]
                # print("city: " + companyCity)
            elif title == "職務類別：":
                jobCategory = [cate.contents[0] for cate in li.findAll('div', {'class': 'category'})]
                print(jobCategory)
            elif title == "工作待遇：":
                jobSalary = li.find('div', {'class': 'listContent'}).contents[0]
                if "面議" in jobSalary:
                    jobSalary = li.find('div', {'class': 'listContent'}).contents[2]
                    result = re.search(r"\d+", jobSalary)
                    time = jobSalary.split("/")[1]
                    if "年" in time:
                        jobSalary = int(int(result[0]) / 12) * 10000
                    elif "月" in time:
                        jobSalary = int(result[0]) * 10000
                    elif "週" in time:
                        jobSalary = int(result[0]) * 4
                    elif "日" in time:
                        jobSalary = int(result[0]) * 30
                    elif "時" in time:
                        jobSalary = int(result[0]) * 8 * 30
                else:
                    time = jobSalary
                    jobSalary = int(jobSalary.split()[1][:-1].replace(',', ''))
                    if "年薪" in time:
                        jobSalary = int(jobSalary / 12)
                    elif "月薪" in time:
                        pass
                    elif "週薪" in time:
                        jobSalary = jobSalary * 4
                    elif "日薪" in time:
                        jobSalary = jobSalary * 30
                    elif "時薪" in time:
                        jobSalary = jobSalary * 8 * 30
                # print("salary: " + str(jobSalary))
        except:
            continue

    # 1: 要求條件
    liList = contentList[1].findAll('li')
    for li in liList:
        try:
            title = li.find('div', {'class': 'listTitle'}).contents[0]
            if title == "身份類別：":
                acceptIdentity = li.find('div', {'class': 'listContent'}).contents[0].split("／")
                # print("identity: " + acceptIdentity)
            elif title == "學歷限制：":
                eduLevel = li.find('div', {'class': 'listContent'}).contents[0].split("、")
                # print("edu: " + eduLevel)
            elif title == "科系限制：":
                acceptMajor = [ major.text[1:] for major in li.findall('a') ]
                # print("accM: " + acceptMajor)
            elif title == "工作經驗：":
                workingExp = li.find('div', {'class': 'listContent'}).contents[0]
                # print("wE: " + workingExp)
            elif title == "需有駕照：":
                certification = li.find('div', {'class': 'listContent'}).contents[0].split("、")
                # print("cer: " + certification)
            elif title == "附加條件：":
                pList = li.find('div', {'class': 'listContent'}).findAll('p')
                for p in pList:
                    others.append(p.contents[0][:-1])
                # print(others)
        except:
            continue

    # 2: 應徵方式、3: hashtag、4: 看過此工作的人還看過 -> 這些我沒抓

    # print(others)

    # deal with messy 'other'
    # correspond_set = [acceptMajor, language, codingLanguage, certification, software]
    remove = []
    for oID, other in enumerate(others):
        if other == "":
            remove.append(oID)
        else:
            # deal with the start of 'other'
            while other[:1].isdigit():
                other = other[1:]
                # print("??: (" + other[0] + ")")
                others[oID] = other
                # print("ori: " + other)

            # remove those not belongs to others
            for setID, keywords in enumerate(keywords_set):
                for keyword in keywords:
                    if keyword in other:
                        print_check = keyword + " in "
                        if setID is 0:
                            if keyword not in acceptMajor:
                                if "不拘" in acceptMajor or len(acceptMajor) == 0:
                                    acceptMajor = [keyword]
                                else:
                                    acceptMajor += [keyword]
                                print_check = print_check + "major"
                        elif setID is 1:
                            if keyword not in language:
                                if "不拘" in language or len(language) == 0:
                                    language = [keyword]
                                else:
                                    language += [keyword]
                                print_check = print_check + "language"
                        elif setID is 2:
                            if keyword not in codingLanguage:
                                if "不拘" in codingLanguage or len(codingLanguage) == 0:
                                    codingLanguage = [keyword]
                                else:
                                    codingLanguage += [keyword]
                                print_check = print_check + "codingLanguage"
                        elif setID is 3:
                            if keyword not in certification and len(other) < 15:
                                if "不拘" in certification or len(certification) == 0:
                                    certification = [other]
                                else:
                                    certification += [other]
                                print_check = print_check + "certification"
                        else:
                            if keyword not in software:
                                if "不拘" in software or len(software) == 0:
                                    software = [keyword]
                                else:
                                    software += [keyword]
                                print_check = print_check + "software"

                        remove.append(oID)
                        print_check = print_check + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        # print(print_check)

            for keyword in keyword_remove:
                if keyword in other:
                    remove.append(oID)

    if remove != []:
        remove = list(set(remove))
        remove.sort()
        remove.reverse()
        print(remove)
        for r in remove:
            others.remove(others[r])

    # print to check before save
    print("city: " + companyCity)
    print("category: {0}".format(jobCategory))
    print("salary: " + str(jobSalary))
    print("identity: {0}".format(acceptIdentity))
    print("eduLevel: {0}".format(eduLevel))
    print("accM: {0}".format(acceptMajor))
    print("workExp: " + workingExp)
    print("cer: {0}".format(certification))
    print("language: {0}".format(language))
    print("codingLanguage: {0}".format(codingLanguage))
    print("software: {0}".format(software))
    print(others)

    # save data
    temp = {
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
        'other': others,
        'jobFullLink': jobFullLink
    }
    if jobSalary != "":
        resultList['jobs'].append(temp)
    else:
        count_data = count_data - 1

    # print out message
    print("fin crawing content of: " + jobName + "\n")


def crawlTitle(url):
    global count_data, file_count, headers

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # res.encoding = 'big5'
    soup = BeautifulSoup(res.text, 'html5lib')
    base_soup = soup.find('ul', {'class': 'halfbox'})
    paginationList = base_soup.find_all('a', {'class': 'mobiFullLInk'})
    companyNameList = base_soup.find_all('div', {'class': 'jbInfoin'})
    nextUrl = ''
    for linkid, link in enumerate(paginationList):
        count_data = count_data + 1
        # print(link)
        companyName = companyNameList[linkid].find('h4').find('a').get('title')[6:].split()[0]
        # print(companyName)
        if "http://" + link.get('href')[2:] not in keyword_pass:
            crawContent(link, companyName)

        if count_data % 100 is 0:
            saveJson()
            file_count = file_count + 1


if __name__ == '__main__':
    page = 146
    while page <= max_page:
        print("================\npage: " + str(page))
        print("total data count now: " + str(count_data))
        print("================\n\n")
        url = base_url + str(page)
        crawlTitle(url)
        page = page + 1
        if page % 1 == 0:
            saveJson()
            file_count = file_count + 1

    # also save in case the last bunch of data is less than 300
    saveJson()

    print("\ntotal data count: " + str(count_data))
