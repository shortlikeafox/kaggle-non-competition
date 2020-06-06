import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

#####
#Here we need to look at the wrestler pages and get
#1. date_of_birth
#2. date_of_death
#3. cause_of_death


#Steps:
#1. Load csv into dataframe.
#2. Go row-by-row and open the pages.  We could use a filter here to filter
#by belt eventually
#3. Add date_of_birth, date_of_death, and cause_of_death to a list

#####

#1. Load csv into a dataframe



df = pd.read_csv('test.csv')

#display(df)

#Let's iterrate the rows and get the information we need
date_of_birth_list = []
date_of_death_list = []
cause_of_death_list = []

link = "Bruno_Sammartino"
wrestler_file=open(f'wrestler_pages/{link}.html', 'rb')
soup = BeautifulSoup(wrestler_file.read(), 'html.parser')
print(link)
dob_search = soup.find('span', {'class':'bday'})
if dob_search is None:
    print("HI")
else:
    print(dob_search.get_text().strip())
  
#Let's get the death
death_date_search = soup.find('th', {'scope':'row'}, text='Died') 
if death_date_search is not None:
    death_date_search = death_date_search.next_element.next_element
    death_date = death_date_search.find('span').get_text()
    death_date_clean = death_date[1:-1]
else:
    death_date_clean = ""
print(death_date_clean)
  

#Let's get the cause of death if available
cause_search = soup.find('th', {'scope':'row'}, text='Cause of death')
if cause_search is not None:
    cause_search = cause_search.next_element.next_element
    cause = cause_search.get_text()
    #print(cause)
else:
    cause = ""
print(cause)
    

for index, row in df.iterrows():
    link = row['link'][6:]
    #print(link)
    wrestler_file=open(f'wrestler_pages/{link}.html', 'rb')
    soup = BeautifulSoup(wrestler_file.read(), 'html.parser')
    print(link)
    dob_search = soup.find('span', {'class':'bday'})
    if dob_search is not None:
        dob = dob_search.get_text().strip()
        print(dob)
    else:
        dob = ""
    date_of_birth_list.append(dob)    

    #Find date of death
    death_date_search = soup.find('th', {'scope':'row'}, text='Died') 
    if death_date_search is not None:
        death_date_search = death_date_search.next_element.next_element
        death_date = death_date_search.find('span').get_text()
        death_date_clean = death_date[1:-1]
    else:
        death_date_clean = ""
    print(death_date_clean)
    date_of_death_list.append(death_date_clean)

    #Find cause of death
    cause_search = soup.find('th', {'scope':'row'}, text='Cause of death')
    if cause_search is not None:
        cause_search = cause_search.next_element.next_element
        cause = cause_search.get_text()
        #print(cause)
    else:
        cause = ""
    print(cause)
    cause_of_death_list.append(cause)


print(len(date_of_birth_list))
print(len(date_of_death_list))
print(len(cause_of_death_list))

df['date_of_birth'] = date_of_birth_list
df['date_of_death'] = date_of_death_list
df['cause_of_death'] = cause_of_death_list

df.to_csv('test_two.csv', index=False)


