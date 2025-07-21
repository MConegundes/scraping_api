import requests
from bs4 import BeautifulSoup as BfS4
import pandas as pd

url = 'https://books.toscrape.com/'

response = requests.get(url)
if response.ok:
    # create a list for all links of the categories:
    links_of_categories_all = []
    soup = BfS4(response.content, "html.parser")
    # take information for the sidebar: categories
    categories = soup.select(".side_categories a")
    for category in categories:
        href = category["href"]
        link = f"http://books.toscrape.com/{href}"
        # create one link of each book:
        links_of_categories_all.append(link)

        # start from the second link, start with Travel:
        if not href == "catalogue/category/books_1/index.html":
            response = requests.get(link)
            if response.ok:
                soup = BfS4(response.content, "html.parser")
                # check if for a next page, take the info: page 1 of 2:
                next_page = soup.findAll('ul', class_='pager')
                if next_page:
                    for page in next_page:
                        all_num_page = page.find("li", class_="current").text
                        # get the last number of info, to know how many pages will be there:
                        num_page = int(all_num_page.strip()[10:])

                        counter = 2
                        while num_page > 1:
                            link_next_page = f"{link.replace('index.html', '')}page-{counter}.html"
                            links_of_categories_all.append(link_next_page)
                            num_page -= 1
                            counter += 1

    # start from the second link in the list:
    links_of_categories = links_of_categories_all[1:]

books_scraped = []
books_in_category = []
for link in links_of_categories:
    book_url = link.strip()
    response = requests.get(book_url)
    if response.ok:
        soup = BfS4(response.content, "html.parser")
        soup_2 = BfS4(response.text, 'html.parser')
        # find all <article class="product_pod">:
        articles = soup.find_all("article", class_="product_pod")
        category = soup.title.text.strip().replace(" | \n     Books to Scrape - Sandbox", "")
        for article in articles:
            a = article.find("a")
            a_link = a["href"]
            book_link = f'http://books.toscrape.com/catalogue/{a_link.replace("../../../", "")}'
            # create link of each book:
            books_in_category.append(book_link)
            
            response = requests.get(book_link)
            if response.ok:
                soup = BfS4(response.content, "html.parser")
                image = soup.find("img")
                image_url = image["src"].replace("../../", "http://books.toscrape.com/")  # Changing relative urls to absolute
                title = image["alt"]
                price = soup.find('p', class_='price_color').text
                availability = soup.find("th", text="Availability").find_next_sibling("td").string.strip()
                rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
                
                books_scraped.append({
                    "Title": title,
                    "Price": price,
                    "Category": category,
                    "Availability": availability,
                    "Rating": rating,
                    "Image URL": image_url,
                    "Link": book_link
                })

books_df = pd.DataFrame(books_scraped)
books_df.to_csv('books_data.csv', index_label='index') 
