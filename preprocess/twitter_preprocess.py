from concurrent.futures import process
import pandas as pd
import numpy as np
import re
import ast
import demoji
import json

from multiprocessing.sharedctypes import Array

from sentence_transformers import SentenceTransformer
from torch import embedding



class preprocess():
    '''
    preprocess data for SBERT
    '''

    def __init__(self) -> None:
        pass


    def decode_text(self,text:str) -> str:
        '''
        decode byte-string decodeto character string
        use.pandas.series.apply()

        Parameters:
            text: str (pandas.series)
        '''
        try:
            result = ast.literal_eval(text)
        finally:
            return result.decode() if isinstance(result, bytes) else text
    

    def clean_text(self,text:str) -> str:
        '''
        text data clean
        use pandas.series.map()

        Parameters:
            text: str  (pandas.series)
        '''
        #remove text meaningless patterns
        remove_re=r'|'.join([r'@[^ ]+',r'https?://[A-Za-z0-9./]+',
                            r'\'s',r'\#\w+',r'&amp ',r'RT',r'www\S+'])
        
        text=re.sub(remove_re,'',text)
        text=re.sub(r'\s+',' ',text) 
        

        return text.strip(' ')


    def notation_check(self,text:str) -> str:
        '''
        check special notations (emoji and emoticon) and in text expression
        use pandas.series.apply()

        Parameters: str (pandas.series)
        '''
        # replace emoji with text
        for emoji,content in demoji.findall(text).items():
            text=text.replace(emoji,' '+content+' ')
            text=re.sub(r'\s+',' ',text)
        
        #replace emoticons with text
        with open('emoticon.json') as pf:
            emoticons=json.load(pf)
        for emoticion, content in emoticons.items():
            text=text.replace(emoticion,' '+content+' ')
            text=re.sub(r'\s+',' ',text)

        return text


    def model_embedding(self,text:pd.Series) -> Array:
        '''
        sentence embedding use sbert
        from Hugging Face: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

        Parameters:
            text: sentence list,
                    group by user_id
        '''
        #pd.series -> list
        #print(data['text'][:20].tolist())
        text=text.tolist()
        #transformer
        sbert = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        embeddings=sbert.encode(text)

        return embeddings


    def embedding_save(self,user_id:int, embeddings:Array) -> pd.DataFrame:
        '''
        save each users sentences embedding s in dataframe

        Parameters:
            user_id: the twitter id of user
            embeddings: the array of SBERT vectors
        '''

        #cal the mean of vectors from one user
        vec_mean=embeddings.mean(axis=0)
        # array -> tolist
        #vec_mean=np.asarray(vec_mean)
        #vec_mean=vec_mean.tolist()
        user_vec_df=pd.DataFrame(data=[vec_mean], columns= [f'D{x+1}' for x in range(vec_mean.shape[0])])
        #insert user_id into dataframe
        user_vec_df.insert(0,"user_id",user_id)

        return user_vec_df

    
    def data_process(self,text_series:pd.Series) ->pd.Series:
        '''
        process sentences into available format

        Parameters:
            text_series: the dataframe of twitter contents

        Return:
            the dataframe series 
        '''
        #decode sentence text
        text_series=text_series.apply(self.decode_text)
        #string normalization
        text_series=text_series.str.normalize('NFKD')
        #remove meaningless info
        text_series=text_series.map(self.clean_text)
        text_series=text_series.apply(self.notation_check)

        return text_series



if __name__=="__main__":
    # data=pd.read_table('./tweets_text/tweets.txt',delimiter=',',header=0)
    # data=data.loc[data['twitter_userid']==27260086][:10]

    # tweet_preprocess=preprocess()
    # data['text']=tweet_preprocess.data_process(data['text'])

    # #grab distinct user's id
    # user_id=(data['twitter_userid'].unique())[0]
    # embeddings=tweet_preprocess.model_embedding(data['text'])
    # user_vec_df=tweet_preprocess.embedding_save(user_id,embeddings)
    # print(user_vec_df)


    #initial object
    # tweet_preprocess=preprocess()
    # user_ids=data['twitter_userid'].unique()

    # #empty stack 
    # emb_vecs=pd.DataFrame()

    # for user_id in user_ids:
    #     #select tweet from specific user
    #     user_tweets=data.loc[data['twitter_userid']==user_id]
    #     #clean tweets for SBERT embedding
    #     user_tweets['text']=tweet_preprocess.data_process(user_tweets['text'])
    #     #sentence embeddings
    #     embeddings=tweet_preprocess.model_embedding(user_tweets['text'])
    #     #save embedding vectors into dataframe
    #     user_vec_df=tweet_preprocess.embedding_save(user_id=user_id,embeddings=embeddings)
    #     #concat dataframes
    #     emb_vecs=pd.concat([emb_vecs,user_vec_df],ignore_index=True)
    
    # #print(emb_vecs)
    pass

