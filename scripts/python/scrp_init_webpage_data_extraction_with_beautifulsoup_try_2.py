#!/usr/bin/env python
# coding: utf-8

# Objective: Create a beautifulsoup based scraper.
# 
# Website to scrape: www.indeed.com.my
# 
# What to scrape: extract the job posting details like position name, salary and location.

# In[1]:


# required libraries
import requests
import time
from bs4 import BeautifulSoup as soup
import urllib.request
import re
import pandas as pd


# In[2]:


# create list of cities in Malaysia from https://en.wikipedia.org/wiki/List_of_cities_in_Malaysia
city = ['George+Town', 'Kuala+Lumpur', 'Ipoh', 'Kuching', 'Johor+Bahru', 'Kota+Kinabalu', 'Shah+Alam', 'Melaka', 'Alor+Setar',
       'Miri', 'Petaling Jaya', 'Kuala Terengganu', 'Iskandar Puteri', 'Seremban']
state_list = ['Penang','Federal Territory','Perak', 'Sarawak', 'Johor', 'Sabah', 'Selangor', 'Melaka', 'Kedah', 'Sarawak', 'Selangor',
        'Terengganu', 'Johor', 'Negeri Sembilan']

max_results_per_city = 800 
df = pd.DataFrame()

page_url = "https://www.indeed.com.my/jobs?q=data+scientist&l="
results = []


# In[3]:


#conducting a request of the stated URL above:
page = requests.get(page_url)


# In[4]:


page_text = soup(page.text, "html.parser")


# In[5]:


#printing soup in a more structured tree format that makes for easier reading
print(page_text.prettify())


# Now, we know that our variable “soup” has all of the information housed in our page of interest. It is now a matter of writing code to iterate through the various tags (and nested tags therein) to capture the information we want.

# In[6]:


def extract_job_title_from_result(page_text):
    jobs = []
    for div in page_text.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)

extract_job_title_from_result(page_text)


# Now, lets extract the company names

# In[7]:


def extract_company_from_result(page_text):
    companies = []
    for div in page_text.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)
 
extract_company_from_result(page_text)


# Lets extract the locations now

# In[8]:


# define the function
def extract_location_from_result(page_text):
    locations = []
    spans = page_text.findAll( name="span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)

# execute the function
extract_location_from_result(page_text)


# Now, extracting the salary

# In[9]:


# define the function
def extract_salary_from_result(page_text):
    salaries = []
    for div in page_text.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find(name= "nobr").text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class":"sjcl"})
                div_three = div_two.find(name="div")
                salaries.append(div_three.text.strip())
            except:
                salaries.append("Nothing found")
    return(salaries)

# execute the function
extract_salary_from_result(page_text)


# In[25]:


#Finally, extracting the job summaries
# define the function
def extract_summary_from_result(page_text):
    summaries = []
    spans = page_text.findAll(name= 'div', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)

# execute the function
extract_summary_from_result(page_text)


# In[30]:


# define the function
def extract_reviews_from_result(page_text):
    reviews = []
    spans = page_text.findAll( name="span", attrs={"class": "slNoUnderline"})
    for review in spans:
        reviews.append(review.text.strip())
    return(reviews)

# execute the function
extract_reviews_from_result(page_text)


# In[43]:


# get the job advert posting date
def extract_advertpostdate_from_result(page_text):
    dates = []
    spans = page_text.findAll( name="span", attrs={"class": "date"})
    for jobdate in spans:
        dates.append(jobdate.text.strip())
    return(dates)

# execute the function
extract_advertpostdate_from_result(page_text)


# Now, calling all these functions and saving them into individual variables. Then add those variables to a dataframe.

# In[44]:


job_title = extract_job_title_from_result(page_text)
company_info = extract_company_from_result(page_text)
company_loc = extract_location_from_result(page_text)
jobDescr = extract_summary_from_result(page_text)
#salary = extract_salary_from_result(page_text)
reviews = extract_reviews_from_result(page_text)
advertpostdate = extract_advertpostdate_from_result(page_text)


# In[45]:


jobs_df = pd.DataFrame(
    {'JobTitle':job_title, 'Company':company_info, 'Location':company_loc, 'Job Description': jobDescr,
     'Date':advertpostdate
     #,'Reviews':reviews
    }
    )


# In[46]:


jobs_df


# #### Further improvement options
# 
# 1. Scrape multiple pages
# 
# Note: The base url is, "https://www.indeed.com.my/jobs?q=data+scientist&l=". The next page url is, `https://www.indeed.com.my/jobs?q=data+scientist&start=10` thereafter the only entity changing in subsequent pages is `start=10`. So the third page, url is `https://www.indeed.com.my/jobs?q=data+scientist&start=20`  
# 

# In[ ]:




