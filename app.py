# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:33:15 2019

@author: maenDev
"""
import sys
from selenium import webdriver
from selenium.common import exceptions
from config import keys
import time
from selenium.webdriver.common.keys import Keys
from os import startfile, mkdir, rename

def signOut(driver):
    driver.find_element_by_xpath('//*[@id="root"]/div/header/a/img').click() 
    driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[2]/ul[2]/li[3]/a').click()
    driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[2]/ul[2]/li[3]/div/nav/div[2]').click()
    driver.close()
    
def makeTabs(driver, url, number):
    for i in range(number):
        driver.execute_script("window.open('"+url+"', 'Chapter "+str(i+2)+"')")

def newTab(driver, url):
    driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND +'t');
    driver.execute_script("window.open('"+url+"', 'new_window')")
    driver.get(url)
    
def getChapter(driver,i):
    driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/div[2]/ol/li['+str(i)+']/div[2]/a[1]').click()
    driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/div[2]/ol/li['+str(i)+']/ul/li[2]/a').click()
    #now we're in the course view, must click the pdf icon
    time.sleep(3)
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/header/nav/a[2]/div').click() #click to prompt "here"
        link = driver.find_element_by_link_text('here')
        pdfUrl = link.get_attribute('href')
        driver.get(pdfUrl)
        time.sleep(1)
    except exceptions.NoSuchElementException:
        print('Chapter ' + str(i) + ' is not found.')
    
def order(k,driver):
    print("Connecting to " + k['url'] + "...")
    driver.get(k['url'])
    print("Signing in...")
    driver.find_element_by_xpath('//*[@id="gatsby-focus-wrapper"]/div/div/header/div/div[1]/div[2]/ul/li[4]/a').click()
    driver.find_element_by_xpath('//*[@id="user_email"]').send_keys(k['email'])
    driver.find_element_by_xpath('//*[@id="new_user"]/button').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(k['password'])
    driver.find_element_by_xpath('//*[@id="new_user"]/div[1]/input').click()
    print("Login successful.")
    time.sleep(3) 
    print("Searching for available courses...")
    driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[1]/div[2]/div[1]/input').send_keys(k['course']+'\n')
    
    search_results = driver.find_element_by_xpath('//*[@id="courses"]/div')
    print("Search results:") #not a list
    #extract <h/4> tag
    trial2 = search_results.find_elements_by_tag_name('h4')
    print('List of available courses:')
    for i, element in enumerate(trial2):
        print(element.text + ' [' + str(i+1) + ']')
    
    #prompt user for course number
    courseNum = 0
    courseNum = input("Input course number: ")
    course = trial2[int(courseNum)].text
    initial_directory = str(keys['directory']) + '\\TEMP_'
    rename(initial_directory, course)

    print("Getting course data...")
    driver.find_element_by_xpath('//*[@id="courses"]/div/article['+str(courseNum)+']/a').click()
    time.sleep(1)
    #detect the total number of chapters n
    chaptersXpath = driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/div[2]/ol')
    
    chapters = chaptersXpath.find_elements_by_tag_name('h4')
    nChap = len(chapters) #total number of chapters
    print("Total number of chapters in this course: " + str(nChap))
    chaptersListUrl = driver.current_url
    
    makeTabs(driver, chaptersListUrl, nChap - 1)
   
    for i in range(nChap):
        m = i+1
        print("Getting chapter " + str(m) + "...")
        if(i>0):
            driver.switch_to.window(driver.window_handles[i])# jump between tabs
        time.sleep(3)
        getChapter(driver,m)
        print("Chapter " + str(m) + " is being downloaded.")
    startfile(initial_directory)
    signOut(driver)
    input("Enter any key to exit...\n")
    exit()
if __name__ =="__main__":
    directory = str(keys['directory']) + '\\TEMP_'
    mkdir(directory)
    profile = {
    "download.default_directory": directory, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    }
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', profile)
    driver = webdriver.Chrome('F:\\automation\\chromedriver.exe', options = options) #input chromedriver location here
    if(len(sys.argv)>1):
        keys['course'] = sys.argv[1]
    order(keys, driver)
    