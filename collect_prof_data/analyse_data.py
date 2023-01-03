import json
from bs4 import BeautifulSoup
import re

def get_difference(h5, span):
    if span:
        h5_set = set(h5.split())
        span_set = set(span.split())
        name = ' '.join(list(h5_set-span_set))
    else:
        name = h5

    return name

def get_text_between_brs(string):
    result = re.findall(r'<br/>(.*?)<br/>', string)
    if result != None:
        result = result[:-1]
        new_list = []
        for element in result:
            if element != '':
                new_list.append(element.strip())
        return new_list
    else:
        return result

def no_view_profile(tag):
    print(len(tag.find_all()) == 0 and "view profile" not in tag.text)


# Opening JSON file
f = open('professors_data.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
for area in data:
    print(area)
    for school in data[area]:
        print(f'\t{school}')
        for department in data[area][school]:
            soup = BeautifulSoup(department, 'html.parser')
            h5_element = soup.find('h5')
            credentials = h5_element.find('span')
            if credentials:
                credentials = credentials.text
                list_credentials = credentials.split(', ')
            else:
                credentials = None
            name = get_difference(h5_element.text, credentials) 
            role = soup.find('strong').text
            school_list = get_text_between_brs(str(soup))
            email = soup.find(text=re.compile("(.*?)@")).text
            #print(f'\t\tName: {name}')
            #print(f'\t\tRole: {role}')
            #print(f'\t\tSchools: {school_list}')
            print(f'\t\tSchools: {school_list}')
            #print(f'\t\tEmail: {email}')
            #print(f'\t\tCredentials: {list_credentials}')

# Closing file
f.close()