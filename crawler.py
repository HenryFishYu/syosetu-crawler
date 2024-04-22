import argparse
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def read_input() -> (str,float):
    parser = argparse.ArgumentParser(description='Crawler for noc.syosetu.com')
    parser.add_argument('--url',required=True,help='the url of article page, for example: https://ncode.syosetu.com/n9066iw/, https://novel18.syosetu.com/n1701iw/')
    parser.add_argument('--interval',required=False,help='interval between each request in seconds')
    args = parser.parse_args()
    return args.url, float(args.interval)
def get_content_from_div(div)->str:
    return div.get_text(strip=True) if div else ""

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.1.1729474580.1699539479; over18=yes; _ga_CQ4S04X1ZS=GS1.1.1699539478.1.0.1699539480.0.0.0; ks2=qb9rxsk49p1; sasieno=0; lineheight=0; fontsize=0; fix_menu_bar=1; cto_bundle=GpHyHV9QNE8lMkZ4RTFZMFZLa2QlMkZ3WThqcGNrampEYWkwYlVtWlR1UUp5dUZQaUY5V2xKc3pHRHJlVUQwRVVlYkZkcUw4T0lmcFBWMGp3V0hUdCUyRlYwc3NKc1psc1hRckVQJTJCTlZoZGlaWmdPbHpnaW5ibCUyQktHbSUyRmxyUk9iWjIxTXglMkZqWEhFc0doRiUyQnBJd2hQVmYlMkJoeW9PMFJvUWclM0QlM0Q; novellayout=1; nlist3=1dbtr.2-17igx.0-lsne.0-18b4x.0-1c801.0-1a4rq.1e-1a6kk.2-1a6ki.0-1bakz.g-1bwg3.1-1c0p5.1-1bnvg.1-1bexw.2-15e1q.j-1a6i9.d; nlist1=1dhic.1; _pubcid=a479f2a3-b013-4913-b058-05a50003d2e5; _ga_211JY8CNFS=GS1.1.1713718028.35.1.1713718680.0.0.0; _ga_C6X74G3CHV=GS1.1.1713718681.17.0.1713718681.0.0.0; _ga_1TH9CF4FPC=GS1.1.1713718044.6.1.1713718934.0.0.0; _ga_2YQV7PZTL9=GS1.1.1713718332.1.1.1713718934.0.0.0",
    "DNT": "1",
    "Host": "",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"'
}

def main():
    url,interval_in_second = read_input()
    print("request website: "+url)
    headers["Host"] = urlparse(url).netloc
    response = requests.get(url, headers=headers)

    html_content = response.content
    print("analyze the website: " + url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    file = open(soup.find("title").text+".txt","w")
    print("the title of this article: "+soup.find("title").text)
    current_chapter = 1
    number_of_chapters = len(soup.find_all("dd"))+1
    for dd_elements in soup.find_all("dd"):
        if interval_in_second:
            print("interval: {interval_in_second} seconds".format(interval_in_second=interval_in_second))
            time.sleep(interval_in_second)
        print("collecting chapter: {current_chapter}/{number_of_chapters}".format(current_chapter=current_chapter,number_of_chapters=number_of_chapters))
        sub_href = dd_elements.find_next("a").get("href")
        response = requests.get(url+sub_href, headers=headers)
        div = BeautifulSoup(response.content, "html.parser").find("div", {"id": "novel_honbun", "class": "novel_view"})
        file.write(get_content_from_div(div))
        file.write("\n")
        current_chapter += 1
    file.close()
    print("done, target file name: " + file.name)


if __name__ == "__main__":
    main()