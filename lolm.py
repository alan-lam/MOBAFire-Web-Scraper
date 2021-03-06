import requests, bs4, sys, multiprocessing, time, platform, webbrowser
import PySimpleGUI as sg
from exports import scrapeGuide1, scrapeGuide2, scrapeGuide3, champions, window, checkbox, misspell_window

MOBAFIRE_URL = 'https://mobafire.com'

if __name__ == '__main__':
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
    
    results = multiprocessing.Manager().dict()
    processes = []

    # scrape web pages
    guide1Process = multiprocessing.Process(target=scrapeGuide1, args=(guide1Link, results))
    processes.append(guide1Process)
    guide1Process.start()
    guide2Process = multiprocessing.Process(target=scrapeGuide2, args=(guide2Link, results))
    processes.append(guide2Process)
    guide2Process.start()
    guide3Process = multiprocessing.Process(target=scrapeGuide3, args=(guide3Link, results))
    processes.append(guide3Process)
    guide3Process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()

    # write to html file and open
    htmlFile = open('lol.html', 'wb')
    guide1 = '<br>'.join(results[0].split('\n'))
    guide2 = '<br>'.join(results[1].split('\n'))
    guide3 = '<br>'.join(results[2].split('\n'))
    html = '<html><head><title>{} guides</title><style>body{{font-family:monospace;}}p{{font-size:150%}}</style></head><body><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p><h1>{}</h1><p>{}</p></body></html>'.format(champion, guide1Title, guide1, guide2Title, guide2, guide3Title, guide3).encode('utf-8')
    htmlFile.write(html)
    htmlFile.close()
    webbrowser.open('lol.html')

    endTime = time.time()
    
    # write time to times.txt
    if timeFlag:
        timeFile = open('times.txt', 'a')
        timeFile.write(platform.system() + ' (multiprocessing) ' + str(endTime-startTime) + '\n')
        timeFile.close()
        import time_analysis
