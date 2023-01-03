# Capilano University Database

## Motivation:
The motivation for this project is to practice the collection, cleaning and storage of data.
+ Python for collecting data (through web scrapping)
  + Regular Expressions
  + BeautifulSoup
+ SQL for saving and analyzing the data
+ Postgre as the Database Manegement System
+ Managing data relationships

## Proceddure
The first step of the project is to collect data from Capilano University website. </br>
Starting with the data from the courses, including:
+ Course Name
+ Course Ticker
+ Credits
+ Hours per week
+ Number of weeks
+ General information about the course
+ Prerequisites
+ Corequisites

# Repository Contents:
+ main.py
  + Python script that collects the data about the courses from the capilano website
  + Snippet of the script
  ```
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
  ```
+ course_data.json
  + Json file with the course data collected using the main.py file
  + Sample of the json data:
  ```
  {
        "course_tag": "MATH 126",
        "course_name": "Calculus II for Physical Sciences and Engineering",
        "credits": "3.00",
        "hours_week": "(4,0,0)",
        "weeks": "15",
        "info": "A study of the anti-derivative, the integral, techniques of integration, applications of the integral, differential equations, sequences,          infinite series and Taylor's Theorem. Continued emphasis on the geometric interpretation of the concepts of calculus.",
        "prerequisite": "MATH 116 with a minimum C- grade",
        "corequesite": null
    }
  ```
  