from urllib.request import urlopen                              #for open site in html file
from urllib.parse import unquote                                #unquote for decrypt url
from bs4 import BeautifulSoup


def send_results(page):
    dict_of_results = {}
    #Exception from rules
    dict_of_excptn = {0 : 'Википедия', 1 : 'Служебная', 2 : 'Категория', 3 : 'Портал', 4 : 'Special', 5 : 'index', 6 : 'Шаблон', 7 : 'Обсуждение', 8 : 'Файл', 9 : 'Проект'}
    excptn_cntr = 10
    html = urlopen(page)
    file_of_results = open('result.txt', 'w')
    doc = BeautifulSoup(html.read(), features = 'lxml');        #BeautifulSoup for parsing html file
    for link in doc.find_all('a'):
        url = str(link.get('href'))
        flag = 0                                                #flag for exceptions 
        if(url.find('wiki', 1, 5) != -1):                       #if the link is relative
            url = 'https://ru.wikipedia.org' + url
            
        url = unquote(url)                                      #unquote for decrypt url   
        for excptn in dict_of_excptn.values():
            if((url.find(excptn, 0, -1) != -1) or (excptn == url)):
                flag = 1
            
        if((url.find('https://ru.wikipedia.org', 0, -1) != -1) and (flag != 1)):
            file_of_results.write(url + '\n')
#           dict_of_results.setdefault(excptn_cntr - 10, url)
            dict_of_excptn.setdefault(excptn_cntr, url)         #add temporary exceptions
            excptn_cntr += 1 
    file_of_results.close()
    for i in range(excptn_cntr - 1, 9, -1):                     #remove all temporary exceptions
        dict_of_excptn.pop(i, )

def get_rules():
    list_of_rules = open('rules.txt')
    return list_of_rules

def print_line(from_line):
    file_of_results = open('result.txt', 'r')
    list_of_results = 'Choose option from the proposed: \n'
    cntr = 0
    for i, line in enumerate(file_of_results):
        if(i >= from_line and i <= from_line + 10):
            list_of_results = list_of_results + str(i + 1) + ' ' + line
            cntr += 1
            break
    from_line += cntr
    file_of_results.close()
    return list_of_results, from_line
