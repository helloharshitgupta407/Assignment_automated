from selenium import webdriver
from getpass import getpass
from bs4 import BeautifulSoup
import requests
import time
import os
import glob
import shutil

#driver setup


class auto_assignment:
    def __init__(self,username,password,section,url="http://52.220.116.248/"):
        self.password=password
        self.username=username
        self.section=section
        self.url=url

    def load_all(self):#1
        
        ass_path=self.make_ass_path()
        driver=self.load_driver(ass_path)
        self.login_portal(driver)
        self.makeAssignmentFolder(ass_path)
        self.find_subject(ass_path,driver)
        driver.close()


    def make_ass_path(self):#2
        ass_path = os.path.join(os.getcwd(), 'assignments\\')
        return ass_path

    def load_driver(self,ass_path):#3

        executable_path = os.getcwd()+"\\chromedriver.exe"
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--window-size=1920,1080')
        prefs = {"download.default_directory" : ass_path,"safebrowsing.enabled":False}
        chromeOptions.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(executable_path=executable_path,options=chromeOptions)
        return driver

    def login_portal(self,driver):#4
        driver.get("http://52.220.116.248/")
        driver.find_element_by_name('email').send_keys(self.username)#entering user name to portal
        driver.find_element_by_id('password').send_keys(self.password)#entering password name to portal
        driver.find_element_by_tag_name('button').click()
        os.system('clear')
        try:
            driver.find_element_by_xpath('//*[@id="sidebar-menu"]/ul/li[4]/a/span').click()#moving to assignment forlder
            os.system('clear')
        except:
            print("******** INVALID USER-ID OR PASSWORD *********")
            time.sleep(5)
            exit()
        time.sleep(1)


    def makeAssignmentFolder(self,ass_path):#5
        try:
            os.mkdir(ass_path)
            print("Making Assignment Folder....")
        except:
	        print ("Assignment folder already exist updating assignments ....")

    def find_subject(self,ass_path,driver):#6
        temp=0
        table=driver.find_elements_by_tag_name('tr')
        os.system('clear')
        print("DOWNLOADING......")
        print("Please wait! It will take few minutes to download")
        
        for i in table:
            #table heading left
            if temp==0:
                temp+=1
                continue
            table_data=i.find_elements_by_tag_name('td')
            if table_data[7].text!=section:
                continue
            sub_name=table_data[3].text
            subject_path = self.make_subject_folder(ass_path,sub_name)
            i.find_element_by_tag_name('a').click()
            time.sleep(2)
            self.download_assignment(driver,ass_path,subject_path)
        
    
    def make_subject_folder(self,ass_path,sub_name):#7
        subject_path = os.path.join(ass_path, sub_name)
        try:
	        os.mkdir(subject_path)
            
        except FileExistsError:
	        pass
        return subject_path
    
    def download_assignment(self,driver,ass_path,subject_path):#8

        #download
        ext = ['*.pdf','*.doc']

        os.chdir(ass_path)

        for i in ext:
            temp_assignment=glob.glob(i)
            time.sleep(1)
            if len(temp_assignment)==1:
                break
        source=ass_path+temp_assignment[0]
        destination=subject_path

        #if assignment already exist
        try:
	        shutil.move(source,destination)
        except shutil.Error:
            # print(source)
            os.remove(source)
            os.system('clear')
            print ("All assignments are up to date......")
            driver.close()
            exit()
        os.system('clear')
        print ("DOWNLOAD COMPLETE")
        print ("All assignments are up to date......")
   
if __name__ == "__main__":
    username=input("Enter Your College Id:-")
    password=input("Enter Your Password:-")
    section = input("Enter Your Class Section:-")
    auto_assignment(username,password,section).load_all()