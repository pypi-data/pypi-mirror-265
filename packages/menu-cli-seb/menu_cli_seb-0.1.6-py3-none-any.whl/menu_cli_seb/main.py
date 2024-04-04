from bs4 import BeautifulSoup
import requests
import json
import sys
from datetime import datetime
from .properties import set_environment_variable, set_environment_variables

CONFIG_FILE = "config.json"

def main():
    if len(sys.argv) < 2:
        print("Usage: python sebfood [day-week]")
        sys.exit(1)

    set_environment_variables()
    argument = sys.argv[1]

    print("Argument received:", argument)
    if argument.lower() == 'day':
        print_day()
    elif argument.lower() == 'week':
        print_out_weeks()
    elif argument.lower() == 'set':
        if(len(sys.argv) > 2  ):
            key = sys.argv[2]
            value = sys.argv[3]
            set_environment_variable(key,value)
        else:
            print("Use set http_proxy proxies")
                
         
def print_day():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
  
    bistro , salluhallen = f'https://www.foodandco.se/api/restaurant/menu/day?date={formatted_date}&language=sv&onlyPublishedMenu=true&restaurantPageId=166181' ,f'https://www.foodandco.se/api/restaurant/menu/day?date={formatted_date}&language=sv&onlyPublishedMenu=true&restaurantPageId=197239'
    print("BISTRO")
    bistro_response = requests.get(bistro)
    bistro_content = bistro_response.json()
    print_out_day(bistro_content['LunchMenu'])
    print("SALUHALLEN")
    salluhallen_response = requests.get(salluhallen)
    salluhallen_content = salluhallen_response.json()  
    print_out_day(salluhallen_content['LunchMenu'])
    
    
def print_out_weeks():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    bistro, saluhallen = f'https://www.foodandco.se/api/restaurant/menu/week?language=sv&onlyPublishedMenu=true&restaurantPageId=166181&weekDate={formatted_date}' ,  f'https://www.foodandco.se/api/restaurant/menu/week?language=sv&onlyPublishedMenu=true&restaurantPageId=197239&weekDate={formatted_date}'    
    print_out_from_uri(bistro)
    print_out_from_uri(saluhallen)

def print_out_from_uri(url):
    response = requests.get(url)
    html_content = response.json()
    
    
    for d in html_content['LunchMenus']:
        print_out_day(d)



def print_out_day(d):
    if d.get('Html'):
        print(d.get('DayOfWeek'))
        soup = BeautifulSoup(d.get('Html'), 'html.parser')
        strong_tags = soup.find_all('strong')
        for tag in strong_tags:
            print(tag.get_text(strip=True))
        print("\n")
            
