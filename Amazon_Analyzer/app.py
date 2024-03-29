import sys
from streamlit import cli as stcli
import pickle
import streamlit as st

import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.downloader.download('vader_lexicon')


 
@st.cache()
  
def prediction(URL):
    
    review=[]
    clean_review = []
    
    l1 = URL.split("/")
    print(l1)
    key = l1.index("dp")
    asin = l1[key+1]
    
    for i in range(2,5):
        try:
            url = "https://www.amazon.in/product-reviews/%s/ref=cm_cr_arp_d_paging_btm_next_%s?ie=UTF8&reviewerType=all_reviews&pageNumber=%s"%(asin, i, i)
            url_access = urllib.request.urlopen(url)
            
            
        except HTTPError as e:
            
            if(str(e) == "HTTP Error 404: Not Found" ):
                return -2
            
        
        
        scraper = BeautifulSoup(url_access,'html.parser')
        
        for i in scraper.find_all('span', attrs={'class':'a-size-base review-text review-text-content'}):
            per_review = i.find('span')
            review.append(per_review)
        
        len(review)
        
        
        
        for each in review:
            clean = str(each).replace('<br/>','')
            clean = clean.replace('<span>','')
            clean = clean.replace('</span>','')
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
    return avg_star

def main():       
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">AMAZON REVIEW SCORE</h1> 
    </div> 
    """
      
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    URL = st.text_input("Enter Amazon Product Link:")
    
      
    if st.button("Predict"): 
        if(len(URL)==0):
            st.warning("Please enter a URL")
            st.stop()
    
        if('amazon' not in URL and len(URL)!=0):
            st.warning("Please enter a valid Amazon URL")
            st.stop()
        result = prediction(URL) 
        if(int(result) == -2):
            st.warning('Product Not Found!')
            st.stop()
        else:
            st.success('Product Score is {:.1f} stars'.format(result))
            
    
    
     
if __name__=='__main__': 
    main()

