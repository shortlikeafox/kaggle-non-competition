# -*- coding: utf-8 -*-

#We are going to scrape for the wwe championship and hopefully build a 
#dataframe
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

"""
Names for the WWE Championship

WWWF World Heavyweight Championship	April 25, 1963 – February 8, 1971
WWWF Heavyweight Championship	February 8, 1971 – March 1, 1979
WWF Heavyweight Championship	March 1, 1979 – December 26, 1983
WWF World Heavyweight Championship	December 26, 1983 – May 27, 1989
WWF Championship	July 18, 1989 – December 9, 2001
Undisputed WWF Championship	December 9, 2001[2] – May 6, 2002[3]
Undisputed WWE Championship	May 6, 2002[3] – May 19, 2002[10]
WWE Undisputed Championship	May 19, 2002[3] – September 2, 2002[11]
WWE Championship	September 2, 2002[11] – December 15, 2013
WWE World Heavyweight Championship	December 15, 2013 – June 27, 2016
WWE Championship	June 27, 2016
[12][13] – July 25, 2016

WWE World Championship	July 26, 2016[14] – December 9, 2016
WWE Championship	December 10, 2016[8] – present

"""

html=urlopen('https://en.wikipedia.org/wiki/List_of_WWE_Champions')
bs=BeautifulSoup(html, 'html.parser')

bs_table = bs.find('table', {'class':'wikitable sortable',
                             'style': 'text-align: center',
                             'width': '100%'})

#display(bs_table)


#What we need to get:
#1. Wrestler name
#2. Reign
#3. Days
#3.5 date
#4. Belt (WWE Championship)
#5. Event
#6. Location
#7. wiki_link (to wrestler's page)


#1. Wrestler name
wrestlers = bs_table.find_all('span', {'class':'fn'})

wrestlers_list = []
wrestlers_link_list = []
for w in wrestlers:
    pos_link = w.find('a')
    wrestlers_list.append(w.get_text().strip())
    wrestlers_link_list.append(pos_link.attrs['href'])




#display(len(wrestlers_list))


#2. Reign
#3. Days
#3.5 Date
#5. Event
#6. Location

event_list = []
reign_list = []
days_list = []
date_list = []
event_list = []
location_list = []
champ_rows = bs_table.find_all('tr')
#print(len(champ_rows))
for row in champ_rows:
    cols = row.find_all('td')
    #print(len(cols))
    pos_reign = ''
    pos_days = ''
    pos_date = ''
    pos_event = ''
    pos_location = ''
    if len(cols) == 9:
        pos_reign = cols[4].get_text()
        pos_date = cols[1].get_text()
        pos_days = cols[5].get_text()
        pos_event = cols[2].get_text()
        pos_location = cols[3].get_text()
    if len(cols) == 10:
        pos_reign = cols[5].get_text()
        pos_days = cols[6].get_text()
        pos_date = cols[2].get_text()
        pos_event = cols[3].get_text()
        pos_location = cols[4].get_text()
    #print(pos_event)
    

    if pos_days.strip() == '<1':
        pos_days = '0'
    pos_days = pos_days.split(" ")[0]
    #We need to remove commas and pluses
    pos_days = pos_days.replace(",", "")
    pos_days = pos_days.replace("+", "")
    
    if (is_integer(pos_reign)):
        if not is_integer(pos_days):
            pos_days = '0'

    
    #print(len(cols), pos_reign, is_integer(pos_reign), pos_days, 
    #      is_integer(pos_days))


    if is_integer(pos_reign):
        reign_list.append(pos_reign.strip())
    #If the is valid we can use that information to include some of the tougher
    #ones like date....
        date_list.append(pos_date.strip())
        event_list.append(pos_event.strip())
        location_list.append(pos_location.strip())
        
    if is_integer(pos_days):
        days_list.append(pos_days.strip())    
        
print(len(wrestlers_list), len(reign_list), len(days_list), len(date_list),
      len(event_list), len(location_list), len(wrestlers_link_list))        


champ_tuples = list(zip(wrestlers_list, reign_list, days_list, date_list,
                        event_list, location_list, wrestlers_link_list))


df = pd.DataFrame(champ_tuples, columns=['name', 'reign', 'days', 'date',
                                         'event', 'location', 'link'])



df['belt'] = 'WWE Championship'
#display(df)



#Let's download the wrestler's individual wiki pages.  This will make
#dealing with them a bit quicker.  Plus we aren't constantly bugging
#wikipedia with requests this way.



#Remove duplicates
link_list_no_dups = list(dict.fromkeys(wrestlers_link_list))

#This code is taken from my UFC Event Scraper.  It should work?
for l in link_list_no_dups:
    l_full = "https://en.wikipedia.org/" + l
    print(l_full)    
    l_name = l[6:]
#    print(l_name)
    html= urlopen(l_full)
    bs = BeautifulSoup(html.read(), 'html.parser')
    with open(f'wrestler_pages/{l_name}.html', "w", encoding='utf-8') as file:
        file.write(str(bs))




df.to_csv('test.csv', index=False)

#4. Belt (WWE Championship)




####OK!  This is complete.  We just need to open the wrestler pages
#and get death info....