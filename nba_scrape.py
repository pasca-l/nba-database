import requests
import bs4
from lxml import html
import re


def search(url):
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    return soup


def player_url():
    letter = input("input letter >> ")
    soup = search("https://www.basketball-reference.com/players/{}/".format(letter))
    link = soup.find(id="players").find_all('a')
    pattern = "^/players/"
    with open("player_url.txt", 'a') as urltxt:
        for i in link:
            result = re.match(pattern, i.get('href'))
            if result:
                urltxt.write(i.get('href') + '\n')


def player_stats():
    with open("player_info.txt") as infotxt:
        id_dict = {}
        for i in infotxt.readlines():
            temp = {i.split(',')[1].strip() : i.split(',')[0].strip()}
            id_dict.update(temp)

    with open("player_url.txt") as urltxt:
        urls = [i.strip() for i in urltxt.readlines()]
        head = urls[0]
        urls = [head + i for i in urls][1:]

    with open("player_stats.txt", 'a') as statstxt:
        for i in urls:
            soup = search(i)
            name = soup.find('h1', itemprop="name")
            stats = soup.find(id="per_game").find('tbody').find_all(['th', 'td'])
            pattern = "\d{4}-\d{2}"
            for j in stats:
                result = re.match(pattern, j.text)
                if result:
                    statstxt.write('\n' + id_dict[name.text.strip()] + ',' + j.text[:4] + ',')
                    continue
                statstxt.write(j.text + ',')
            statstxt.write('\n\n')
            print(name.text)


def player_image():
    with open("player_url.txt") as urltxt:
        urls = [i.strip() for i in urltxt.readlines()]
        head = urls[0]
        urls = [i.split('/')[-1:][0].replace(".html", ".jpg") for i in urls]
        urls = [head + "/req/202012251/images/players/" + i for i in urls][1:]

    for i, j in enumerate(urls):
        req = requests.get(j)
        if req.status_code == 200:
            print("Downloading: " + j)
            with open("/Users/sy/program/python_program/collecting_program/image/" +
                "{}".format(str(i+1)) + ".jpg", 'wb') as f:
                f.write(req.content)


import os
def image_sql():
    path = "/Users/sy/Desktop/KEIO/データベース概論/データベース概論 プログラムとデータ/image"
    files = os.listdir(path)
    files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
    files_file.sort()

    with open("append_image.sql", 'a') as sqltxt:
        for i in files_file:
            num = i[:-4]
            string = f'update playerinfo set pict=\'{i}\' where playerid={num};\n'
            print(string)
            sqltxt.write(string)


def teamabrev_toid(txtfile):
    with open("team_info.txt") as infotxt:
        id_dict = {}
        for i in infotxt.readlines():
            temp = {i.split(',')[5].strip() : i.split(',')[0].strip()}
            id_dict.update(temp)

    with open(txtfile) as statstxt:
        format = [i for i in statstxt.readlines() if len(i.split(',')) == 32]

    formatted = []
    for i in format:
        list = i.split(',')
        try:
            list[3] = id_dict[list[3]]
        except:
            with open("team_info.txt") as infotxt:
                counter = len(infotxt.readlines()) + 1
                team = list[3]
                list[3] = str(counter)
            with open("team_info.txt", 'a') as infotxt:
                infotxt.write(str(counter) + ',,,,,' + team + ',\n')
            with open("team_info.txt") as infotxt:
                id_dict = {}
                for i in infotxt.readlines():
                    temp = {i.split(',')[5].strip() : i.split(',')[0].strip()}
                    id_dict.update(temp)
        data = ','.join(list)
        formatted.append(data)

    with open(txtfile, 'w') as statstxt:
        statstxt.writelines(formatted)


def players():
    with open("player_url.txt") as urltxt:
        urls = [i.strip() for i in urltxt.readlines()]
        head = urls[0]
        urls = [head + i for i in urls][1:]

    with open("player_info.txt", 'a') as infotxt:
        counter = 1
        for i in urls:
            soup = search(i)
            soup = soup.find(id="meta")
            name = soup.find(itemprop="name").text.strip()

            try:
                height = soup.find(itemprop="height").text
            except:
                height = ''

            try:
                weight = soup.find(itemprop="weight").text[:-2]
            except:
                weight = ''

            try:
                bday = soup.find(itemprop="birthDate").text
            except:
                bday = ''
            else:
                bday = bday.strip()[:-4].strip().strip(',') + ' ' + bday.strip()[-4:]

            try:
                bplace = soup.find(itemprop="birthPlace").text.strip().split(',')[1][1:]
            except:
                bplace = ''

            list = [counter, name, height, weight, bday, bplace]
            print(list)
            for j in list:
                infotxt.write(str(j) + ',')
            infotxt.write('\n')
            counter += 1


