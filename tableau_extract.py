# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 18:56:23 2021

@author: ababbar
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from credentials_okta import webdriver_path,okta_user_id,okta_user_passwrd
import pandas as pd
import re

# user_id = okta_user_id
# user_passwd = okta_user_passwrd


def get_login( user_id,
              user_passwd,
              url='https://tableau.discovery.com',
              webdriver_path =r'C:\Users\ababbar\Downloads\driver\chromedriver.exe',
              delay=100):

    browser=webdriver.Chrome(webdriver_path)
    browser.get(url)
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'okta-signin-username')))

    inputElement = browser.find_element_by_id("okta-signin-username")
    inputElement.send_keys(user_id)
    
    inputElement = browser.find_element_by_id("okta-signin-password")
    inputElement.send_keys(user_passwd)
    
    inputElement = browser.find_element_by_id("okta-signin-submit")
    inputElement.submit()

    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ng-app')))

    
    return(browser)

def get_load_dashbrd(browser,url,
                     delay=100):

    #go to dashboard webpage    
    browser.get(url)
    
    # myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 
                                                                                 # 'viz')))
    myElem = WebDriverWait(browser, delay)\
        .until(EC.frame_to_be_available_and_switch_to_it((0)))

    try:
        
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                                                                                      '.FilterTitle')))
    except:
        print("Time out to find filter")
        print("May not have filters in dashboard")
    
    # time.sleep(sleep_time)

    #get switch to iframe as dashboard is containarize in iframe
    # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    # time.sleep(sleep_time)
    return(browser)


def get_html_dashbrd(browser):
    #get html body of dashboard
    # html = browser.execute_script("return document.body.innerHTML;")
    html_source = browser.page_source
    return(html_source)


def remove_element(original_list,list_to_remove):

    result=[word for word in original_list if word not in list_to_remove]

    return result

def text_cleaning(input_list):
    list2=map(lambda x:x.lower(),input_list)
    result=list(set([s.strip() for s in list2]))
    return [i.title() for i in result]

def get_words_frm_html(html_source=''):    
    soup = BeautifulSoup(html_source)
    
    for script in soup(["script", "style"]):
        script.decompose()
    strips = list(soup.stripped_strings)
    return(strips)


def get_filter_name(html_source):
    soup = BeautifulSoup(html_source,"html.parser")
    filter_title_html = soup.find_all(class_='FilterTitle')
    filter_title_html
    filter_titles= []
    
    for ele in filter_title_html:
        # filter_titles.append(str(ele))
        # filter_key = (ele).text
    
        if 'Filter' in (ele).text:        
            filter_key = (ele).text
            filter_key = filter_key.replace('Filter','').replace('Inclusive','')
            filter_titles.append(filter_key)
    return(filter_titles)

def get_parameter_name(html_source):
    soup = BeautifulSoup(html_source,"html.parser")
    filter_title_html = soup.find_all(class_='ParamTitle')
    filter_title_html
    filter_titles= []
    
    for ele in filter_title_html:
        filter_key = (ele).text    
        filter_titles.append(filter_key)
    return(filter_titles)

def get_filter_value(browser,num_fltr):

    tag= 'tableau_base_widget_LegacyCategoricalQuickFilter_'

    # html_all=''
    filter_values = []
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    for i in num_fltr:      
        try:
            
            inputElement = browser.find_element_by_id(tag+str(i))
            inputElement.click()
            html_source = browser.page_source
            # html_source = html_source_new+html_source
            # inputElement = browser.find_element_by_id(tag+str(i)+'_menu')
            # inputElement.click()
            # # browser.switch_to.default_content()
            # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
            soup = BeautifulSoup(html_source,"html.parser")
            clss = 'facetOverflow'
            filter_values_html = soup.find_all(class_=clss)
            
            filter_value = [ele.text for ele in filter_values_html]   
            filter_values.append(filter_value)
            # webdriver.ActionChains(browser).context_click().perform()
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

        except:
            print(i)

    return(filter_values)

