import requests
import re
from bs4 import BeautifulSoup
import csv

def movie_birth(url_birth):
    page_birth = requests.get(url_birth)
    soup_birth = BeautifulSoup(page_birth.content, 'html.parser')
    listers = soup_birth.findAll("div", class_="lister-item mode-detail")
    birth_list=[]

    for lister in listers:
        image_lister = lister.findAll("div", class_="lister-item-image")
        image = image_lister[0].img["src"]
        birth = [image]
        name_lister = lister.findAll("h3",class_="lister-item-header")
        name = name_lister[0].a.text.strip()
        birth.append(name)
        details_lister = lister.findAll("p",class_="text-muted text-small")
        details = []
        for detail in details_lister:
            details.append(detail.text.strip())
            for i in details:
                i = i.split(' |\n ')
                if len(i) == 2:
                    profession = i[0]
                    birth.append(profession)
                    bestwork = i[1]
                    birth.append(bestwork)
                else:
                    profession = 'null'
                    birth.append(profession)
                    bestwork = i[0]
                    birth.append(bestwork)
                birth_list.append(birth)

    return birth_list
   
url_front = "https://www.imdb.com/search/name?birth_monthday="

for month in range(1,13):
    for day in range(1,32):
         month_2d  = '{:02d}'.format(month)
         day_2d = '{:02d}'.format(day)
         for i in range(0,41):
             page = i*50
             if page < 50 :
                 url_birth = url_front + str(month_2d) + "-" + str(day_2d)
             else:
                 url_birth = url_front + str(month_2d) + "-" + str(day_2d) + "&start=" + str(page+1) + "&ref_=rlm"
             
            
             print(url_birth)
             content = movie_birth(url_birth)
             if len(content) > 0:
                filepath = month_2d+day_2d+"_"+str(i+1)+".csv"
                
                with open(filepath, 'w', newline='') as csvfile:
                    mywriter = csv.writer(csvfile)
                    mywriter.writerows(content)   
                    print(filepath,"saved.")
             elif len(content) == 0:
                  break
