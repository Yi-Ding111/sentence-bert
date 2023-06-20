import pandas as pd
from decouple import config
import tweepy
import numpy as np


Bearer_Token=config('Bearer_Token')
Access_Token=config('Access_Token')
Access_Secret=config('Access_Secret')
API_Key=config('API_Key')
API_Key_Secret=config('API_Key_Secret')



class Twitter:
    '''
    Twitter object to ingest and save data
    '''
    def __init__(self,Bearer_Token,Access_Token, 
                      Access_Secret,API_Key,API_Key_Secret) -> None:
        '''
        Initializing tweepy API connection

        parameters:
            Bearer_Token: twitter bearer token env var
            Access_Token: twitter access token env var
            Access_Secret: twitter asscess token secret env var
            API_Key: twitter consumer key env var
            API_Key_Secret: consumer key secret env var
        '''
        self.Bearer_Token=Bearer_Token
        self.Access_Token=Access_Token
        self.Access_Secret=Access_Secret
        self.API_Key=API_Key
        self.API_Key_Secret=API_Key_Secret
        #initialize tweepy client
        self.client=tweepy.Client(bearer_token=self.Bearer_Token,
                                  consumer_key=self.API_Key,
                                  consumer_secret=self.API_Key_Secret,
                                  access_token=self.Access_Token,
                                  access_token_secret=self.Access_Secret,
                                  return_type=[dict])
    
    def valid_user(self,data) -> list:
        '''
        filter records with invalid id

        Parameters:
            data: twitter users info
        '''
        #data=pd.read_table('./twitter_id.txt',delimiter=',')
        #print(data.shape[0])
        #filter all empty rows with null twitter_id
        if data['twitter_userid'].isnull().sum()!=0:
            data['twitter_userid'].replace('',np.nan,inplace=True)
            data.dropna(subset=['twitter_userid'],inplace=True)
        #print(data.shape[0])
        user_id=data.twitter_userid.unique().tolist()

        return user_id
    

    def text_crawler(self,id,tweet_cont) -> list:
        '''
        scrape twitter text based on user id 

        Parameters:
            id : twitter yser id
            tweet_cont: twitter text (list)

        Return:
            tweet_cont
        '''

        response=self.client.get_users_tweets(id=int(id),
                                 max_results=100, 
                                 exclude='retweets',
                                 tweet_fields=['author_id','id','created_at','text'])
        try:
            for tweet in response.data:
                tweet_cont.append([tweet.author_id,tweet.id,tweet.created_at,tweet.text.encode("utf-8")])

            end_time=tweet.created_at
            iter_time=0
        except:
            return tweet_cont

        while len(response)>0 and iter_time<3 and str(end_time)>'2010-11-06T00:00:00-00:00':
            response=self.client.get_users_tweets(id=int(id), 
                                            max_results=100,
                                            exclude='retweets', 
                                            end_time=end_time, 
                                            tweet_fields=['author_id','id','created_at','text'])
            try:
                for tweet in response.data:
                    tweet_cont.append([tweet.author_id,tweet.id,tweet.created_at,tweet.text.encode("utf-8")])
                
                end_time=tweet.created_at
                iter_time+=1

            except:
                break
        
        return tweet_cont
    

    def tweet_save(self,tweet_cont) -> None:
        '''
        save file into txt
        '''
        tweet_df=pd.DataFrame(tweet_cont)#,columns=['twitter_userid','text_id','created_at','text'])
        tweet_df.to_csv('./tweets_text/tweets.txt',header=['twitter_userid','text_id','created_at','text'],index=False)


if __name__=="__main__":
    data=pd.read_table('./twitter_id.txt',delimiter=',')
    twitter=Twitter(Bearer_Token,Access_Token,Access_Secret,API_Key,API_Key_Secret)
    #filter
    user_id=twitter.valid_user(data=data)
    #print(user_id)

    tweets=[]
    for id in user_id:
        tweets=twitter.text_crawler(id=id,tweet_cont=tweets)
    
    #save
    twitter.tweet_save(tweets)