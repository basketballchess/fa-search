import cloudscraper
from lxml import html

from bs4 import BeautifulSoup
import pandas as pd
import time

scraper = cloudscraper.create_scraper()
root = "https://www.iafd.com"

def scrape(url: str, retries=0):
    global iafd_uuid_url
    try:
        scraped = scraper.get(url, timeout=(3, 20))
    except requests.exceptions.Timeout as exc_time:
        log.debug(f"Timeout: {exc_time}")
        return scrape(url, retries + 1)
        print("A")
    except Exception as e:
        log.error(f"scrape error {e}")
        sys.exit(1)
        print("B")

    if scraped.status_code >= 400:
        if retries < 10:
            wait_time = random.randint(1, 4)
            log.debug(f"HTTP Error: {scraped.status_code}, waiting {wait_time} seconds")
            time.sleep(wait_time)
            return scrape(url, retries + 1)
        log.error(f"HTTP Error: {scraped.status_code}, giving up")
        print("C")

        sys.exit(1)

    iafd_uuid_url = scraped.url
    return scraped.content



url = f"{root}/distrib.rme/distrib=7300/d%26e-media-networks.htm"

txt = scrape(url)

soup = BeautifulSoup(txt, 'html.parser')
tbody = soup.find('tbody')


# Extract the data from the tbody
data = []
for row in tbody.find_all('tr'):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    link = row.find('a').get('href')
    cols.append(f"{root}{link.strip()}")
    data.append(cols)

count = 0
for row in data:
    vidLink = row[-1]
    vidTxt = scrape(vidLink)
    soupVid = BeautifulSoup(vidTxt, 'html.parser')

    if (soupVid.find("div", {"id": "synopsis"}) is not None):
        syn = soupVid.find("div", {"id": "synopsis"}).find("div", {"class": "padded-panel"}).find("li").text
        row.append(syn)

    print(count)
    count += 1

movies_df = pd.DataFrame(data)
movies_df.to_csv("scenes_synopses.csv")


df = pd.read_csv("scenes_synopses.csv")
df.columns = ["Count", "Title", "Doorway", "Year", "nan1", "nan2", "Link", "Synopsis"]

df = df.drop(["Count", "nan1", "nan2"], axis=1)
print(df.head())


performers = []
count = 0
for href in df["Link"]:
    vidTxt = scrape(href)
    soupVid = BeautifulSoup(vidTxt, "html.parser")

    perfs = soupVid.find("div", {"class": "panel panel-default"}).find_all("div", {"class": "castbox"})
   
    for perf in perfs:
        perfLink = perf.find("a")
        perfUrl = root + perfLink['href']
        perfName = perfLink.text

        perfTxt = scrape(perfUrl)
        perfSoup = BeautifulSoup(perfTxt, "html.parser")
        tab = perfSoup.find("a", {"aria-controls": "perflist"})

        careerSceneNum = tab.text.split()[2][1:][:-1]

        performers.append([perfName, perfUrl, careerSceneNum])
    
    print(count)
    count += 1
    time.sleep(0.5)


perf_df = pd.DataFrame(performers)
print(perf_df.head())
perf_df.to_csv("performers.csv")