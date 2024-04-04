import datetime
import os
from subprocess import run
import requests
from bs4 import BeautifulSoup
def get_current_date():
    '''Using datetime module and it's formating, I made this function to get the day date in the formate of the url'''
    current_date = datetime.datetime.today()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    return f"{day}/{month}/{year}"
def request_website():
    '''Testing the connection'''
    try:
        req = requests.get(url=f'https://mobile.yallakora.com/match-center/مركز-المباريات?date={get_current_date()}#days',timeout=10)
    except TimeoutError:
        raise TimeoutError
    return req
def get_data():
    '''getting the data and fetching it'''
    content = BeautifulSoup(request_website().content,"xml")
    match_week = content.find_all('div',{'class':'date'})
    teamA = content.find_all('div',{'class':'teams teamA'})
    teamB = content.find_all('div',{'class':'teams teamB'})
    matchTime = content.find_all('span',{'class':'time'})
    matchStat = content.find_all('div',{'class':'matchStatus'})
    formatted_data = ""
    for i in range(len(teamA)):
       formatted_data += (
    f"\nWeek of the match => {match_week[i].text.strip()}\n"
    f"Team A :\t{teamA[i].text.strip()}\n"
    f"Team B :\t{teamB[i].text.strip()}\n"
    f"Time of the match => {matchTime[i].text.strip()}\n"
    f"Status of the match => {matchStat[i].text.strip()}\n" + 50 * "-"
)
    return formatted_data
def present_data(choice ='2'):
    '''by using os and subprocess modules, I present data in text file accoeding to user choice'''
    dir = os.getcwd()
    file_path = os.path.join(dir,"matches.txt")
    if choice == '1':
        with open(file_path, "a",encoding="utf-8") as file_write:
            file_write.write('\n' + get_current_date().center(50,'=') + '\n')
            file_write.write(get_data())
            file_write.close()
        run(["start",file_path],shell=True)
    elif choice == '2':
        with open(file_path, "w",encoding="utf-8") as file_write:
            pass
        with open(file_path, "a",encoding="utf-8") as file_write:
            file_write.write('\n' + get_current_date().center(50,'=') + '\n')
            file_write.write(get_data())
            file_write.close()
        run(["start",file_path],shell=True)
    else:
        raise ValueError("please Enter valid number 1 or 2")
print('''This app will show the matches today in a text file''')
answer = input('''Do you want to clear the file
                  Please chosse number (1 or 2)
                  (1) I don't want to clear this file
                  (2) I want to clear the file
                  Note that in case you don't chooce the default is (2)''').strip()
present_data(answer)
