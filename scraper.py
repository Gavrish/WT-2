from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
browser.get("https://www.indiabix.com/general-knowledge/basic-general-knowledge/006001")
l = [['Question','Option A','Option B','Option C','Option D','Answer']]

for i in range(10):
	
	elems = browser.find_elements_by_class_name('bix-tbl-container')

	for elem in elems:
		quest = elem.find_element_by_class_name('bix-td-qtxt').text
		print(quest)
	
		op = elem.find_elements_by_class_name('bix-tbl-options')
	
		temp = op[0].text.split("\n")
		opta = temp[0].split(".")[1].strip()
		optb = temp[1].split(".")[1].strip()
		optc = temp[2].split(".")[1].strip()
		optd = temp[3].split(".")[1].strip()
		print(temp)  		
		
		ans = elem.find_element_by_css_selector("[id^=hdnAnswer]").get_attribute('value')
		print(ans)
		
		print('\n')		
		l.append([quest,opta,optb,optc,optd,ans])
	browser.get('https://www.indiabix.com/general-knowledge/basic-general-knowledge/00600' + str(i+2))

with open('questions.csv','a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(l)
