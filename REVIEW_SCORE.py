

import requests
from bs4 import BeautifulSoup
import urllib.request


review=[]
clean_review = []


ASIN = input('Enter the 10-digit ASIN(Amazon Standard Identification Number) from the url:')
# FOR EG: https://www.amazon.in/dp/B01BHML9M2, here ASIN =  B01BHML9M2



for i in range(2,5):
    url = "https://www.amazon.in/product-reviews/%s/ref=cm_cr_arp_d_paging_btm_next_%s?ie=UTF8&reviewerType=all_reviews&pageNumber=%s"%(ASIN, i, i)
    url_access = urllib.request.urlopen(url)
    
    scraper = BeautifulSoup(url_access,'html.parser')
    
    
    
    for i in scraper.find_all('span', attrs={'class':'a-size-base review-text review-text-content'}):
        per_review = i.find('span')
        print(per_review)
        review.append(per_review)
    
    len(review)
    
    
    
    for each in review:
        clean = str(each).replace('<br/>','')
        clean = clean.replace('<span>','')
        clean = clean.replace('</span>','')
        print(clean)
        clean_review.append(clean)
    
    

with open('Review.txt', "w+", encoding=('utf-8')) as filehandle:
    filehandle.writelines("%s\n" % review for review in clean_review)
    
    
    
    
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

df = pd.DataFrame(clean_review,columns=['Reviews'])
reviews = df

reviews['neg'] = reviews['Reviews'].apply(lambda x:sia.polarity_scores(x)['neg'])
reviews['neu'] = reviews['Reviews'].apply(lambda x:sia.polarity_scores(x)['neu'])
reviews['pos'] = reviews['Reviews'].apply(lambda x:sia.polarity_scores(x)['pos'])

reviews['compound'] = reviews['Reviews'].apply(lambda x:sia.polarity_scores(x)['compound'])


star5 = [j for i, j in enumerate(reviews['Reviews']) if 1 >= reviews['compound'][i] > 0.6]
star4 = [j for i, j in enumerate(reviews['Reviews']) if 0.6 >= reviews['compound'][i] > 0.2]
star3 = [j for i, j in enumerate(reviews['Reviews']) if 0.2 >= reviews['compound'][i] > -0.2]
star2 = [j for i, j in enumerate(reviews['Reviews']) if -0.2 >= reviews['compound'][i] > -0.6]
star1 = [j for i, j in enumerate(reviews['Reviews']) if -0.6 >= reviews['compound'][i] > -1]

avg_star = (5*len(star5) + 4*len(star4) + 3*len(star3) + 2*len(star2) + 1*len(star1)) / (len(star1)+len(star2)+len(star3)+len(star4)+len(star5))

    
    
    
    
    
    


