#Public Test
from subprocess import call
from xml.dom import minidom
import xml.etree.ElementTree as ET
import selenium
from selenium import webdriver
from timeit import default_timer as timer
import time

import requests
import yaml

import logger

def bandwidth_maximum_test(self):
    log = logger.attach_to_logger(__name__)
    log.info('Starting: Bandwidth Maximum Test')
    start = timer()
    end = None

    call(["sc", "stop", "Killer Network Service x64"]) #Stops killer network service via command line

    #Now that killer network service is stopped, user.xml can be updated
    tree = ET.parse('C:/ProgramData/RivetNetworks/Killer/user.xml') #Loads file, should be consistent across all computers due to Killer's install process
    root = tree.getroot() #Gets root out of the tree parse
    sh = root.find('NetworkInfos') #Finds parent
    networkinfo = sh.find('NetworkInfo') #Finds child which contains the attributes we are looking for
    
    networkinfo.set('BandwidthUp', bandwidthup) #Updates bandwidth upload max speed value
    networkinfo.set('BandwidthDown', bandwidthdown) #Updates bandwith download max speed value
    tree.write('C:/ProgramData/RivetNetworks/Killer/user.xml') #Overrides the old user.xml file with a new updated file.

    #Now we need to start Killer and see if change is made
    call(["sc", "start", "Killer Network Service x64"]) #Starts killer network service via command line
    
    driver = webdriver.Chrome(executable_path = 'C:/Users/Rivet/Desktop/chromedriver_win32/chromedriver.exe') #Slave computer needs a folder with chromeddriver.exe in it for this line to run
    driver.get('http://killernetworking.speedtestcustom.com/')#Opens up killer's speed test via chrome
    id_box = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div/button')#Isolates the "go" button
    id_box.click()#clicks go button
    time.sleep(38)#waits for test to be completed
    download_element = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[1]/div[2]/div/div/span')#Grabs download element via xpath
    upload_element = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[2]/div[2]/div[2]/div/div/span')#Grabs download element via xpath
    downloadSpeed = download_element.text #Grabs download speed from element
    uploadSpeed = upload_element.text #Grabs upload speed from element

    downloadSpeed = float(downloadSpeed) * 1000000
    uploadSpeed = float(uploadSpeed) * 1000000

    downloadError = 0.93 - downloadSpeed/float(bandwidthdown)  
    uploadError = 0.93 - uploadSpeed/float(bandwidthup)

    log.info('Download Error: ' + downloadError)
    log.info('Upload Error: ' + uploadError)
change_max_bandwidth()
