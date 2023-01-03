import json
import requests
import re
from bs4 import BeautifulSoup

def parse_re_co_requisites_info(major_div):
    '''
    Function that search and parse the information about the Prerequisite and Corequisite.
    input: 
        - the div with the course information
    output:
        - returns the prerequisite and corequisite for the course
    '''
    div_description = major_div.find_all('p')
    
    corequisite = None
    prerequisite = None
    count = 0
    while count < len(div_description):
        if div_description[count].text == 'Prerequisites':
            prerequisite = div_description[count+1]
        elif div_description[count] == 'Co-requisites':
            corequisite = div_description[count+1]
        
        count += 1

    if prerequisite != None:
        prerequisite = prerequisite.text
    
    if corequisite != None:
        corequisite = corequisite.text

    return (prerequisite , corequisite)

 
def get_course_info(end_url):
    '''
    Based in the end of the url, the function return the amount of credits, hours, weeks
    and info of the course
    '''

    page = requests.get('https://www.capilanou.ca/' + end_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    major_div = soup.find('div', {'class': "course-content"})
    credits = major_div.find('div', {'class': "course-credits"}).text.replace('\n','')
    hours = major_div.find('div', {'class': "course-hours"}).text.replace('\n','')
    weeks = major_div.find('div', {'class': "course-weeks"}).text.replace('\n','')
    course_description = major_div.find('div', {'class':"course-description"}).text.replace('\n','')
    
    prerequisite, corequesite = parse_re_co_requisites_info(major_div)
    
    return (credits, hours, weeks, course_description, prerequisite, corequesite)

def append_json_file(lista_dicts, name_file):
    '''
    Save the data in the json file.
    Given the name of the file, and the list with the courses information (in dictonary form)
    '''
    with open(name_file + '.json', "r+") as file:
        data = json.load(file)
        data.extend(lista_dicts)
        file.seek(0)
        json.dump(data, file, indent=4)

def create_list_not_saved(file_name):
    '''
    Creates a list with the courses that were not saved in the json file yet.
    In case the program stoped before finishing up the search.
    '''
    with open(file_name + '.json', "r+") as file:
        data = json.load(file)

    lista = []
    for dict_ in data:
        lista.append(dict_['course_tag'])

    return lista

def collect_data(soup):
    '''
    Function that collects the course data given the soup object, with the website information.
    '''
    course_list = soup.find(id="course-listing")
    pattern = f'programs--courses/courses'
    courses = soup.find_all('a', {'href': re.compile(pattern)})

    count = 0
    lista_courses = []
    lista_saved_courses = create_list_not_saved('courses_data')
    length_lista_saved_courses = len(lista_saved_courses)

    for course in courses:
        course_tag = course.parent.parent.find('td').text
        if course_tag not in lista_saved_courses:
            course_name = course.text
            end_link = course['href']
            n_credits, n_hours, n_weeks, info,  prerequisite, corequesite= get_course_info(end_link)
            courses_dict = {
                'course_tag': course_tag,
                'course_name':course_name,
                'credits': n_credits,
                'hours_week': n_hours,
                'weeks': n_weeks,
                'info':info,
                'prerequisite' : prerequisite,
                'corequesite': corequesite

            }
            lista_courses.append(courses_dict)
            append_json_file(lista_courses, 'courses_data')
            lista_courses = []

        count+=1

        if count % 100 == 0 and lista_courses != []:
            print('Saved in Json')
            append_json_file(lista_courses, 'courses_data')
            lista_courses = []


    append_json_file(lista_courses, 'courses_data')

def main():
    url_courses = "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/?tab=tab-courses"
    page = requests.get(url_courses)
    soup = BeautifulSoup(page.text, 'html.parser')

    collect_data(soup)

main()
