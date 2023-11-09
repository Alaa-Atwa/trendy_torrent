from bs4 import BeautifulSoup
import requests
from itertools import zip_longest
import csv
import subprocess

trends_names = []
links = []
torrent_sizes = []

url = "https://1337x.to/trending"
response = requests.get(url)

# creating soup
soup = BeautifulSoup(response.content, "html.parser")
trends = soup.find_all("td", {"class":"coll-1 name"})

# extracting titles and links
for trend in trends:
    trends_names.append(trend.find("a").getText())
    link = "https://1337x.to" + trend.find("a").attrs["href"]
    links.append(link)

# extract file sizes
sizes = soup.find_all("td", {"class":"coll-4 size mob-uploader"})
for size in sizes:
    clear_size = size.text.strip().split('B')[0]+"B"
    torrent_sizes.append(clear_size)

# unpacking
file_list = [trends_names, torrent_sizes, links]
exported = zip_longest(*file_list)

# saving to a csv file
with open("trending.csv", "w", newline='') as file:
    wr = csv.writer(file, delimiter="\t")
    wr.writerow(["title", "torrent_size", "link"])
    wr.writerows(exported)
    file.close()

subprocess.call(("open", "trending.csv"))
