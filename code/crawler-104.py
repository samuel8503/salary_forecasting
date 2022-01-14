import requests
from bs4 import BeautifulSoup
import json
import random
import string
from time import sleep

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
page = 1
max_page = 150
base_url1 = "https://www.104.com.tw/jobs/search/?ro=0&jobcat=2007000000%2C2008000000&page="
base_url2 = "&mode=s&jobsource=2018indexpoc"
count_data = 0
resultList = {'jobs': []}  # the data save to json
file_count = 1
keyword_major = ["電機", "電子", "資工", "通訊", "資訊工程", "工業工程", "應用數學", "理工", "資訊與設計系", "資訊科技學系",
                 "資訊科學學系", "資訊管理學系"]
keyword_language = ["多益", "TOEIC", "托福", "TOFEL", "iBT", "雅司", "IELTS"]
keyword_codingLanguage = ["Javascript", "R", "C++", "C語言", "Python", "HTML", "CSS", "SQL", "VBA", "python", "JAVA", 
                          "C#", "shell script", "Java Script", "Java", "PHP", "Visual Basic", ".net", "JavaScript", 
                          "Verilog", "Perl", "Objective-C", "Swift"]
keyword_software = ["OFFICE", "EXCEL", "Labview", "PLC", "Visual Studio", "ASP.NET", "github", "Linux", "Juniper",
                    "VueJs", "AngularJS", "Git", "git", "AD", "Office", "Windows", "windows", "Server", "server",
                    "GIT", "docker", "MongoDB", "Word", "PowerPoint", "Excel", "Outlook", "jQuary", "jupyter", "Android",
                    "iOS", "OpenGL", "OpenCV", "RedisDB", "Struts1", "Spring", "Hibernate", "SpringBoot", "Eclipse", "AWS",
                     "Office", "App", "Unity", "MSSQL", "MySQL"]
keyword_remove = ["報名", "面試", "時間", "工作待遇", "底薪", "月薪", "分紅", "業績", "補充", "條件", "面議", "吃苦耐勞",
                  "處理問題", "團隊", "合作能力", "溝通", "敏捷", "擅長工具", "積極", "責任心", "公司", "抗壓", "跨領域", "合作",
                  "書面審查", "畢業證書", "職缺", "輪值", "輪班", "加班", "未填寫", "PDF", "必要", "加分", "不拘"]
keyword_certification = ["證照"]
keywords_set = [keyword_major, keyword_language, keyword_codingLanguage, keyword_certification, keyword_software]
# something wrong with these url
keyword_pass = ["http://www.104.com.tw/job/6mezx?jobsource=2018indexpoc", "http://www.104.com.tw/job/6qthw?jobsource=hotjob_chr",
                "http://www.104.com.tw/job/6sfc7?jobsource=2018indexpoc", "http://www.104.com.tw/job/6pumo?jobsource=n104bank2",
                "http://www.104.com.tw/job/6pgxa?jobsource=n104bank2", "http://www.104.com.tw/job/6mezx?jobsource=n104bank2",
                "http://www.104.com.tw/job/3mv4v?jobsource=n104bank2", "http://www.104.com.tw/job/6mezl?jobsource=n104bank2",
                "http://www.104.com.tw/job/5t3x4?jobsource=n104bank2", "http://www.104.com.tw/job/6bhsz?jobsource=n104bank2",
                "http://www.104.com.tw/job/409bx?jobsource=n104bank2", "http://www.104.com.tw/job/5328y?jobsource=n104bank2",
                "http://www.104.com.tw/job/6g0qe?jobsource=n104bank2", "http://www.104.com.tw/job/6rz3x?jobsource=n104bank2",
                "http://www.104.com.tw/job/40puf?jobsource=n104bank2", "http://www.104.com.tw/job/53np3?jobsource=n104bank2",
                "http://www.104.com.tw/job/6i4ty?jobsource=n104bank2", "http://www.104.com.tw/job/6oq49?jobsource=n104bank2",
                "http://www.104.com.tw/job/6nu2n?jobsource=n104bank2", "http://www.104.com.tw/job/6fkou?jobsource=n104bank2",
                "http://www.104.com.tw/job/5qho7?jobsource=n104bank2", "http://www.104.com.tw/job/6p621?jobsource=n104bank2",
                "http://www.104.com.tw/job/6bbfu?jobsource=n104bank2", "http://www.104.com.tw/job/5td3h?jobsource=n104bank2",
                "http://www.104.com.tw/job/6aem2?jobsource=n104bank2", "http://www.104.com.tw/job/6owf8?jobsource=n104bank2",
                "http://www.104.com.tw/job/5b2rd?jobsource=n104bank2", "http://www.104.com.tw/job/6lzko?jobsource=n104bank2",
                "http://www.104.com.tw/job/6nbf9?jobsource=n104bank2"]


def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False


def saveJson():
    global file_count
    with open("jobs_104_" + str(file_count) + ".json", 'w', encoding='utf8') as outfile:
        json.dump(resultList, outfile, ensure_ascii=False, indent=2, separators=(',', ': '))
        # use .decode to turn it back


