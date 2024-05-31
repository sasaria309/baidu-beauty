# baidu_beauty_scraper.py
import requests
from bs4 import BeautifulSoup
import csv

def scrape_baidu(query, num_results):
    search_url = f"https://www.baidu.com/s?wd={query}&rn={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for result_item in soup.find_all('div', class_='result'):
        title = result_item.find('h3').get_text()
        description = result_item.find('div', class_='c-abstract')
        description = description.get_text() if description else "No description"
        link = result_item.find('a')['href']
        results.append({'title': title, 'description': description, 'link': link})

    return results

def save_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Description', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def main():
    query = "美白"
    num_results = 10
    results = scrape_baidu(query, num_results)
    save_to_csv(results, 'baidu_beauty_results.csv')
    print(f"Saved {len(results)} results to baidu_beauty_results.csv")

if __name__ == "__main__":
    main()
