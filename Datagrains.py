import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
import argparse

def saveData(path, filename, header, body):
    Path(path).mkdir(exist_ok=True, parents=True)
    
    with open(path + "/" + filename + ".csv", "w", encoding="utf8", newline="") as fp:
        write = csv.writer(fp)

        write.writerow(header)
        write.writerows(body) 

def getData(url, name):
    text = requests.get(url).text
    soup = BeautifulSoup(text, "lxml")
    tables = soup.find_all("div", {"class":"cotacao"})

    for table in tables:
        tableName = str(table.find("a").text.strip("\n")).replace("/", "-")
        
        thead = table.find("thead")
        thead2 = thead.find_all("th")
        header = [h.text for h in thead2]

        tbody = table.find("tbody")
        tbody2 = tbody.find_all("tr")

        body = list()
        for tr in tbody2:
            
            td = [td.text for td in tr.find_all("td")]
            if td:
                body.append(td)

        saveData(name, tableName, header, body)

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pracas", nargs="+", help="Escolha as praças ex: milho, cafe, soja", required=True)
args = parser.parse_args()

pracas = {
    "milho":"https://www.noticiasagricolas.com.br/cotacoes/milho",
    "soja":"https://www.noticiasagricolas.com.br/cotacoes/soja",
    "cafe":"https://www.noticiasagricolas.com.br/cotacoes/cafe",
}

for praca in args.pracas:
    getData(pracas.get(praca), praca)