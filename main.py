from selenium import webdriver
import time
import datetime

web = webdriver.Chrome('F:\\GitHub\\jobfinder\\chromedriver.exe')

searchStr = "backend"

maxpageXpath = '//*[@id="jobs_block_pager"]/span[6]/a'
maxpage = 999
pagenow = 1
cookieAccepted = False
alreadyFound = {}
max_id = 0

file = open("lastjobs.txt","a",encoding='utf-8')
file.write(""+"\n")
file.write(str(datetime.datetime.now())+"\n")
file.write(""+"\n")
file.close()


file = open("lastjobs.txt",encoding='utf-8')
for row in file:
    row = row.strip().split(" | ")
    if len(row)>1: #nem elválasztó
        key = row[2] + " | " + row[3]
        id = int(row[0])
        if id>max_id:
            max_id = id
        alreadyFound[key] = True
file.close()

def getpagelink(page):
    if page>maxpage:
        return False
    else:
        return "https://www.profession.hu/allasok/"+str(page)+",0,0,backend%401%401?keywordsearch"

def get_max_page():
    maxpageelement = web.find_element_by_xpath(maxpageXpath)
    link = maxpageelement.get_attribute("href")
    maxpage = link.split(",")[0].split("/")[-1]
    return int(maxpage)

def get_jobs_on_page():
    elements = web.find_elements_by_class_name("job-card__title")
    companies = web.find_elements_by_class_name("job-card__company-name")
    companyaddresses = web.find_elements_by_class_name("job-card__company-address")
    i = 0
    for element in elements:
        link = element.find_elements_by_tag_name("a")[0].get_attribute('href')
        title = element.find_elements_by_tag_name("a")[0].get_attribute('innerText')
        company = companies[i].get_attribute('innerText')
        address = companyaddresses[i].get_attribute('innerText')
        if not((title + " | " + company) in alreadyFound):
            global max_id
            max_id = max_id + 1
            row = str(max_id) + " | 0 | " + title + " | " + company + " | " + address + " | " + link
            file = open("lastjobs.txt","a",encoding='utf-8')
            file.write(row + "\n")
            file.close()
        i = i + 1

while True:
    link = getpagelink(pagenow)
    if not link:
        break
    else:
        web.get(link)
        if not cookieAccepted:
            cookieAccepted = True
            web.execute_script("Cookiebot.dialog.submitConsent();")

        time.sleep(3)
        get_jobs_on_page()

        pagenow = pagenow + 1
        

    if maxpage==999:
        maxpage = get_max_page()



file = open("lastjobs.txt","a",encoding='utf-8')
file.write(""+"\n")
file.write("==="+"\n")
file.write(""+"\n")
file.close()