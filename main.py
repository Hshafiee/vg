from pprint import pprint
import requests , re
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    Resutls = {}

    URL = "https://www.vpngate.net/en/"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=URL, headers=headers)


    soup = BeautifulSoup(r.content, 'html5lib') 


    TableList 	= soup.findAll('table', attrs = {'id':'vg_hosts_table_id'})

    ServerTable = TableList[2]

    # ServerTable_Header 	= ServerTable.find('tr')
    # ServerTable_Header 	= ServerTable_Header.find_all('b')
    # ServerTable_Header	= [str(x).replace("<b>" , "") for x in ServerTable_Header]
    # ServerTable_Header	= [str(x).replace("</b>" , "") for x in ServerTable_Header]
    # ServerTable_Header	= [str(x).replace("<br/>" , " ") for x in ServerTable_Header]

    ServerTable_Content	= ServerTable.find_all('tr')[1:]

    for Row in ServerTable_Content :
        RowData             = {}
        ContryRow 	        = Row.find("td")
        Contry		        = re.search(r'<br/>(.*)</td>' , str(ContryRow)).group(1)

        AddressRow	        = Row.find("span" , attrs={'style':'color: #006600;'})
        Address		        = str(AddressRow).replace('<span style="color: #006600;">' , "").replace('</span>' , "")
        RowData['socket']   = Address

        ServerRow	        = Row.select("td:nth-child(2) > span:nth-child(3)" , attrs={'style':'font-size: 10pt;'})
        ServerIP            = str(ServerRow).replace('<span style="font-size: 10pt;">' , "").replace('</span>' , "").replace('[' , "").replace(']' , "")

        RowData['server']   = ServerIP

        if Address != "None" :
            if Contry in Resutls :
                Resutls[Contry].append(RowData)
            else :
                Resutls[Contry] = [RowData]

    return Resutls
