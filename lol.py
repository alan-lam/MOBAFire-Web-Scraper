import requests, bs4, sys, time, platform, webbrowser
import PySimpleGUI as sg
from guidescrape import scrapeGuide1, scrapeGuide2, scrapeGuide3

MOBAFIRE_URL = 'https://mobafire.com'

# create GUI
sg.theme('DarkBlue')
checkbox = sg.Checkbox('Time Program (Leave unchecked unless you know what it does)')
layout = [[sg.Text('For names with spaces, separate with a dash (e.g. lee-sin)')], [sg.Text('Enter champion name: '), sg.InputText()], [checkbox], [sg.Ok(), sg.Cancel()]]
window = sg.Window('MOBAFire Web Scraper', layout)

# ask for input
while True:
    event, values = window.read()
    if event == 'Ok':
        champion = values[0].lower()
        break
    else:
        window.close()
        sys.exit()
window.close()

# time program if checkbox is checked
timeFlag = checkbox.Get()
if timeFlag:
    startTime = time.time()

# handle champions with space-separated names, common alternative names, or potential misspellings
champions = dict.fromkeys(['sol', 'aurelionsol'], 'aurelion-sol')
champions.update(dict.fromkeys(['blitz'], 'blitzcrank'))
champions.update(dict.fromkeys(['cait'], 'caitlyn'))
champions.update(dict.fromkeys(['cass'], 'cassiopeia'))
champions.update(dict.fromkeys(['gath', 'cho-gath'], 'chogath'))
champions.update(dict.fromkeys(['mundo', 'drmundo'], 'dr-mundo'))
champions.update(dict.fromkeys(['eve'], 'evelynn'))
champions.update(dict.fromkeys(['ez'], 'ezreal'))
champions.update(dict.fromkeys(['fiddle'], 'fiddlesticks'))
champions.update(dict.fromkeys(['gp'], 'gangplank'))
champions.update(dict.fromkeys(['hec'], 'hecarim'))
champions.update(dict.fromkeys(['heim'], 'heimerdinger'))
champions.update(dict.fromkeys(['jarvan', 'iv'], 'jarvan-iv'))
champions.update(dict.fromkeys(['sa', 'kai-sa'], 'kaisa'))
champions.update(dict.fromkeys(['kass'], 'kassadin'))
champions.update(dict.fromkeys(['kat'], 'katarina'))
champions.update(dict.fromkeys(['zix', 'kha-zix'], 'khazix'))
champions.update(dict.fromkeys(['maw', 'kog', 'kog-maw'], 'kogmaw'))
champions.update(dict.fromkeys(['blanc', 'le-blanc'], 'leblanc'))
champions.update(dict.fromkeys(['lee', 'sin', 'leesin'], 'lee-sin'))
champions.update(dict.fromkeys(['liss'], 'lissandra'))
champions.update(dict.fromkeys(['malz'], 'malzahar'))
champions.update(dict.fromkeys(['yi', 'masteryi'], 'master-yi'))
champions.update(dict.fromkeys(['fortune', 'missfortune'], 'miss-fortune'))
champions.update(dict.fromkeys(['mord', 'morde'], 'mordekaiser'))
champions.update(dict.fromkeys(['morg'], 'morgana'))
champions.update(dict.fromkeys(['naut'], 'nautilus'))
champions.update(dict.fromkeys(['nid'], 'nidalee'))
champions.update(dict.fromkeys(['noc', 'noct'], 'nocturne'))
champions.update(dict.fromkeys(['nunu', 'willump', 'nunu-and-willump'], 'nunu-amp-willump'))
champions.update(dict.fromkeys(['ori'], 'orianna'))
champions.update(dict.fromkeys(['panth'], 'pantheon'))
champions.update(dict.fromkeys(['sai', 'rek-sai'], 'reksai'))
champions.update(dict.fromkeys(['renek'], 'renekton'))
champions.update(dict.fromkeys(['sej'], 'sejuani'))
champions.update(dict.fromkeys(['shyv'], 'shyvana'))
champions.update(dict.fromkeys(['raka'], 'soraka'))
champions.update(dict.fromkeys(['kench', 'tahmkench'], 'tahm-kench'))
champions.update(dict.fromkeys(['trist'], 'tristana'))
champions.update(dict.fromkeys(['tryn', 'trynd'], 'tryndamere'))
champions.update(dict.fromkeys(['tf', 'fate', 'twistedfate'], 'twisted-fate'))
champions.update(dict.fromkeys(['koz', 'vel-koz'], 'velkoz'))
champions.update(dict.fromkeys(['vlad'], 'vladimir'))
champions.update(dict.fromkeys(['voli'], 'volibear'))
champions.update(dict.fromkeys(['ww'], 'warwick'))
champions.update(dict.fromkeys(['wuk', 'wu-kong', 'kong'], 'wukong'))
champions.update(dict.fromkeys(['zhao', 'xinzhao', 'xin'], 'xin-zhao'))
champions.update(dict.fromkeys(['yas'], 'yasuo'))
champions.update(dict.fromkeys(['zil'], 'zilean'))

if champion in champions:
    champion = champions[champion]

# make request for mobafire
mobafireLink = MOBAFIRE_URL + '/league-of-legends/' + champion + '-guide'
mobaRes = requests.get(mobafireLink)
try:
    mobaRes.raise_for_status()
except:
    print('Page not found. Mobafire link invalid.')
    sys.exit()

mobaSoup = bs4.BeautifulSoup(mobaRes.text, 'html.parser')

# get guide titles
titles = mobaSoup.select('.browse-list h3')
guide1Title = titles[0].text
guide2Title = titles[1].text
guide3Title = titles[2].text

# get guide links
guides = mobaSoup.select('.browse-list a')
guide1Link = MOBAFIRE_URL + guides[0].attrs['href']
guide2Link = MOBAFIRE_URL + guides[1].attrs['href']
guide3Link = MOBAFIRE_URL + guides[2].attrs['href']

# scrape web pages
results = ['', '', '']
scrapeGuide1(guide1Link, results)
scrapeGuide2(guide2Link, results)
scrapeGuide3(guide3Link, results)

# write to html file and open
htmlFile = open('lol.html', 'wb')
guide1 = '<br>'.join(results[0].split('\n'))
guide2 = '<br>'.join(results[1].split('\n'))
guide3 = '<br>'.join(results[2].split('\n'))
html = '<html><head><title>{} guides</title><style>body{{font-family:monospace;}}</style></head><body><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p></body></html>'.format(champion, guide1Title, guide1, guide2Title, guide2, guide3Title, guide3).encode('utf-8')
htmlFile.write(html)
htmlFile.close()
webbrowser.open('lol.html')

endTime = time.time()

# write time to times.txt
if timeFlag:
    timeFile = open('times.txt', 'a')
    timeFile.write(platform.system() + ' (serial)')
    timeFile.write('\n')
    timeFile.write(str(endTime-startTime))
    timeFile.write('\n')
    import time_analysis
