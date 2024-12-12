from bs4 import BeautifulSoup
import requests
from newspaper import Article
from datetime import datetime, timedelta
import pytz
from urllib.parse import urljoin
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

def summarize(articlee):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize the following text between 300 and 350 words:\n\n{articlee}")
    summary = response.text.strip()
    return summary

def crunchscrape():
    total_pages = 3
    now = datetime.now(pytz.utc)
    results= []

    for page_num in range(1, total_pages + 1):
        url = f"https://techcrunch.com/latest/page/{page_num}/"
        page= requests.get(url)
        soup= BeautifulSoup(page.text, 'lxml')

        headlines = soup.find_all('a', class_='loop-card__title-link')
        links = soup.find_all('a',class_='loop-card__title-link')
        hrefs = [link['href'] for link in links if 'href' in link.attrs]
        timetags = soup.find_all('time', class_='loop-card__meta-item loop-card__time wp-block-tc23-post-time-ago')
        timetag = [timetag['datetime'] for timetag in timetags if 'datetime' in timetag.attrs]

        for headline,hrefs, time_tag in zip(headlines,hrefs, timetag):
            article_time = datetime.fromisoformat(time_tag)
            if now - article_time > timedelta(days=1):
                break         
            article = Article(hrefs)
            article.download()
            article.parse()
            summ= summarize(article.text)
            
            result = {
                "headline": headline.get_text(),
                "link": hrefs,
                "time": time_tag,
                "summary": summ,
            }

            results.append(result)
            time.sleep(1.2)
    time.sleep(15)
    return results

def venturescrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    url= 'https://venturebeat.com/category/ai/'
    page= requests.get(url, headers=headers)
    soup= BeautifulSoup(page.text, 'lxml')
    results= []

    headlines = soup.find_all('h2', class_='ArticleListing__title')
    timetags = soup.find_all('time', class_='ArticleListing__time')
    timetag = [timetag['datetime'] for timetag in timetags if 'datetime' in timetag.attrs]
    now = datetime.now(pytz.UTC)

    for headline, time_tag in zip(headlines, timetag):
        article_time = datetime.fromisoformat(time_tag)
        if now - article_time > timedelta(days=1):
            break
        a_tag = headline.find('a') 
        href= a_tag['href']

        article = Article(href)
        article.download()
        article.parse()

        summ= summarize(article.text)
        result = {
                "headline": headline.get_text(),
                "link": href,
                "time": time_tag,
                "summary": summ,
            }
        results.append(result)
        time.sleep(1.2)
    time.sleep(15)
    return results

def vergescrape():
    url= 'https://www.theverge.com/tech'
    page= requests.get(url)
    soup= BeautifulSoup(page.text, 'lxml')
    results= []

    headlines = soup.find_all('a', class_='after:absolute')
    time_elements = soup.find_all('time')
    time_values = [time_element['datetime'] for time_element in time_elements if 'datetime' in time_element.attrs]
    now = datetime.now(pytz.UTC)

    for headline, time_tag in zip(headlines, time_values):
        article_time = datetime.fromisoformat(time_tag)
        if now - article_time > timedelta(days=1): 
            break
        href= headline['href'] 
        full_url = urljoin(url, href)
        
        article = Article(full_url)
        article.download()
        article.parse()

        summ= summarize(article.text)
        result = {
                "headline": headline.get_text(),
                "link": href,
                "time": time_tag,
                "summary": summ,
            }
        results.append(result)
        time.sleep(1.2)
    return results
