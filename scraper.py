import random
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


# ============================================================
# SETTINGS
# ============================================================

BOOKS_URL = "https://books.toscrape.com/"
QUOTES_URL = "https://quotes.toscrape.com/"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    )
}

TIMEOUT = 15


# ============================================================
# COMMON HTTP FUNCTION
# ============================================================

def get_soup(url):
    """
    Download a webpage and return a BeautifulSoup object.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT
    )

    response.raise_for_status()

    return BeautifulSoup(response.text, "lxml")


# ============================================================
# 1. BOOKS TO SCRAPE
# ============================================================

def scrape_book_details(book_url):
    """
    Scrape detailed information from one book page.
    """

    soup = get_soup(book_url)

    # Book title
    title = soup.find("h1").get_text(strip=True)

    # Price
    price = soup.select_one(".price_color").get_text(strip=True)

    # Stock status
    stock = soup.select_one(".availability").get_text(" ", strip=True)

    if "In stock" in stock:
        stock_status = "In stock"
    else:
        stock_status = "Out of stock"

    # Rating
    rating_element = soup.select_one(
        "p.star-rating"
    )

    rating = "Unknown"

    if rating_element:
        rating_classes = rating_element.get("class", [])

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        for class_name in rating_classes:
            if class_name in rating_map:
                rating = rating_map[class_name]
                break

    # Description
    description = ""

    description_heading = soup.find(
        "div",
        id="product_description"
    )

    if description_heading:
        description_element = description_heading.find_next(
            "p"
        )

        if description_element:
            description = description_element.get_text(
                " ",
                strip=True
            )

    # Product information
    product_info = {}

    table = soup.select_one("table.table.table-striped")

    if table:

        for row in table.select("tr"):

            cells = row.find_all("td")

            if len(cells) == 2:

                key = cells[0].get_text(
                    " ",
                    strip=True
                )

                value = cells[1].get_text(
                    " ",
                    strip=True
                )

                product_info[key] = value

    # Category
    category = "Unknown"

    breadcrumbs = soup.select(
        "ul.breadcrumb li"
    )

    if len(breadcrumbs) >= 3:
        category = breadcrumbs[2].get_text(
            " ",
            strip=True
        )

    return {
        "book_name": title,
        "price": price,
        "stock_status": stock_status,
        "rating": rating,
        "description": description,
        "category": category,
        "product_information": product_info,
        "product_url": book_url
    }


def scrape_books(pages=5):
    """
    Scrape books from the first N pages.
    """

    books = []

    for page_number in range(1, pages + 1):

        if page_number == 1:
            url = BOOKS_URL
        else:
            url = urljoin(
                BOOKS_URL,
                f"catalogue/page-{page_number}.html"
            )

        print(
            f"Scraping Books page {page_number}: {url}"
        )

        soup = get_soup(url)

        book_links = soup.select(
            "article.product_pod h3 a"
        )

        for link in book_links:

            book_url = urljoin(
                url,
                link.get("href")
            )

            try:

                book = scrape_book_details(
                    book_url
                )

                books.append(book)

                print(
                    f"  ✓ {book['book_name']}"
                )

            except requests.RequestException as error:

                print(
                    f"  ✗ Failed: {error}"
                )

            # Small delay between requests
            time.sleep(0.2)

    return books


# ============================================================
# 2. QUOTES TO SCRAPE
# ============================================================

def scrape_quote_authors(number_of_authors=15):
    """
    Scrape distinct quote authors.

    The quote pages contain links to author profile pages.
    We follow those profile pages to obtain additional data.
    """

    authors = {}

    page_number = 1

    while len(authors) < number_of_authors:

        url = (
            f"{QUOTES_URL}page/{page_number}/"
        )

        print(
            f"Scraping Quotes page {page_number}"
        )

        soup = get_soup(url)

        quote_blocks = soup.select(
            "div.quote"
        )

        if not quote_blocks:
            break

        for quote in quote_blocks:

            author_element = quote.select_one(
                "small.author"
            )

            if not author_element:
                continue

            author_name = author_element.get_text(
                strip=True
            )

            author_link = quote.select_one(
                "a"
            )

            if not author_link:
                continue

            author_url = urljoin(
                url,
                author_link.get("href")
            )

            if author_name not in authors:

                authors[author_name] = author_url

            if len(authors) >= number_of_authors:
                break

        page_number += 1

    results = []

    for author_name, author_url in authors.items():

        print(
            f"Scraping author: {author_name}"
        )

        soup = get_soup(author_url)

        nationality = "Unknown"
        date_of_birth = "Unknown"
        description = ""

        # Author nationality
        nationality_element = soup.select_one(
            ".author-born-location"
        )

        if nationality_element:

            nationality = nationality_element.get_text(
                " ",
                strip=True
            )

        # Date of birth
        birth_element = soup.select_one(
            ".author-born-date"
        )

        if birth_element:

            date_of_birth = birth_element.get_text(
                " ",
                strip=True
            )

        # Description
        description_element = soup.select_one(
            ".author-description"
        )

        if description_element:

            description = description_element.get_text(
                " ",
                strip=True
            )

        results.append({
            "name": author_name,
            "nationality": nationality,
            "date_of_birth": date_of_birth,
            "description": description,
            "profile_url": author_url
        })

        time.sleep(0.2)

    return results


# ============================================================
# 3. RANDOM WIKIPEDIA PAGE
# ============================================================

def scrape_random_wikipedia():

    print(
        "\nSelecting random Wikipedia page..."
    )

    response = requests.get(
        WIKIPEDIA_URL,
        headers=HEADERS,
        timeout=TIMEOUT,
        allow_redirects=True
    )

    response.raise_for_status()

    final_url = response.url

    soup = BeautifulSoup(
        response.text,
        "lxml"
    )

    # Page title
    title_element = soup.select_one(
        "#firstHeading"
    )

    title = (
        title_element.get_text(strip=True)
        if title_element
        else "Unknown"
    )

    # Extract paragraphs
    paragraphs = soup.select(
        "div.mw-parser-output > p"
    )

    text = []

    for paragraph in paragraphs:

        paragraph_text = paragraph.get_text(
            " ",
            strip=True
        )

        if paragraph_text:
            text.append(paragraph_text)

    content = "\n".join(text)

    return {
        "title": title,
        "url": final_url,
        "content": content
    }


# ============================================================
# SAVE DATA
# ============================================================

def save_books(books):

    df = pd.DataFrame(books)

    # Convert dictionary to readable text
    df["product_information"] = df[
        "product_information"
    ].apply(str)

    df.to_csv(
        "output/books.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"\nSaved {len(df)} books."
    )


def save_authors(authors):

    df = pd.DataFrame(authors)

    df.to_csv(
        "output/quote_authors.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Saved {len(df)} authors."
    )


def save_wikipedia(page):

    df = pd.DataFrame([page])

    df.to_csv(
        "output/wikipedia_random_page.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "Saved random Wikipedia page."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("WEB SCRAPING PROJECT")
    print("=" * 60)

    # --------------------------------------------------------
    # BOOKS
    # --------------------------------------------------------

    books = scrape_books(
        pages=5
    )

    save_books(books)

    # --------------------------------------------------------
    # QUOTE AUTHORS
    # --------------------------------------------------------

    authors = scrape_quote_authors(
        number_of_authors=15
    )

    save_authors(authors)

    # --------------------------------------------------------
    # RANDOM WIKIPEDIA
    # --------------------------------------------------------

    wikipedia_page = scrape_random_wikipedia()

    save_wikipedia(
        wikipedia_page
    )

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()