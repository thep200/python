import os
import requests    #can cai dat
from bs4 import BeautifulSoup #can cai dat

yourPathSave = str(input("Nhap dia chi luu file (vd: f:/, d:/hoc tap/)  "))

listName = ["mononoke", "mimi", "howl" "karigurashi", "chihiro", "kokurikozaka", "kazetachinu", "ponyo", "ged", "ghiblies", "baron", "marnie", "kaguyahime", "yamada"]
# modify listname de crawler theo y minh

Status = True
Count = 0

for keyMain in listName:

    if Status:
        print("Downloading...")
        Status = False
    
    Count += 1


    start = 0
    links = []

    ghibli = "http://www.ghibli.jp/works/" + keyMain + "/#frame"
    url = "http://www.ghibli.jp/gallery/"

    result = requests.get(ghibli)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")

    colection = soup.select('a[href^= \"' + url + keyMain + '\"]')

    for img in colection:
        links.append(img['href'])

    os.mkdir(yourPathSave + "/" + keyMain)
    
    for index, imglink in enumerate(links):
        if start < len(links):
            imgdata = requests.get(imglink).content
            imgname = yourPathSave + "/" + keyMain + "/" + str(index + 1) + ".jpg"
            with open(imgname, 'wb') as file:
                file.write(imgdata)
                start += 1

    if Count == len(listName):
        print("Done!")
    #this is my first change




    





