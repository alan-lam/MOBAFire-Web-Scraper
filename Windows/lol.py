import requests, bs4, sys, webbrowser
import PySimpleGUI as sg
from exports import scrapeGuide1, scrapeGuide2, scrapeGuide3, champions, dist_window, misspell_window

MOBAFIRE_URL = 'https://mobafire.com'

# ask for input
while True:
    event, values = dist_window.read()
    if event == 'Ok':
        champion = values[0].lower()
        break
    else:
        dist_window.close()
        sys.exit()
dist_window.close()

if champion in champions:
    champion = champions[champion]

# make request for mobafire
mobafireLink = MOBAFIRE_URL + '/league-of-legends/' + champion + '-guide'
mobaRes = requests.get(mobafireLink)
try:
    mobaRes.raise_for_status()
except:
    misspell_window.read()
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
html = '<html><head><title>{} guides</title><style>body{{font-family:monospace;}}p{{font-size:150%}}</style></head><body><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p></body></html>'.format(champion, guide1Title, guide1, guide2Title, guide2, guide3Title, guide3).encode('utf-8')
htmlFile.write(html)
htmlFile.close()
webbrowser.open('lol.html')
