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
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
from_data = {
    'search_work': '軟體／工程',
    'find_work_mode1': '2_1011_0001_0000',
    'find_work_mode2': '2_1011_0002_0000',
    's_find_work_mode1': '軟體／工程全部',
    's_find_work_mode2': 'MIS／網管全部',
    'order_by': 'neworder',
    'order_ascend': 'desc',
    'strrec': '0',
    'search_type': 'job',
    'search_item': '1',
    'search_from': 'joblist',
    'job_show_type': 'L',
    'search_job_t': '1'
}
page = 1
rec_per_page = 30
url = "https://www.yes123.com.tw/admin/job_refer_list.asp"
count_data = 0
resultList = {'jobs': []}  # the data save to json
file_count = 1
keyword_major = ["電機", "電子", "資工", "通訊", "資訊工程", "工業工程", "應用數學", "理工", "資訊與設計系", "資訊科技學系",
                 "資訊科學學系", "資訊管理學系"]
keyword_language = ["多益", "TOEIC", "托福", "TOFEL", "iBT", "雅司", "IELTS"]
keyword_codingLanguage = ["javascript", "c++", "c語言", "python", "html", "css", "sql", "vba", "c#", "shell script",
                          "php", ".net", "r語言", "java script"]
keyword_software = ["office", "excel", "labview", "plc", "visual studio", "asp.net", "github", "linux", "juniper",
                    "vue", "angular", "react", "git", "ad", "office", "windows", "server", "redisdb", "struts1", "mysql"
                    "docker", "mongodb", "word", "powerpoint", "excel", "outlook", "app", "unity", "mssql", "aws"
                    "spring", "hibernate", "springboot", "eclipse"]
keyword_remove = ["報名", "面試", "時間", "工作待遇", "底薪", "月薪", "分紅", "業績", "補充", "條件", "面議", "吃苦耐勞",
                  "處理問題", "團隊", "合作能力", "溝通", "敏捷", "擅長工具", "積極", "責任心", "公司", "抗壓", "跨領域", "合作",
                  "書面審查", "畢業證書", "職缺", "輪值", "輪班", "加班", "未填寫", "PDF", "必要", "加分", "不拘", "熱情"]
keyword_certification = ["證照"]
keywords_set = [keyword_major, keyword_language, keyword_codingLanguage, keyword_certification, keyword_software]
# something wrong with these url
keyword_pass = ["https://www.yes123.com.tw/admin/job_refer_comp_job_detail2.asp?p_id=5414806_89540085&job_id=20191121180035770260"]


def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False


