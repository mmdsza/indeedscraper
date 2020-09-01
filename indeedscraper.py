import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
chromedriver_location=('INSERT CHROMEDRIVER LOCATION HERE')

#PLACE CHROMEDRIVER LOCATION
timestamp = datetime.now().strftime("%Y%m%d")
filename = "indeed"+timestamp+".csv"

f = open(filename, "w", encoding="utf8")

headers = "jobTitle, jobCategory, jobCompany, jobDescription, salary, url\n"

f.write(headers)

driver = webdriver.Chrome(ChromeDriverManager().install())
#This first loop gets the job links needed to iterate through later on
links = []
for i in range(0,8000,10):
	firsturl='https://www.indeed.co.in/jobs?l=India&filter=0&start='+str(i)
	driver.get(firsturl)
	test = driver.page_source
	sopa = BeautifulSoup(test, 'html.parser')
	testes = sopa.find_all("div", {"class":"jobsearch-SerpJobCard unifiedRow row result clickcard"})
	for link in testes:
	    cleanlink = link.h2.a["href"]
	    fulllink = "https://www.indeed.co.in"+cleanlink
	    links.append(fulllink)


#Going through every link to revtrieve the needed info
for link in links:
    driver.get(link)
    url = driver.page_source
    soup = BeautifulSoup(url, 'html.parser')
    jobposting = soup.find_all("div", {"class":"jobsearch-ViewJobLayout-jobDisplay icl-Grid-col icl-u-xs-span12 icl-u-lg-span7"})
    for data in jobposting:
        jobtitle = data.div.h1.text.strip().replace(",", ";")
        jobcompanyBrute = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div[2]")
        jobCompanyClean = jobcompanyBrute.text.partition("-")[0].replace(",", ";")
        jobDescriptionRaw = driver.find_element_by_xpath("//*[@id='jobDescriptionText']").text.replace(',', ";").replace('\n', ' ')
        salarysubstring = "Salary"
        salary = "-99notscrapable"
        categorybrute = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div[2]/div/div/div[1]").text
        categoryclean = categorybrute.partition("jobs")[0].replace(",", ";")
        joblink = driver.current_url.replace(",", ";")


        csvLineEntries = [jobtitle.replace(",", " "), categoryclean.replace(",", " "), jobCompanyClean.replace(",", " "), jobDescriptionRaw.replace(",", " "),  salary.replace(",", " "), joblink.replace(",", " ")]
        csvLine = ','.join([entry.replace('\n', ' ') for entry in csvLineEntries])

        f.write(csvLine + '\n')



f.close()



driver.quit()
