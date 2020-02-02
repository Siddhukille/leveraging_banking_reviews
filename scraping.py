# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:16:59 2019

@author: siddhartha Kille
"""

from requests import get
import datetime
import pandas as pd
url_prefix = 'https://www.depositaccounts.com/banks/reviews/'
url_suffix = '.html'
bank_list = ['georgias-own-cu', 'bank-of-america', 'capital-one-360', 'delta-community-credit-union',
             'ally-bank', 'georgia-banking-company', 'wells-fargo-bank', 'synchrony-bank', 'cit-bank',
             'associated-credit-union', 'american-express-national-bank', 'chase-manhattan-bank',
             'citibank', 'us-bank', 'pnc-bank-national-association', 'suntrust-bank']

def check_combine(list_):
    review = ''
    for ele in list_:
        review = review + str(ele)
        review.replace('<br/>', '')
    return review

#dictionary to store reviews of each bank
banks_data_dict = {}

#scraping for each bank_name i,e. for each webpage
for bank_name in bank_list:
    print(bank_name)
    #generating desired URL using dynamic bank_name
    url = url_prefix + bank_name + url_suffix
    response = get(url)
    #list to store all the reviews for each indivisual bank
    bank_review_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #finding and retrieving all review conatiners in that page
        review_containers = soup.find_all('div', class_= 'bankReviewContainer')
        #looping through each review container
        for review in review_containers:
#            print(review)
            #dictionary to store each component of review
            review_dict = {}
            #retrieving all relevant elements from the containers
            name = review.div.meta.get('content')
            if len(list(review.h3)) == 0:
                summary = ''
            else:
                summary = list(review.h3)[0]
            review_id = review.div.div.get('data-id')
            bank_id = review.div.div.get('data-bankid')
            user_id = review.div.div.get('data-userid')
            review_text = check_combine(list(review.p))
            date_posted = review.div.div.span.get('datetime')
            rating_container = review.find_all('meta', itemprop = 'rating')
            rating = rating_container[0].get('content')
            #adding extracted componentsto the dictionary
            review_dict['summary'] = summary
            review_dict['review_id'] = int(review_id)
            review_dict['bank_id'] = int(bank_id)
            review_dict['bank_name'] = name
            review_dict['user_id'] = int(user_id)
            review_dict['rating'] = int(rating)
            review_dict['review'] = review_text
            review_dict['date_posted'] = datetime.datetime.strptime(date_posted, '%Y-%m-%d')
            #adding review to reviews_list
            bank_review_list.append(review_dict)
    else:
        print('Status_code: ', response.status_code, ' for: ', bank_name)
    #adding bank_review_list to the banks_data_dict
    banks_data_dict[bank_name] = bank_review_list
    
    
data_df = pd.DataFrame(columns = list(banks_data_dict['bank-of-america'][0].keys()) )
for bank_name in bank_list:
    bank_reviews = banks_data_dict[bank_name]
    for review in bank_reviews:
        data_df = data_df.append(review, ignore_index = True)
        
data_df.to_csv('./review_data.csv')
            