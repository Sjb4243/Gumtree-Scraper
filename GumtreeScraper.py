from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests

print("What do you want to search for?")
search_item = input(">").replace(" ", "%20")
print("What is your postcode?")
search_location = input(">")
URL = f"https://www.gumtree.com/search?search_category=all&q={search_item}&search_location={search_location}"

page = requests.get(URL)
parse = BeautifulSoup(page.content, "html.parser")
results = parse.find(id = "srp-results")

try:
    page.raise_for_status()  # Ensure the request didn't fail
except HTTPError:
    print("Gumtree has blocked the client from searching for a bit")
    exit(0)  # Quit the program

no_results = results.find_all("h2", class_ = "space-mbn txt-normal")
for item in no_results:
    if item.text.startswith("Sorry"):
        print("No results found")
        break

all_results = results.find_all("article", class_ = "listing-maxi")
all_hrefs = results.find_all("a")

for element, link in zip(all_results, all_hrefs):
    post_title = element.find("h2", class_="listing-title")
    post_location = element.find("span", class_="truncate-line")

    if post_title and post_location:  # Only do it if both are not None (implicitly checked)
        post_location_modified = post_location.text.replace("\n", "")
        char_removal = post_location_modified.index("|") + 1
        print(post_title.text.strip("\n"))
        print(f"Post location: {post_location_modified[char_removal:]}")
        print(f"URL: https://www.gumtree.com{link.get('href')}")
        print("__________________________________________________________________")