def crawContent(link, companyName):
    global count_data
    # init variables
    jobFullLink = "http://" + link.get('href')[2:]
    jobName = link.contents[0]
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
    print("crawing content of: " + jobName + "\ncompany:" + companyName +"\nlink:"+ jobFullLink)

    # start crawing
    sleep(INTERVAL)
    res = requests.get(jobFullLink, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html5lib')
    contentList = soup.find('main', {'class': 'main'}).findAll('section', {'class': 'info'})

    # 0: 工作內容
    liList = contentList[0]  # .findAll('li')
    pList = liList.find('p')
    if pList is not None:
        others += pList.text.split("\n")
    companyCity = liList.find('dd', {'class':'addr'}).contents[0]
    companyCity = companyCity.replace(" ", "").replace("\n", "")
    allCate = liList.find('dd', {'class': 'cate'}).findAll('span')
    cates = []
    for cate in allCate:
        if len(cate.contents) != 0:
            # print(cate.contents[0])
            cates.append(cate.contents[0])
    jobCategory = cates
    jobSalary = liList.find('dd', {'class': 'salary'}).contents  # .split(" ")
    # print("?????: (" + jobSalary[0] + ")")
    jobSalary[0] = jobSalary[0].strip()
    jobSalary[0] = jobSalary[0].replace(",", "")
    jobSalary[0] = jobSalary[0].replace("元", "")
    jobSalary[0] = jobSalary[0].replace("以上", "")
    if jobSalary[0][:4] == "待遇面議":
        # print("?????: (" + jobSalary[2] + ")")
        top = jobSalary[2][1]
        jobSalary = int(top + "0000")
    elif jobSalary[0][:2] == "月薪":
        jobSalary = int(jobSalary[0][3:].split("~")[0])
    elif jobSalary[0][:2] == "年薪":
        jobSalary = int(int(jobSalary[0][3:].split("~")[0]) / 12)
    elif jobSalary[0][:2] == "週薪":
        jobSalary = int(jobSalary[0][3:].split("~")[0]) * 4
    elif jobSalary[0][:2] == "日薪":
        jobSalary = int(jobSalary[0][3:].split("~")[0]) * 30
    elif jobSalary[0][:2] == "時薪":
        jobSalary = int(jobSalary[0][3:].split("~")[0]) * 8 * 30

    # 1: 要求條件
    liList = contentList[1].findAll('dt')
    liList_dd = contentList[1].findAll('dd')
    for d, li in enumerate(liList):
        try:
            title = li.contents[0]
            if title == "接受身份：":
                acceptIdentity = liList_dd[d].contents[0].split("、")
                # print("identity: " + acceptIdentity)
            elif title == "學歷要求：":
                eduLevel = liList_dd[d].contents[0].split("、")
                # print("edu: " + eduLevel)
            elif title == "科系要求：":
                acceptMajor = liList_dd[d].contents[0].split("、")
                # print("accM: " + acceptMajor)
            elif title == "工作經歷：":
                workingExp = liList_dd[d].contents[0]
                # print("wE: " + workingExp)
            elif title == "語文條件：":
                allLanguage = liList_dd[d].contents  # findAll('li')
                # print(allLanguage)
                # print("英文" in str(allLanguage))
                if "英文" in str(allLanguage):
                    language.append("英文")
                if "中文" in str(allLanguage):
                    language.append("中文")
                if "台語" in str(allLanguage):
                    language.append(("台語"))
            elif title == "具備駕照：":
                carLicense = liList_dd[d].contents[0].split("、")
                for l in carLicense:
                    certification.append(l)
            elif title == "擅長工具：":
                for l in liList_dd[d].contents[0].split("、"):
                    others.append(l)
            elif title == "其他條件：":
                pList = liList_dd[d].contents
                # print(pList)
                for p in pList:
                    if isinstance(p, str):
                        # print("p: " + p)
                        p_ = p.split("\n")
                        for p__ in p_:
                            p___ = p__.split("。")
                            for p____ in p___:
                                if p____ != "":
                                    others.append(p____)
                print(others)
        except:
            continue

    # 2: 應徵方式、3: hashtag、4: 看過此工作的人還看過 -> 這些我沒抓

    # print(others)

    # deal with messy 'other'
    # correspond_set = [acceptMajor, language, codingLanguage, certification, software]
    remove = []
    for oID, other in enumerate(others):
        # other = other.replace(" ", "")
        other = other.replace("\t", "")
        other = other.replace("\r", "")
        if other == "" or other == " ":
            remove.append(oID)
        else:
            # deal with the start of 'other'
            while len(other) != 0 and (other[0].isdigit() or other[0] in string.punctuation or other[0] == " "):  # or is_alpha(other[:1]):
                other = other[1:]
                # print("??: (" + other[0] + ")")
                # print("ori: " + other)
            if other != "":
                others[oID] = other
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
    soup = BeautifulSoup(res.text, 'html5lib')
    base_soup = soup.find('div', {'id': 'js-job-content'})
    paginationList = base_soup.find_all('a', {'class': 'js-job-link'})
    companyNameList = base_soup.find_all('article')

    for linkid, link in enumerate(paginationList):
        count_data = count_data + 1
        # print(link)
        companyName = companyNameList[linkid].get('data-cust-name')  # get('data-job-name')
        # print(companyName)
        if "http://" + link.get('href')[2:] not in keyword_pass and companyName[:6] != "GARMIN":
            crawContent(link, companyName)

        if count_data % 20 == 0:
            USER_AGENT = random.choice(USER_AGENT_LIST)
            print(USER_AGENT)
            headers = {'User-agent': USER_AGENT}

        """
        if count_data % 100 == 0:
            saveJson()
            file_count = file_count + 1
        """


if __name__ == '__main__':
    # page = 118
    while page <= max_page:
        print("================\npage: " + str(page))
        print("total data count now: " + str(count_data))
        print("================\n\n")
        url = base_url1 + str(page)  # + base_url2
        crawlTitle(url)
        page = page + 1
        saveJson()
        file_count = file_count + 1

    # also save in case the last bunch of data is less than 300
    saveJson()

    print("\ntotal data count: " + str(count_data))