def saveJson():
    global file_count
    with open("jobs_yes123_" + str(file_count) + ".json", 'w', encoding='utf8') as outfile:
        json.dump(resultList, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
        # use .decode to turn it back


def crawContent(jobFullLink, jobName, companyName):
    global count_data
    # init variables
    # jobFullLink = "https://www.yes123.com.tw/admin/" + link.get('href')
    # jobName = link.text
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
    print("crawing content of: " + jobName + "\ncompany:" + companyName + "\nlink:" + jobFullLink)

    # start crawing
    sleep(INTERVAL)
    res = requests.get(jobFullLink, headers=headers, timeout=10)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html5lib')
    contentList = soup.find('div', {'class': 'left'}).find_all('div', {'class': 'comp_detail'})

    for content in contentList:
        title = content.find('h2').text
        if "徵才說明" in title:
            liList = content.findAll('li')
            for li in liList:
                try:
                    title = li.find('span', {'class': 'tt'}).text # .split('：')[0].strip()
                    if "工作地點" in title:
                        companyCity = li.find('span', {'class': 'rr'}).text.split()[0]
                        # print("city: " + companyCity)
                    elif "職務類別" in title:
                        jobCategory = li.find('span', {'class': 'rr'}).text[:-6].split()
                    elif "薪資待遇" in title:
                        jobSalary = li.find('span', {'class': 'rr'}).text.split()
                        if len(jobSalary) == 1:
                            jobSalary = 0
                        elif "按件計酬" in jobSalary[0]:
                            return
                        else:
                            time = jobSalary[0]
                            jobSalary = int(jobSalary[1].replace(',', ''))
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
                except:
                    continue
        elif "工作條件" in title:
            liList = content.findAll('li')
            for li in liList:
                try:
                    title = li.find('span', {'class': 'tt'}).text # .split('：')[0].strip()
                    if "身份類別" in title:
                        acceptIdentity = li.find('span', {'class': 'rr'}).text.strip().split()
                        # print("identity: " + acceptIdentity)
                    elif "學歷要求" in title:
                        eduLevel = li.find('span', {'class': 'rr'}).text.strip().split("、")
                        # print("edu: " + eduLevel)
                    elif "科系要求" in title:
                        acceptMajor = li.find('span', {'class': 'rr'}).text[:-6].strip().split("、")
                        # print("accM: " + acceptMajor)
                    elif "工作經驗" in title:
                        workingExp = li.find('span', {'class': 'rr'}).text.strip()
                        # print("wE: " + workingExp)
                except:
                    continue
        elif "技能與求職專長" in title:
            liList = content.findAll('li')
            i = 0
            while i < len(liList):
                 
                title = liList[i].find('span', {'class': 'tt'}).text
                if "電腦技能" in title:
                    title = None
                    while title is None:
                        cate = liList[i].find('span', {'class': 'rr'}).text.strip()
                        print(cate)
                        if "程式設計" in cate:
                            codingLanguage += cate[5:].strip().split("／")
                        elif "網頁技術" in cate:
                            codingLanguage += cate[5:].strip().split("／")
                        elif "作業系統" in cate:
                            software += cate[5:].strip().split("／")
                        elif "資料庫" in cate:
                            software += cate[4:].strip().split("／")
                        elif "辦公室應用" in cate:
                            software += cate[6:].strip().split("／")
                        elif "未填寫" not in cate:
                            others += cate.split("、")
                        
                        i += 1
                        if i == len(liList):
                            break
                        title = liList[i].find('span', {'class': 'tt'})
                    i -= 1
                elif "工作技能" in title:
                    lines = liList[i].find('span', {'class': 'rr'}).text.split("\n")
                    for line in lines:
                        others += line.split("、")
                elif "具備駕照" in title:
                    certification += liList[i].find('span', {'class': 'rr'}).text.strip().split("、")
                i += 1
        elif "其他條件" in title:
            others += content.find('li').text.split("\n")

    # deal with messy 'other'
    # correspond_set = [acceptMajor, language, codingLanguage, certification, software]
    
    remove = []
    for oID, other in enumerate(others):
        if other.strip() == "":
            remove.append(oID)
        else:
            # deal with the start of 'other'
            while other[:1].isdigit():
                other = other[1:]
                # print("??: (" + other[0] + ")")
                others[oID] = other
                # print("ori: " + other)
            allR = [m.start() for m in re.finditer("R", other)]
            for r in allR:
                if "r&d" not in other.lower():
                    is_R = True
                    if r + 1 < len(other):
                        if other[r + 1].isalpha():
                            is_R = False

                    if r != 0:
                        if other[r - 1].isalpha():
                            is_R = False

                    if is_R:
                        # print("R:!!!!!: " + other[r-2:r+2])
                        remove.append(oID)
                        if "R" not in codingLanguage:
                            codingLanguage += ["R"]

            other = other.lower()
            others[oID] = other
            # print(other)
            allJava = [m.start() for m in re.finditer("java", other)]
            for java in allJava:
                is_Java = True
                # print(other[java + 4])
                # print(other[java + 4:java + 10])
                if java + 4 < len(other):
                    if is_alpha(other[java + 4]):  # other[java + 4].is_alpha():
                        is_Java = False
                if java + 10 < len(other):
                    if other[java + 5:java + 11] == "script" or other[java + 4: java + 10] == "script":
                        is_Java = False
                if java != 0:
                    if is_alpha(other[java - 1]):  # .is_alpha():
                        is_Java = False

                if is_Java:
                    # print("Java:!!!!!: " + other[java - 2:java + 4])
                    remove.append(oID)
                    if "java" not in codingLanguage:
                        codingLanguage += ["java"]

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
                        print(print_check)

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


def crawlTitle(url, from_data):
    global count_data, file_count, headers

    res = requests.post(url, headers=headers, data=from_data)
    res.encoding = 'utf-8'
    # res.encoding = 'big5'
    soup = BeautifulSoup(res.text, 'html5lib')
    base_soup = soup.find('div', {'class': 'box_detail_left'})
    if base_soup is None:
        return False
    paginationList = base_soup.find_all('a', {'class': 'jobname'})
    companyNameList = base_soup.find_all('a', {'class': 'bsname'})
    nextUrl = ''
    for linkid, link in enumerate(paginationList):
        count_data = count_data + 1
        companyName = companyNameList[linkid].get('title')
        if companyName is None:
            count_data -= 1
            continue
        print("{0}. CompanyName: {1}, Link: {2}".format(count_data, companyName, link))

        if "ad_rc" in link.get('href'):
            href = "https://www.yes123.com.tw" + link.get('href')[link.get('href').find("|@") + 2 : -2]
            print(href)
        else:
            href = "https://www.yes123.com.tw/admin/" + link.get('href')
        
        if href not in keyword_pass:
            crawContent(href, link['title'], companyName)

        if count_data % 20 == 0:
            USER_AGENT = random.choice(USER_AGENT_LIST)
            print(USER_AGENT)
            headers = {'User-agent': USER_AGENT}

    return True


if __name__ == '__main__':
    while crawlTitle(url, from_data):
        print("================\npage: " + str(page))
        print("total data count now: " + str(count_data))
        print("================\n\n")
        page = page + 1
        saveJson()
        file_count = file_count + 1
        from_data['strrec'] = str(int(from_data['strrec']) + rec_per_page)

    # also save in case the last bunch of data is less than 300
    saveJson()

    print("\ntotal data count: " + str(count_data))
