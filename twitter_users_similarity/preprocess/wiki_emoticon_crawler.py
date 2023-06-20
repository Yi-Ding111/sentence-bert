from cgitb import html
from urllib import response
from bs4 import BeautifulSoup
import requests

from requests.exceptions import HTTPError
import pandas as pd
import json
wiki_url='https://en.wikipedia.org/wiki/List_of_emoticons'
table_name='Sideways Latin-only emoticons'
emoticions={}
try:
    response=requests.get(wiki_url)
    soup=BeautifulSoup(response.text,'html.parser')
    for content in soup.find_all('table',attrs={'class':"wikitable"}):
        #print(content.prettify())
        #print('------------------------------------')
        try:
            #print(content.caption.get_text().strip())
            if content.caption.get_text().strip()=='Sideways Latin-only emoticons':
                #print(content.find_all('th'))
                table_title=content.find_all('th')
                title_list=[]
                for title in table_title:
                    title_list.append(title.get_text().strip())
                #print(title_list)
                #break
                all_icon=[]
                trs=content.tr
                for tr in trs.find_next_siblings('tr'):
                    row_icon=[]
                    tds=tr.td
                    row_icon.append([str(x) for x in tds if getattr(x, 'name', None) !='br'])
                    for td in tds.find_next_siblings('td'):
                        row_icon.append([str(x) for x in td if getattr(x, 'name', None) !='br'])
                        #row_icon.append(list(td.stripped_strings.strip('\n')))
                    all_icon.append(row_icon)
                #print(all_icon)
                # all_mean=content.find_all('a')
                # for mean in all_mean:
                #     print(mean.get_text())
                #print(all_icon)
                #print(trs.find_next_siblings('tr'))
                #for tr in trs.find_next_siblings('tr'):
                    #print(tr)
                #print(trs.find_next_sibling('td'))
                #print([x for x in trs if getattr(x,'name',None)!='br'])
                #print([x for x in tr.find_next_sibling('td').contents if getattr(x, 'name', None) != 'br'])
                for row in all_icon:
                    try:
                        soup2 = BeautifulSoup(row[-1][0],'html.parser')
                        mean=str(soup2.get_text())
                    except:
                        mean='Error'

                    for col1 in row[:-2]:
                        for ele in col1:
                            eicon=ele.strip()
                            emoticions[eicon]=mean
                #print(emoticions)
        except:
            continue
    
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')

except Exception as err:
    print(f'Other error occurred: {err}')


#saving
with open('emoticon2.json', 'w',encoding='utf8') as fp:
    json.dump(emoticions, fp,  indent=4, ensure_ascii=False)