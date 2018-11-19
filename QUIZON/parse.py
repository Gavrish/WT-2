import lxml
from bs4 import BeautifulSoup
import lxml
import pickle
import json
import sys
import urllib.request
sys.setrecursionlimit(1000)
soup = BeautifulSoup(open('celebrity.html'),"lxml")

def findData(tag):
    if(tag.has_attr('class') and tag['class'][0]=="data"):
        # print(tag)
        return True
    else:
        # print(tag)
        return False
y=soup.tbody.find_all(findData)
celebrities=[]
for data in y:
    celebrities.append(data.contents[5].a.string)
    img_url=data.td.img["src"].split("/")

    img_url.pop()
    img_url.append("0x0.jpg")
    img_url[0]="https:"
    img_url="/".join(img_url)
    print(img_url)
    # urllib.request.urlretrieve(img_url, "celebPics/"+data.contents[5].a.string+".jpg")

print(len(celebrities))
# with open('celeb.txt', 'w') as fp:
#     json.dump(celebrities, fp)
