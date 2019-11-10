from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from pynput.keyboard import Key, Controller
import requests
import time
import clipboard

#sets path for Study Tools url chromedriver
urlPearson1 = 'add your url here'
urlPearson2 = 'add a second url here'
urlPearsonOriginal = 'add pearson textbook link here'
urlQuizlet = "https://quizlet.com"
urlQuizletCreate = "https://quizlet.com/create-set"

#macOS PATH
mac_chrome_path = '/usr/local/bin/chromedriver'
#Windows PATH
windows_chrome_path = 'D:/Downloads/chromedriver_win32/chromedriver.exe'

#Opens Chrome
#Change the variable in the parenthesis based on your OS
driver = webdriver.Chrome(mac_chrome_path)

#Opens and logs into Quizlet
driver.get(urlQuizlet)
driver.find_element_by_class_name("SiteHeader-signInBtn").click()

#Types in username and password and clicks log in
driver.find_element_by_id("username").send_keys("put your quizlet username here")
driver.find_element_by_id("password").send_keys("put your quizlet password here")
driver.find_element_by_class_name('UILoadingButton').click()


#########################


#Opens and logs into Pearson
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

driver.get(urlPearsonOriginal)
sleep(1)
driver.find_element_by_xpath('/html/body/section[1]/div[1]/div[2]/div/p[2]/a').click()
sleep(2)
#Add Login Details Here
driver.find_element_by_id("username").send_keys("put your Pearson username here")
driver.find_element_by_id ("password").send_keys("put your Pearson password here")

driver.find_element_by_id("mainButton").click()
sleep(2)
driver.get(urlPearson2)
#Add Login Details Here
driver.find_element_by_id("username").send_keys("put your Pearson username here")
driver.find_element_by_id ("password").send_keys("put your Pearson password here")
driver.find_element_by_id("mainButton").click()


#Loads HTML into BeautifulSoup
sleep(4)
html_doc = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
soup = BeautifulSoup(html_doc, "html.parser")

#Gets number of chapters in textbook
nChapters = 0
for class_ in soup.find_all(class_="chapterTitle"):
	nChapters = nChapters+1

bookTitle = soup.find_all(class_="titleHeader")[0].getText()

sleep(3)

for i in range(nChapters):
	#Opens ith chapter page
	print(i)
	chapterTitles = []
	chapterTitles = driver.find_elements_by_class_name("chapterTitle")
	chapterTitles[i].click()
	html_doc2 = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
	soup2 = BeautifulSoup(html_doc2, "html.parser")

	setTitle = soup2.find_all(class_="chapterText")[0].getText()
	setTitleTxt = setTitle.replace(":","")
	#f = open(setTitleTxt + ".txt","w+", encoding='utf-8')

	#Finds number of terms in set
	nterms=0
	for class_ in soup2.find_all(class_="termTitle"):
		nterms = nterms+1

	quizletCopy = ""
	#Loops through each term and definition
	for i in range(nterms):
		term = soup2.find_all(class_="termTitle")[i].getText()
		definition = soup2.find_all(class_="termDefinition")[i].getText()
		#Removes pronunciation text that is in some definitions
		if definition[0] == "(":
			if not definition[1].isnumeric():
				closeParanthesis = definition.find(")")
				definition = definition[(closeParanthesis + 2):]
		#Removes terms whose definition is just a referral to another term
		if definition[0:4] == "See ":
			continue
		#Prints and writes each term and definition to the .txt file
		#f.write(term + " - " + definition + "\n")
		quizletCopy = quizletCopy + term + " - " + definition + "\n"

	#quizletCopy = f.read()
	#f.close()
	print(quizletCopy)
	clipboard.copy(quizletCopy)
	driver.get(urlPearson2)
	driver.switch_to.window(driver.window_handles[0])
	#Delay and goes to create set
	sleep(1)
	driver.get(urlQuizletCreate)
	#Clicks import from external source
	driver.find_element_by_xpath("//*[@id='SetPageTarget']/div/div[1]/div[3]/div/button").click()
	driver.find_element_by_class_name("ImportTerms-textarea").send_keys(Keys.CONTROL, 'v') #paste
	driver.find_element_by_xpath("//*[@id='SetPageTarget']/div/div[3]/div[1]/div/form/div[2]/div[1]/div/label[3]/span[2]/span/label/div/input").send_keys(" - ")
	sleep(2)
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[3]/div[1]/div/form/div[1]/button').click()
	sleep(3)
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[1]/div[2]/div/div/div/label/div/div/div[2]/textarea').send_keys(bookTitle + " - " + setTitle)
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[1]/div[2]/div/div/div/label/div/div/div[2]/textarea').send_keys(Keys.TAB)
	#Clicks Choose Language for Term
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/span[2]/div').click()
	sleep(1)
	keyboard = Controller()
	keyboard.press('e')
	keyboard.release('e')
	keyboard.press('n')
	keyboard.release('n')
	keyboard.press('g')
	keyboard.release('g')
	keyboard.press('l')
	keyboard.release('l')
	keyboard.press('i')
	keyboard.release('i')
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)

	#Clicks Choose Language for Term
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[1]/div[2]/div/div/div/label/div/div/div[2]/textarea').send_keys(Keys.TAB)
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/span[2]/div').click()
	sleep(1)
	keyboard = Controller()
	keyboard.press('e')
	keyboard.release('e')
	keyboard.press('n')
	keyboard.release('n')
	keyboard.press('g')
	keyboard.release('g')
	keyboard.press('l')
	keyboard.release('l')
	keyboard.press('i')
	keyboard.release('i')
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)

	#Clicks Create Set
	driver.find_element_by_xpath('//*[@id="SetPageTarget"]/div/div[1]/div[1]/div/div/div/div[3]/button').click()

	#Exit alert
	sleep(2)
	#driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/div/span/div/span/button').click()
	driver.switch_to.window(driver.window_handles[1])
	sleep(1)
	#end