def teams():
    teams = ['TOR', 'BOS', 'NYK', 'BRK', 'PHI', 'CLE', 'IND', 'DET', 'CHI',
             'MIL', 'MIA', 'ATL', 'CHO', 'WAS', 'ORL', 'OKC', 'POR', 'UTA',
             'DEN', 'MIN', 'GSW', 'LAC', 'SAC', 'PHO', 'LAL', 'SAS', 'DAL',
             'MEM', 'HOU', 'NOP']

    with open("team_info.txt", 'a') as teamtxt:
        counter = 1
        for i in teams:
            name = input(i + " team name >> ")
            conference = input(i + " conference >> ")
            division = input(i + " division >> ")
            coach = input(i + " coach >> ")

            list = [counter, name, conference, division, coach, i]
            for j in list:
                teamtxt.write(str(j) + ',')
            teamtxt.write('\n')
            counter += 1


def match_url():
    letter = input("input month >> ")
    soup = search("https://www.basketball-reference.com/leagues/NBA_2020_games-{}.html".format(letter))
    link = soup.find(id="schedule").find_all('a')
    pattern = "/boxscores/.*html"
    with open("match_url.txt", 'a') as urltxt:
        for i in link:
            result = re.match(pattern, i.get('href'))
            if result:
                urltxt.write(i.get('href') + '\n')
                print(result)


def match_schedules():
    letter = input("input month >> ")
    soup = search("https://www.basketball-reference.com/leagues/NBA_2020_games-{}.html".format(letter))
    match = soup.find(id="schedule").text.replace("Box Score", " ").replace("0p", "0p ").split('\n')
    with open("match_info.txt", 'a') as matchtxt:
        for i in match:
            if len(i) >= 30:
                matchtxt.write(i + '\n')
                print(i)


# def match_reform():
#     with open("match_info.txt") as matchtxt:
#         lines = matchtxt.readlines()
#     with open("match_info2.txt", 'a') as matchtxt:
#         for i in lines:
#             result = re.sub(",", "", i)
#             print(result)
#             matchtxt.write(result)


def teamname_toid():
    with open("match_info.txt") as matchtxt:
        lines = matchtxt.readlines()

    with open("team_info.txt") as infotxt:
        id_dict = {}
        for i in infotxt.readlines():
            temp = {i.split(',')[1].strip() : i.split(',')[0].strip()}
            id_dict.update(temp)
        del id_dict[""]

    with open("match_info.txt", 'w') as matchtxt:
        for i in lines:
            for j in id_dict:
                i = re.sub(j, id_dict[j], i)
            matchtxt.write(i)
            print(i)


import random
def goods_generator():
    with open("goods_info.txt", 'a') as goodstxt:
        for j in range(30):
            items = ["t-shirt s-size", "t-shirt m-size", "t-shirt l-size", "socks", "blanket",
                    "gift basket", "duffle bag", "plaque", "photograph A", "photograph B",
                    "photograph C", "hat", "hoodie", "jersey"]
            choice = random.sample(items, 10)

            for i in choice:
                info = str(j+1) + "," + i + ",{:.2f}".format(random.uniform(30, 120))
                goodstxt.write(info + '\n')
                print(info)


def goods_idwithname():
    with open("goods_name.txt", 'a') as goodstxt:
        items = ["t-shirt s-size", "t-shirt m-size", "t-shirt l-size", "socks", "blanket",
                "gift basket", "duffle bag", "plaque", "photograph A", "photograph B",
                "photograph C", "hat", "hoodie", "jersey"]
        for i, name in enumerate(items):
            goodstxt.write(str(i+1) + ',' + name + '\n')
            print(i, name)


def goods_format():
    items = ["t-shirt s-size", "t-shirt m-size", "t-shirt l-size", "socks", "blanket",
            "gift basket", "duffle bag", "plaque", "photograph A", "photograph B",
            "photograph C", "hat", "hoodie", "jersey"]
    itemdict = {}
    for i, name in enumerate(items):
        temp = {name : i+1}
        itemdict.update(temp)

    with open("goods.csv") as goodstxt:
        for i in goodstxt.readlines():
            i = i.split(',')
            i = i[1:]
            i[1] = str(itemdict[i[1]])
            i = ','.join(i)
            with open("goods_info.txt", 'a') as goods2txt:
                goods2txt.write(i)
            print(i)


def main():
    image_sql()


if __name__ == '__main__':
    main()
