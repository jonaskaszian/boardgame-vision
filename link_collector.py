#Selenium Setup
#https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
#https://scottspence.com/posts/use-chrome-in-ubuntu-wsl
#import pytest
import time
import json
import csv
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


import pathlib
script_directory = pathlib.Path().absolute()


options = Options()
#options.binary_location = '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe' 
options.binary_location = '/usr/bin/google-chrome' 

#options.add_argument("user-data-dir=/home/jonas/git/boardgame-vision/selenium")
options.add_argument(f"user-data-dir={script_directory}/selenium-data")

class LinkCollecter():
  def setup_method(self, method):
    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options = options)
    self.driver.set_window_size(1936, 1056)
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()
  
  def collect_links(self,starting_link, num_images,save_location='game_links_selenium.csv'):
    # Test name: Gloomhaven
    # Step # | name | target | value
    # 1 | open | https://boardgamegeek.com/image/2437871/gloomhaven | 
    #self.driver.manage().window().maximize();
    if type(starting_link)== int :
      starting_link =str(starting_link)
    if starting_link.isnumeric():
      starting_link= "https://boardgamegeek.com/image/"+starting_link

    self.driver.get(starting_link)
    full_link=self.driver.execute_script("return window.location.href")
    game_name= full_link.split('/')[-1]
    link_list=[game_name]
    link_list.append(full_link)
    time.sleep(0.5)
    # 2 | click | css=.tw-right-0 > .svg-inline--fa > path | 
    #self.driver.find_element(By.CSS_SELECTOR, ".tw-right-0 > .svg-inline--fa > path").click()
    # 3 | executeScript | return window.location.href | pageurl
    #self.vars["pageurl"] = self.driver.execute_script("return window.location.href")
    for j in range(num_images):
        #self.driver.find_element(By.CSS_SELECTOR, ".tw-right-0 > .svg-inline--fa > path").click()
        element = self.driver.find_element(By.CSS_SELECTOR,".tw-right-0 > .svg-inline--fa > path")
        webdriver.ActionChains(self.driver).move_to_element(element ).click(element ).perform()
        time.sleep(0.5)
        link_list.append(self.driver.execute_script("return window.location.href"))
    with open(save_location,'a') as f:
        write= csv.writer(f)
        write.writerow(link_list)
    return link_list
    
with open ('game_numbers', 'rb') as fp:
    gns = pickle.load(fp)
gns[4]='2294663' # This is not how it has been downloaded, but I will maybe replace the images in the dataset with those generated by starting at this image.
gns[7]='2737531' # This is not how it has been downloaded, but I will maybe replace the images in the dataset with those generated by starting at this image.
gns[10]='2691267'
gns[18]='2558121'
gns[22]='1279348'
gns[28]='2224818'
gns[29]='2725228'
gns[36]='8072'
gns[37]='2864172'
gns[37]='2864172'
gns[41]='250656'
gns[42]='4322118'
gns[43]='5896904' #has only 88 images
gns[44]='2903568'
gns[47]='3451529' #has only 129 images
gns[49]='4979708'
tester=LinkCollecter()
tester.setup_method(None)
tester.collect_links(3451529,128)


#game_names=['Gloomhaven','Brass Birmingham','Pandemic Legacy Season 1','Ark Nova','Terraforming Mars','Gloomhaven Jaws of the Lion','Twilight Imperium Fourth Edition','Star Wars Rebellion','Gaia Project','War of the Ring Second Edition','Spirit Island','Through the Ages A New Story of Civilization','Great Western Trail','Twilight Struggle','Dune Imperium','Scythe','The Castles of Burgundy','Nemesis','7 Wonders Duel','Brass Lancashire','Concordia','A Feast for Odin','Terra Mystica','Wingspan','Arkham Horror The Card Game','Clank Legacy Acquisitions Incorporated','Eclipse Second Dawn for the Galaxy','Root','Everdell','Viticulture Essential Edition','Orleans','Lost Ruins of Arnak','Mage Knight Board Game','Food Chain Magnate','Barrage','Marvel Champions The Card Game','Puerto Rico','Too Many Bones','Caverna The Cave Farmers','Blood Rage','Pax Pamir Second Edition','Agricola','Underwater Cities','The Crew Mission Deep Sea','Anachrony','Maracaibo','Mansions of Madness Second Edition','Pandemic Legacy Season 2','The Crew The Quest for Planet Nine','On Mars','Tzolkin The Mayan Calendar','Power Grid','Clans of Caledonia','Crokinole','Le Havre','Star Wars Imperial Assault','Cascadia','Kingdom Death Monster','Pandemic Legacy Season 0','Mechs vs Minions','Lisboa','The Quacks of Quedlinburg','The Gallerist','Paladins of the West Kingdom','Azul','Android Netrunner','Eclipse','Aeons End','The 7th Continent','Through the Ages A Story of Civilization','Race for the Galaxy','Clank A DeckBuilding Adventure','Five Tribes','Fields of Arle','Teotihuacan City of Gods','Grand Austria Hotel','Agricola Revised Edition','Robinson Crusoe Adventures on the Cursed Island','Kanban EV','The Voyages of Marco Polo','7 Wonders','Lords of Waterdeep','Dominant Species','Sleeping Gods','Great Western Trail Second Edition','Tainted Grail The Fall of Avalon','Architects of the West Kingdom','El Grande','Keyflower','Caylus','Battlestar Galactica The Board Game','Beyond the Sun','Mombasa','Dominion Intrigue','Troyes','Raiders of the North Sea','The Lord of the Rings Journeys in MiddleEarth','Twilight Imperium Third Edition','Eldritch Horror','Lorenzo il Magnifico']
#first_images=[]
#games=zip(game_names, first_images)

for gn in gns[48:50] :
    tester.collect_links(gn,150)
