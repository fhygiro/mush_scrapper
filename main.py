import requests
from bs4 import BeautifulSoup as BS
import time
import json


def main():
    site_url = "https://amanita.club"
    url = "https://amanita.club/#products"
    req = requests.get(url)
    src = req.text

    current_but = []
    link_list = []

    soup = BS(src, "lxml")
    button_list = soup.find_all(class_="button-2")

    for button in button_list:
        span = button.find("span")
        if span.text.strip() == "Подробнее":
            current_but.append(button)

    for button in current_but:
        link = button.find("a").get("href")
        link_list.append(link)

    data_list = []

    for link in link_list:
        url = site_url + link
        req = requests.get(url)
        src = req.text
        soup = BS(src, "lxml")

        name = soup.find(class_="e_261344").find("h1").text.strip()

        if "Подарочный сертификат" in name:
            continue

        description = soup.find(class_="e_357396").text.strip().replace("\n", "").replace("\r", "").replace("\t", "")
        all_span = soup.find(class_="e_132652").find_all("span")
        price = ""

        for span in all_span:
            if "Купить" in span.text:
                continue
            else:
                price = span.text.strip()

        print(url + " is done")

        data = {
            "name": name,
            "description": description,
            "price": price
        }

        data_list.append(data)

        time.sleep(0)

    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data_list, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()