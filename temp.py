import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
workbook = xlsxwriter.Workbook('Buzdolabi Inceleme.xlsx')
worksheet = workbook.add_worksheet()
url1 = "https://www.hepsiburada.com/samsung-rt46k6000ww-tr-no-frost-buzdolabi-p-MTSAMRT46K6000WWTR"
url2 = "https://www.hepsiburada.com/profilo-bd2155wfnn-f-enerji-sinifi-453-lt-nofrost-ustten-donduruculu-buzdolabi-p-HBCV00000OTS59"
url3 = "https://www.hepsiburada.com/vestel-nf45001-no-frost-buzdolabi-p-HBCV000004EJI3"
url4 = "https://www.hepsiburada.com/bosch-kdn55nwf1n-453-lt-no-frost-buzdolabi-p-HBCV00000UH4UY"
url5 = "https://www.hepsiburada.com/altus-alk-471-x-514-lt-no-frost-buzdolabi-p-HBCV000004XEHQ"

url_liste = [url1, url2, url3, url4, url5]
genel_liste = []
sayac = 0
satir=0
satir5=0
satir6=0
for i in range(5):
    link = url_liste[i]
    response = requests.get(url_liste[i], headers=headers)
    html_icerigi = response.content
    soup = BeautifulSoup(html_icerigi,"html.parser")
    isim = soup.find("h1", {"itemprop" : "name"}).text.strip()
    fiyat = soup.find("span", {"data-bind" : "markupText:'currentPriceBeforePoint'"}).text
    puan = soup.find("span", {"class" : "hermes-AverageRateBox-module-g3di4HmmxfHjT7Q81WvH"}).text
    marka = soup.find("span", {"class" : "brand-name"}).text
    yorum_link = soup.find("a", {"class" : "hermes-Maestro-module-XAIcq5L_jAzoDcgS2PtF hermes-Maestro-module-jvao1_hTA8K6hu1rH1Ma hermes-Maestro-module-LktAajyTR1DN5rj22WiD"})
    yorum_link = yorum_link.get("href")
    yorum_link1 = yorum_link + "?sayfa=" 
    ort=0  
    x=1
    y_liste = list()
    yp_liste = list()

    for k in range(7):   

        yorum_link2 = yorum_link1 + str(x) + ""
        x = x + 1
        print(yorum_link2)
        r2 = requests.get(yorum_link2, headers=headers)
        soup2 = BeautifulSoup(r2.content, "html.parser")
        st1 = soup2.find_all("div", {"class" : "hermes-ReviewCard-module-BJtQZy5Ub3goN_D0yNOP"})        
        yorum_puan = soup2.find_all("div", {"class" : "hermes-RatingPointer-module-UefD0t2XvgGWsKdLkNoX"}) 
        for i in range(10):
            print("deneme")
            yorum_puan2 = yorum_puan[i].find_all("div", {"class" : "star"})
            yorum_puan2 = len(yorum_puan2)
            print(yorum_puan2)
            ort = ort + yorum_puan2
            yorum = st1[i].find("span", {"itemprop" : "description"})
            if yorum == None:
                if yorum_puan2 == 1:
                        yorum = "Çok kötü. Asla almayın."
                elif yorum_puan2 == 2:
                        yorum = "Kötü. Bu ürünü tavsiye etmem."
                elif yorum_puan2 == 3:
                        yorum = "Orta. Ortalama bir ürün. İşinizi görebilir."
                elif yorum_puan2 == 4:
                        yorum = "İyi. Parasınun karşılığını veriyor. Tavsiye ederim."
                elif yorum_puan2 == 5:
                        yorum = "Çok iyi. Muhteşem bir ürün. Bu ürünü kesinlikle alabilirsiniz."
            else:
                yorum = (yorum.text)
            print(yorum)
            yp_liste.append(yorum_puan2)
            y_liste.append(yorum)
            worksheet.write(satir5,5,yorum_puan2)
            satir5 = satir5 + 1
            worksheet.write(satir6,6,yorum)
            satir6 = satir6 + 1
    ort = ort / 70
    ort = round(ort,1)
    genel_liste.append([isim, marka, puan, fiyat, link])    
    worksheet.write(satir,0,isim)
    worksheet.write(satir,1,marka)
    worksheet.write(satir,2,puan)
    worksheet.write(satir,3,fiyat)
    worksheet.write(satir,4,link)
    satir = satir + 70

    sayac = sayac + 1
    if(sayac==5):
        break   

workbook.close()