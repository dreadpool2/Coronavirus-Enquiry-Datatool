import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

#Ignore SSL Errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# below func for removing < and >
def funcSplit(y):
    if(len(y) <= 2):
        return ""
    first = y.split(">")
    second = first[1].split("<")
    if(second[0] == '' or second[0] == ' '):
        return "0"
    if(second[0] == "N/A"):
        return "0"
    return second[0]
    
url_a = "https://www.worldometers.info/coronavirus/?"
url =  urllib.request.Request(url_a, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup("tr")
defo = list()

countriesCases = dict()
countriesDeaths = dict()
countriesRecover = dict()
countries = list()

max_cases = 0;
for i in range(9, 221):
    list_1 = re.findall(">.*?<",str(tags[i]))
    temp = list()
    for obj in list_1:
        string_1 = funcSplit(obj)
        temp.append(string_1)
    defo.append(temp)
    max_cases = max(max_cases, int(temp[3].replace(',','')))
    print("Progress - "+str(i)+"/456")
 
def full_table(cases):
    correct_index = 0
    print("\n")
    listHead = ["", "Country", "","Cases", "NewCases", "Deaths", "NewDeaths", "Recovered", "A. Cases","Serious", "PopC-Rat.", "PopD-Rat.", "Ttl-Tests", "PopT-Rat.", "Continent"]
    print("{: ^2} {: ^24} {: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}".format(*listHead))
    listHead = ["", "-------", "","-----", "--------", "------", "---------", "---------", "--------","-------", "---------", "---------", "---------", "---------", "---------"]
    print("{: ^2} {: ^24} {: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}".format(*listHead))

    ranged = cases.split(' ')
    for i in range(0, 212):
        if(int(defo[i][3].replace(',','')) >= int((ranged[0]).replace(',','')) and int(defo[i][3].replace(',','')) <= int((ranged[1]).replace(',',''))):
            correct_index+=1
            defo[i][0] = correct_index    
            print("{: ^2} {: ^24} {: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}{: ^10}".format(*defo[i]))

def sort_cases_inc(cases):
    defo.sort(key = lambda x: int(x[3].replace(',','')))
    full_table(cases)

def sort_cases_dec(cases):
    defo.sort(key = lambda x: int(x[3].replace(',','')), reverse=True)
    full_table(cases)

def sort_continent(cases):
    defo.sort(key = lambda x: x[14])
    full_table(cases)

def sort_deaths_inc(cases):
    defo.sort(key = lambda x: int(x[5].replace(',','')))
    full_table(cases)

def sort_deaths_dec(cases):
    defo.sort(key = lambda x: int(x[5].replace(',','')), reverse=True)
    full_table(cases)

def sort_rec_rat(cases):
    defo.sort(key = lambda x: 0 if (x[7] == '') else int(x[7].replace(',',''))/int(x[3].replace(',','')), reverse=True)
    full_table(cases)

def sort_dec_new(cases):
    defo.sort(key = lambda x: 0 if (x[4] == '') else int(x[4].replace(',','')), reverse=True)
    full_table(cases)

def sort_dec_death(cases):
    defo.sort(key = lambda x: 0 if (x[6] == '') else int(x[6].replace(',','')), reverse=True)
    full_table(cases)

def sort_dec_death_rate(cases):
    defo.sort(key = lambda x: 0 if (x[5] == '') else int(x[5].replace(',',''))/int(x[3].replace(',','')), reverse=True)
    full_table(cases)

def sort_ttl_cas_rat(cases):
    defo.sort(key = lambda x: 0 if (x[12] == '') else int(x[12].replace(',',''))/int(x[3].replace(',','')), reverse=True)
    full_table(cases)

switcher={
            0: full_table,
            1: sort_cases_inc,
            2: sort_cases_dec,
            3: sort_continent,
            4: sort_deaths_inc,
            5: sort_deaths_dec,
            6: sort_dec_new,
            7: sort_dec_death,
            8: sort_dec_death_rate,
            9: sort_ttl_cas_rat,
            10: sort_rec_rat
         }

while(True):
    print("\n*****Enquiry Kiosk*****\n")
    print("1]Full Table")
    print("2]Table Sorted According to Increasing Cases")
    print("3]Table Sorted According to Decreasing Cases")
    print("4]Table Sorted According to Continent")
    print("5]Table Sorted According to Increasing Deaths")
    print("6]Table Sorted According to Decreasing Deaths")
    print("7]Table Sorted According to Decreasing New Cases")
    print("8]Table Sorted According to Decreasing New Deaths")
    print("9]Table Sorted According to Death Rate [Decreasing Order]")
    print("10]Table Sorted According to Cases/Total-Tests-Taken [Decreasing Order]")
    print("11]Table Sorted According to Recovered/Cases Ratio [Decreasing Order]\n\n")


    inp = input("Enter your Query No.: ")
    inp1 = input("Enter Range of Cases (Min-cases Max-Cases) [Max Cases - "+str(max_cases)+"] : ")
    
    switcher[int(inp)-1]("0 "+str(max_cases)) if inp1 == 'N' else switcher[int(inp)-1](inp1)

    