def get_parameter_value(browser,num_fltr):

    tag= 'tableau_base_widget_ParameterControl_'

    # html_all=''
    filter_values = []
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    for i in num_fltr:      
        try:
            
            inputElement = browser.find_element_by_id(tag+str(i))
            inputElement.click()
            html_source = browser.page_source
            # html_source = html_source_new+html_source
            # inputElement = browser.find_element_by_id(tag+str(i)+'_menu')
            # inputElement.click()
            # # browser.switch_to.default_content()
            # browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
            soup = BeautifulSoup(html_source,"html.parser")
            clss = 'tabMenuItemName'
            filter_values_html = soup.find_all(class_=clss)
            
            filter_value = [ele.text for ele in filter_values_html]   
            filter_values.append(filter_value)
            # webdriver.ActionChains(browser).context_click().perform()
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

        except:
            print(i)

    return(filter_values)



#extract filter name and values
noise_text = ['Unexpected Error','|','*','Click To Show All Values', 'Filter', '✓', 'Showing All Values','Press Esc To Clear Any Mark Selections. To Open The View Data Window, Press Control-Shift-Enter.','An Unexpected Error Occurred. If You Continue To Receive This Error Please Contact Your Tableau Server Administrator.','Press ESC to clear any mark selections. To open the View Data window, press Control-Shift-Enter.', 'An unexpected error occurred. If you continue to receive this error please contact your Tableau Server Administrator.', 'Undo', 'Redo', 'Revert', 'Refresh', 'Pause', 'View: Original', 'Subscribe', 'Edit', 'Share', 'Download', 'Comments', 'Full Screen']

def flatten(t):
    return [item for sublist in t for item in sublist]

def textcleaner(Original_list,Noise_containing_list,match_anywhere=True,
                start_match=False,end_match=False):
    noisefilteredlist = []
    startswith = []
    endswith = []
    if match_anywhere==True:
        noisefilteredlist=[sentence.lower() for sentence in Original_list if not any(word in sentence.lower().split(" ") for word in Noise_containing_list)]    

    elif start_match==True:
        noise_list=tuple(Noise_containing_list)
        startswith = [x.lower() for x in Original_list if not x.lower().startswith(noise_list)]

    elif end_match==True:
        noise_list=tuple(Noise_containing_list)
        endswith= [x.lower() for x in Original_list if not x.lower().endswith(noise_list)]    
    else:
        pass
    return list(set(noisefilteredlist+startswith+endswith))

def replace_chars(original_list,noise_list,
                  regex=False,any_match=True,
                  startswith=True,endswith=True):

    if any_match==True:
        rplc_lst=[re.sub("({})".format('|'.join(noise_list)), ' ',  p,flags=re.I) for p in original_list]
        return rplc_lst

    elif startswith==True:
        rplc_lst=[re.sub("^({})".format('|'.join(noise_list)), '',  p) for p in original_list]
        return rplc_lst

    elif endswith==True:
        rplc_lst=[re.sub("({})$".format('|'.join(noise_list)), '',  p) for p in original_list]
        return rplc_lst

    elif regex==True:
        rplc_lst = [re.sub("({})".format('|'.join(noise_list)), '',  p) for p in original_list]
        return rplc_lst

def drop_match_list(list1,list2,threshold):
    try:
        x=[]
        list1=[i for i in list1 if i] # deletes the empty list elements
        #list1=list(filter(lambda x: x, list1))
        
        for i in list1:
            x.append(len([j for j in i if j in list2 ])/len(i)*100) #calculate the percentage of elements present
            indexes=[idx for idx, element in enumerate(x) if element > threshold] # get the indexes of the element in which is less than threshold
            filtered_threshold_list=[i for j, i in enumerate(list1) if j not in indexes] # drop the elements greater than threshold
            
        return filtered_threshold_list
    except Exception as e:
        print(e)
        return(list1)
