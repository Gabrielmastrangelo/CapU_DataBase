import json
import requests
import re
from bs4 import BeautifulSoup


def return_areas(link):
    '''
    Function that given a link returns the schools of the study area
    '''
    page = requests.get('https://capilanou.ca' + link)
    soup = BeautifulSoup(page.text, 'html.parser')

    areas_of_study_links = soup.find_all('a', {'class' : 'button ghost'})

    #Get the areas of study and its links
    areas_of_study = {}
    for link in areas_of_study_links:
        list_words = link.text.split()
        if list_words[0] == 'Study':
            area = ' '.join(list_words[1:]).upper().replace(' AT CAPU','')
            areas_of_study[area] = link['href']

    return areas_of_study

def return_dict_schools(link):
    ''' Return the school from the area'''
    dict_areas = return_areas(link,)

    for area in dict_areas:
        dict_areas[area] = return_areas(dict_areas[area])
    
    return dict_areas

def return_our_people(link):
    '''
    Return the content of the Our People tab in the School's website
    '''
    page = requests.get('https://capilanou.ca' + link)
    soup = BeautifulSoup(page.text, 'html.parser')

    all_staff = soup.find_all('div', {'class' : 'page-alert'})

    lista_str = [str(x) for x in all_staff]

    return lista_str

def main():

    print('Start collecting data...')

    link = '/programs--courses/search--select/explore-our-areas-of-study/'

    result = return_dict_schools(link)

    for area in result:
        for school in result[area]:
            link = result[area][school]
            result[area][school] = return_our_people(link)

    # Serializing json
    json_object = json.dumps(result, indent=4)
    
    # Writing to sample.json
    with open("collect_prof_data/professors_data.json", "w") as outfile:
        outfile.write(json_object)

main()

print('Done')