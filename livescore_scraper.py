#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.environ["LANG"] = "en_US.UTF-8"

import requests
import pandas as pd
import bs4 as bs
from selenium import webdriver
import datetime


# In[6]:


class livescore_scraper:    
    def __init__(self): ## CTOR
        ## The browser driver which will be used to process the request
        self._browser = webdriver.Chrome('./chromedriver.exe')
    
    def scrape(start_date, end_date, country='france'):
        '''
        Scrapes the website www.livescore.com for soccer scores
        @param start_date, end_date the date interval which scores we want
        @param country the country in which we want to get the scores
        @return a DataFrame containing every match found in the given interval
        '''
        matchs = []
        ## Convert the given dates to datetime
        begin = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        ## Compute the number of days to process
        nb_days = (end - begin).days
        
        ## Process those days
        for d in range(nb_days+1):
            today = (begin + datetime.timedelta(d))
            ## First build the url we want to visit
            url = 'https://www.livescore.com/en/football/{}/ligue-1/#/{}'.format(country, today.strftime("%Y%m%d"))

            ## Get the required data from the url
            self._browser.get(url)
            sauce = self._browser.page_source

            ## Analyze it with BeautifulSoup
            soup = bs.BeautifulSoup(sauce, 'lxml')

            ## These are the fields we are looking for on the website
            home_class = "FootballMatchRow_teamName__28Hxv"
            home_score_class = "FootballMatchRow_score__home__2-xt3"

            away_class = "FootballMatchRow_teamName__28Hxv"
            away_score_class = 'FootballMatchRow_score__away__30bhM'

            home_teams = soup.find_all('span', {'class' : home_class})[::2]
            home_scores = soup.find_all('span', {'class' : home_score_class})

            away_teams = soup.find_all('span', {'class' : away_class})[1::2]
            away_scores = soup.find_all('span', {'class' : away_score_class})


            ## Build a list containing all of our data
            for i in range(len(home_teams)):
                teams = '{} - {}'.format(home_teams[i].text, away_teams[i].text)
                home_team = home_teams[i].text
                away_team = away_teams[i].text
                home_score = home_scores[i].text
                away_score = away_scores[i].text
                score = '{} - {}'.format(home_scores[i].text, away_scores[i].text)
                if home_score == '?':
                    matchs.append((today, home_team, 0, away_team, 0, False))
                else:
                    matchs.append((today, home_team, int(home_score), away_team, int(away_score), True))
                    
        ## Build and return the corresponding DataFrame
        return pd.DataFrame(matchs, columns=['date', 'home_team', 'home_score', 'away_team', 'away_score', 'played'])


# In[ ]:




