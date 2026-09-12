# Web Scraping and Data Analysis Project

A professional Python web scraping project that demonstrates how to collect, process, store, query, and analyze data from multiple websites.

This project scrapes:

1. Books from **Books to Scrape**
2. Distinct quote authors from **Quotes to Scrape**
3. A randomly selected article from **Wikipedia**

The project uses **Python**, **Requests**, **BeautifulSoup**, **Pandas**, and **LXML** to demonstrate practical web scraping and beginner-friendly data analysis techniques.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Objectives](#project-objectives)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Features](#features)
- [Data Sources](#data-sources)
- [Books Scraper](#books-scraper)
- [Quotes Scraper](#quotes-scraper)
- [Wikipedia Scraper](#wikipedia-scraper)
- [Installation](#installation)
- [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
- [Installing Dependencies](#installing-dependencies)
- [Running the Scraper](#running-the-scraper)
- [Scraped Output](#scraped-output)
- [Querying the Scraped Data](#querying-the-scraped-data)
- [Book Queries](#book-queries)
- [Quote Author Queries](#quote-author-queries)
- [Wikipedia Queries](#wikipedia-queries)
- [Interactive Query System](#interactive-query-system)
- [How the Scraper Works](#how-the-scraper-works)
- [Web Scraping Concepts Demonstrated](#web-scraping-concepts-demonstrated)
- [Data Processing](#data-processing)
- [Error Handling](#error-handling)
- [Responsible Scraping](#responsible-scraping)
- [Possible Improvements](#possible-improvements)
- [Learning Outcomes](#learning-outcomes)
- [Future Development](#future-development)
- [Author](#author)
- [License](#license)

---

## Project Overview

This project demonstrates the complete workflow of a practical web scraping application.

The application sends HTTP requests to publicly available scraping-practice websites, downloads their HTML content, parses the HTML using BeautifulSoup, extracts useful information, and stores the results in CSV files using Pandas. It also demonstrates how scraped data can be queried and analyzed after collection.

**Overall workflow:**

`Website` → `HTTP Request` → `HTML Response` → `BeautifulSoup` → `Data Extraction` → `Data Cleaning` → `Pandas DataFrame` → `CSV Files` → `Data Querying and Analysis`

---

## Project Objectives

The main objectives of this project are to:

- Learn the fundamentals of web scraping with Python
- Extract structured information from HTML pages
- Work with multiple pages through pagination
- Follow links from listing pages to detail pages
- Extract information from individual product pages
- Remove duplicate quote authors
- Scrape author profile information
- Work with redirected URLs
- Scrape a random Wikipedia article
- Store scraped data in CSV files
- Load scraped data using Pandas
- Query and filter datasets
- Perform basic data analysis
- Build reusable scraping functions
- Practice writing clean and maintainable Python code

---

## Technologies Used

### Python

Python is the primary programming language used to build the scraper. It provides a large ecosystem of libraries for:

- Web scraping
- Data analysis
- Automation
- Machine learning
- Data visualization

### Requests

Used to send HTTP requests to websites and retrieve their HTML content.

```python
response = requests.get(url)
```

The response contains the HTML document returned by the website.

### BeautifulSoup

Used to parse HTML and extract information from web pages.

```python
soup = BeautifulSoup(response.text, "lxml")
```

It allows the program to search for:

- Tags
- Classes
- IDs
- Links
- Tables
- Text
- Other HTML elements

### LXML

Used as the HTML parser for BeautifulSoup, providing fast and reliable HTML parsing.

```python
BeautifulSoup(response.text, "lxml")
```

### Pandas

Used to store, manipulate, query, and analyze the scraped data.

```python
df = pd.read_csv("output/books.csv")
```

Pandas makes it possible to perform operations such as:

- Filtering
- Searching
- Sorting
- Counting
- Aggregation
- Statistical analysis

---

## Project Structure

```text
WebScrapingProject/
│
├── .ScrapeEnv/
├── scraper.py
├── data_query.py
├── requirements.txt
├── README.md
└── output/
    ├── books.csv
    ├── quote_authors.csv
    └── wikipedia_random_page.csv
```

---

## Features

The project contains three major scraping components.

### 1. Books Scraper

Collects books from the first five pages of Books to Scrape. Each page contains 20 books, therefore: **5 pages × 20 books = 100 books**.

The scraper collects:

- Book name
- Price
- Stock status
- Rating
- Description
- Category
- Product information
- Product URL

### 2. Quotes Scraper

Collects distinct quote authors. The program is configured to collect 15 unique authors, which satisfies the requirement of collecting between 10 and 20 distinct authors.

The scraper collects:

- Author name
- Nationality/birth-location information
- Date of birth
- Author description
- Author profile URL

### 3. Wikipedia Random Page Scraper

Uses Wikipedia's random-page endpoint. The program:

1. Requests a random Wikipedia page
2. Follows the redirect
3. Identifies the selected article
4. Extracts the article title
5. Extracts available article paragraphs
6. Saves the result to a CSV file

---

## Data Sources

The project uses scraping-practice and public web resources.

| Source | Description | URL |
|---|---|---|
| **Books to Scrape** | Fictional bookstore built for practicing web scraping | https://books.toscrape.com/ |
| **Quotes to Scrape** | Practice site with quotes, authors, tags, pagination, and author profile pages | https://quotes.toscrape.com/ |
| **Wikipedia** | Used for the random-page scraping component | https://en.wikipedia.org/wiki/Special:Random |

---

## Books Scraper

The Books scraper starts from the main Books to Scrape website and processes five pages.

**Pagination workflow:** `Page 1` → `Page 2` → `Page 3` → `Page 4` → `Page 5`

Each page contains approximately 20 books, so the expected result is approximately **100 books**.

### Book Data Collected

For every book, the scraper collects:

| Field | Description | Example |
|---|---|---|
| Book Name | The title of the book | *A Light in the Attic* |
| Price | The displayed price of the book | £51.77 |
| Stock Status | Simplified availability status | `In stock` / `Out of stock` |
| Rating | Numeric rating converted from a CSS class | One → 1, Two → 2, Three → 3, Four → 4, Five → 5 |
| Description | Extracted from the individual product page | — |
| Category | Extracted from the breadcrumb navigation | Poetry, Fiction, Fantasy, Mystery, Romance, Historical Fiction |
| Product Information | Dynamically extracted from the product-information table | UPC, Product Type, Price (excl./incl. tax), Tax, Availability, Number of reviews |

Instead of hard-coding every field, the scraper loops through the product-information table and extracts its key-value pairs, which makes it more flexible.

---

## Quotes Scraper

The quote scraper begins from the Quotes to Scrape pagination system and continues through quote pages until it finds the required number of unique authors.

```python
number_of_authors = 15
```

This provides a result within the requested range of 10–20 authors.

### Removing Duplicate Authors

A dictionary is used to prevent duplicate authors from being scraped repeatedly:

```python
authors = {}

if author_name not in authors:
    authors[author_name] = author_url
```

If an author appears multiple times (e.g. `Albert Einstein`, `Albert Einstein`, `Albert Einstein`), the scraper stores the author only once — reducing unnecessary requests.

### Author Profile Scraping

After collecting unique author names and profile URLs, the scraper follows each author profile and extracts:

- Name
- Nationality/birth location
- Date of birth
- Description
- Profile URL

This demonstrates a common web scraping technique known as **Follow Detail Links**:

`Quote Page` → `Author Name` → `Author Profile URL` → `Author Profile` → `Author Information`

---

## Wikipedia Scraper

The Wikipedia component uses the random-page endpoint:

```text
https://en.wikipedia.org/wiki/Special:Random
```

This redirects to a randomly selected Wikipedia article. The scraper captures the final URL:

```python
final_url = response.url
```

It then extracts:

- Article title
- Article URL
- Article paragraphs

The result is stored in `output/wikipedia_random_page.csv`.

---

## Installation

### Step 1: Clone or Download the Project

If the project is hosted on GitHub, clone it using:

```bash
git clone https://github.com/AirchildDev/WebScraping-Project
cd WebScraping_Project
```

If you created the project manually, simply navigate to the folder.

## Setting Up the Virtual Environment

Creating a virtual environment prevents the project's dependencies from interfering with other Python projects.

```powershell
python -m venv .ScrapeEnv
.ScrapeEnv\Scripts\Activate.ps1
```

After activation, the terminal should display:

```text
(.ScrapeEnv) PS C:\Users\YourName\OneDrive\Desktop\WebScrapingProject>
```

## Installing Dependencies

Install all dependencies using:

```bash
pip install -r requirements.txt
```

The required packages are:

- requests
- beautifulsoup4
- pandas
- lxml

You can also install them directly:

```bash
pip install requests beautifulsoup4 pandas lxml
```

## Running the Scraper

Make sure the virtual environment is active, then run:

```bash
python scraper.py
```

The program will execute the three scraping processes.

### Expected Execution Flow

```text
============================================================
WEB SCRAPING PROJECT
============================================================

Scraping Books page 1
Scraping Books page 2
Scraping Books page 3
Scraping Books page 4
Scraping Books page 5

Saved 100 books.

Scraping Quotes page 1
Scraping author: ...
Scraping author: ...
Scraping author: ...

Saved 15 authors.

Selecting random Wikipedia page...

Saved random Wikipedia page.

============================================================
SCRAPING COMPLETE
============================================================
```

The exact book names and Wikipedia article will vary.

---

## Scraped Output

After successful execution, the output folder should contain:

```text
output/
├── books.csv
├── quote_authors.csv
└── wikipedia_random_page.csv
```

| File | Fields |
|---|---|
| **books.csv** | `book_name`, `price`, `stock_status`, `rating`, `description`, `category`, `product_information`, `product_url` |
| **quote_authors.csv** | `name`, `nationality`, `date_of_birth`, `description`, `profile_url` |
| **wikipedia_random_page.csv** | `title`, `url`, `content` |

---

## Querying the Scraped Data

Scraping and querying are two different stages:

- **Scraping** means: `Website` → `Collect Data`
- **Querying** means: `Stored Data` → `Search / Filter / Analyze`

The scraper collects the information; Pandas is then used to query the resulting CSV files.

## Book Queries

Create or use `data_query.py` and load the books:

```python
import pandas as pd

books = pd.read_csv("output/books.csv")
```

**Basic inspection:**

```python
print(books.head())            # first five books
print(books.head(10))          # first ten books
print(books.tail())            # last five books
print(len(books))              # 100
print(books.shape)             # (100, 8) -> 100 rows, 8 columns
print(books.columns.tolist())  # column names
```

**Select columns:**

```python
print(books["book_name"])
print(books[["book_name", "price"]])
```

**Filter by stock status:**

```python
in_stock = books[books["stock_status"] == "In stock"]
print(in_stock[["book_name", "price", "category"]])
```

**Filter by rating:**

```python
five_star = books[books["rating"] == 5]
print(five_star[["book_name", "rating", "price", "category"]])

high_rated = books[books["rating"] >= 4]
print(high_rated[["book_name", "rating", "price"]])
```

**Filter by category:**

```python
poetry = books[books["category"] == "Poetry"]
print(poetry)

fiction = books[books["category"] == "Fiction"]
print(fiction)

print(books["category"].unique())        # list all categories
print(books["category"].value_counts())  # count books per category
```

**Search for a book (case-insensitive):**

```python
result = books[
    books["book_name"].str.contains("love", case=False, na=False)
]
print(result)
```

This matches `love`, `Love`, and `LOVE` alike.

**Convert prices to numbers:**

The scraped price contains the pound symbol (e.g. `£51.77`). For calculations, convert it to a float:

```python
books["price_numeric"] = (
    books["price"].str.replace("£", "", regex=False).astype(float)
)
```

**Price-based queries:**

```python
expensive = books[books["price_numeric"] > 50]
print(expensive[["book_name", "price"]])

cheap = books[books["price_numeric"] < 30]
print(cheap[["book_name", "price"]])

most_expensive = books.loc[books["price_numeric"].idxmax()]
print(most_expensive)

cheapest = books.loc[books["price_numeric"].idxmin()]
print(cheapest)

average_price = books["price_numeric"].mean()
print(f"Average price: £{average_price:.2f}")

print(books["price_numeric"].max())
print(books["price_numeric"].min())
```

## Quote Author Queries

```python
authors = pd.read_csv("output/quote_authors.csv")

print(authors.head())
print(len(authors))
print(authors["name"])
print(authors[["name", "nationality"]])
```

**Search for an author:**

```python
result = authors[
    authors["name"].str.contains("Einstein", case=False, na=False)
]
print(result)
```

## Wikipedia Queries

```python
wikipedia = pd.read_csv("output/wikipedia_random_page.csv")

print(wikipedia.loc[0, "title"])
print(wikipedia.loc[0, "url"])
print(wikipedia.loc[0, "content"])
```

## Interactive Query System

The project can also provide an interactive command-line interface:

```bash
python data_query.py
```

```text
==============================
BOOK DATABASE
==============================

1. Show first 10 books
2. Show 5-star books
3. Show books in stock
4. Show categories
5. Search book
6. Show most expensive book
7. Show cheapest book
8. Show average price
9. Exit
```

This turns the scraped CSV dataset into a basic command-line database application.

---

## How the Scraper Works

The scraper follows a reusable architecture:

`HTTP Request` → `HTML Page` → `BeautifulSoup` → (`Books`, `Quotes`, `Wikipedia`) → (`Details`, `Authors`, `Article`) → `Pandas` → `CSV`

### Reusable HTTP Function

The scraper contains a reusable function:

```python
def get_soup(url):
    ...
```

This function:

1. Sends the HTTP request
2. Checks for HTTP errors
3. Parses the returned HTML
4. Returns a BeautifulSoup object

This avoids repeating the same request and parsing code throughout the project.

### HTTP Request

```python
response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
```

The website responds with HTML.

### HTTP Status Checking

```python
response.raise_for_status()
```

This detects unsuccessful HTTP responses instead of silently processing invalid pages.

### HTML Parsing

```python
BeautifulSoup(response.text, "lxml")
```

This converts raw HTML into a searchable document.

### CSS Selectors

BeautifulSoup supports CSS selectors:

```python
soup.select_one(".price_color")           # selects an element with class "price_color"
soup.select("article.product_pod h3 a")   # finds book links within the product listing
```

### Pagination

```python
for page_number in range(1, pages + 1):
    ...
```

With `pages = 5`, the program processes pages `1` → `2` → `3` → `4` → `5`.

### Following Detail Links

The Books listing page does not contain every piece of information required. The scraper first obtains the product URL:

```python
book_url = urljoin(url, link.get("href"))
```

Then requests the individual book page — known as **detail-page scraping**.

### Dynamic Product Information

Instead of manually coding every product-information field, the scraper loops through the table (`HTML Table` → `Key → Value` pairs), producing a dictionary such as:

```json
{
    "UPC": "...",
    "Product Type": "Books",
    "Price (excl. tax)": "...",
    "Price (incl. tax)": "...",
    "Tax": "...",
    "Availability": "...",
    "Number of reviews": "..."
}
```

This approach makes the scraper more flexible.

### Duplicate Handling

The Quotes scraper uses a dictionary to prevent duplicate authors:

```python
authors = {}

if author_name not in authors:
    authors[author_name] = author_url
```

This prevents the program from unnecessarily scraping the same author profile multiple times.

### URL Joining

Websites often provide relative URLs (e.g. `../book/example/index.html`). The scraper uses `urljoin()` to convert relative links into complete URLs — safer than manually concatenating strings.

### Request Timeout

```python
TIMEOUT = 15
```

This prevents the program from waiting indefinitely if a website does not respond.

### User-Agent

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 ..."
}
```

This identifies the request as coming from a browser-like client.

### Request Delay

```python
time.sleep(0.2)
```

A small delay between requests reduces load on the server — a useful practice when building responsible scrapers.

---

## Error Handling

```python
try:
    ...
except requests.RequestException as error:
    ...
```

This allows the program to handle request-related problems without necessarily terminating the entire scraping process. For example, if one book page fails, the scraper can report the failure and continue.

## Data Processing

The scraper cleans extracted text using:

```python
get_text(" ", strip=True)
```

This removes unnecessary whitespace and produces cleaner data — for example, turning messy HTML text into a clean string like `In stock (22 available)` instead of retaining unnecessary line breaks and spaces.

---

## Responsible Scraping

This project is designed for educational purposes and uses scraping-practice resources. When scraping websites in real-world projects, always consider:

- The website's Terms of Service
- `robots.txt`
- Rate limits
- Copyright restrictions
- Privacy requirements
- Server load
- API availability
- Whether automated access is permitted

Do not use scraping techniques to bypass authentication, access private information, defeat security controls, or overwhelm websites with requests. Whenever an official API is available and appropriate, consider using it instead of scraping HTML.

---

## Possible Improvements

The project can be extended significantly.

### 1. Retry Failed Requests

Implement automatic retries for temporary network failures.

**Strategy:** `Request` → `Failed?` → (Yes → `Wait` → `Retry`) / (No → `Continue`)

### 2. Logging

Replace simple `print()` statements with Python's `logging` module to record:

- Successful requests
- Failed requests
- Errors
- Scraping progress
- Runtime information

### 3. Command-Line Arguments

The scraper could accept parameters such as:

```bash
python scraper.py --pages 10
python scraper.py --authors 20
```

This would make the application more configurable.

### 4. Database Storage

Instead of CSV files, the data could be stored in SQLite, PostgreSQL, or MySQL.

**Possible architecture:** `Websites` → `Python Scraper` → `Data Cleaning` → `PostgreSQL` → `SQL Queries`

### 5. Data Visualization

Pandas and Matplotlib could be used to visualize the scraped data:

- Books by category
- Rating distribution
- Price distribution
- Average price by category
- Number of books by stock status

### 6. Web Dashboard

The scraped data could be displayed through Django, Flask, or Streamlit — a future version could provide a browser-based interface for searching books and authors.

### 7. Automated Scheduling

**Flow:** `Every day` → `Run scraper` → `Update dataset` → `Analyze changes`

### 8. Export to Excel

```python
books.to_excel("books.xlsx", index=False)
```

### 9. Data Cleaning Pipeline

A more advanced version could introduce a dedicated data-cleaning stage:

`Scraping` → `Raw Data` → `Cleaning` → `Validation` → `Transformation` → `Storage`

---

## Learning Outcomes

After completing this project, a learner should understand the fundamentals of:

- Python web scraping
- HTTP requests
- HTML
- CSS selectors
- BeautifulSoup
- Requests
- LXML
- Pagination
- URL handling
- Detail-page scraping
- Duplicate removal
- Data extraction
- Data cleaning
- CSV storage
- Pandas
- Data filtering
- Data searching
- Data aggregation
- Basic data analysis
- Error handling
- Responsible web scraping

---

## Web Scraping Concepts Demonstrated

This project demonstrates several important scraping patterns.

| Pattern | Flow |
|---|---|
| **1. Basic Page Scraping** | `URL` → `Request` → `HTML` → `Parse` → `Extract` |
| **2. Pagination** | `Page 1` → `Page 2` → `Page 3` → `Page 4` → `Page 5` |
| **3. Detail Pages** | `Listing Page` → `Product Link` → `Product Page` → `Detailed Information` |
| **4. Deduplication** | `Author, Author, Author, Author` → `Unique Author` |
| **5. Random Page** | `Random Endpoint` → `Redirect` → `Selected Page` → `Extract Content` |

### Full Project Workflow

`START` → `Install Python` → `Create Virtual Environment` → `Install Dependencies` → `Run scraper.py` → (`Books` / `Quotes` / `Wikipedia`) → (`100 books` / `15 authors` / `1 random article`) → `CSV Files` → `Pandas Loading` → `Data Querying` → `Data Analysis` → `END`

---

## Running the Complete Project

| Step | Action | Command |
|---|---|---|
| 1 | Open PowerShell | — |
| 2 | Navigate to the project | `cd "$HOME\OneDrive\Desktop\WebScrapingProject"` |
| 3 | Activate the virtual environment | `.ScrapeEnv\Scripts\Activate.ps1` |
| 4 | Install dependencies | `pip install -r requirements.txt` |
| 5 | Run the scraper | `python scraper.py` |
| 6 | Check the output | `dir output` |
| 7 | Query the data | `python data_query.py` |

---

## Troubleshooting

**Python is not recognized**

```bash
python --version
```

If Python is installed but the command is unavailable, verify that Python is correctly installed and available through PATH.

**Virtual environment does not activate**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.ScrapeEnv\Scripts\Activate.ps1
```

**ModuleNotFoundError**

```text
ModuleNotFoundError: No module named 'bs4'
```

Install the missing package:

```bash
pip install beautifulsoup4
# or reinstall everything:
pip install -r requirements.txt
```

**CSV file not found**

Make sure the scraper has been executed first, then verify the output:

```bash
python scraper.py
dir output
```

**Website request error** — check:

- Internet connection
- Website availability
- URL
- HTTP response status
- Timeout settings

---

## Requirements

The project requires:

- Python 3.x
- requests
- beautifulsoup4
- pandas
- lxml

---

## Author

**Ekeoma Chidiebere Onuoha**
Python Developer | Web Developer | AI & Machine Learning Student
GitHub: [https://github.com/AirchildDev](https://github.com/AirchildDev)

---

## License

This project is intended primarily for educational and portfolio purposes. The scraping targets used in this project are selected for learning and demonstration purposes. When adapting the project to other websites, review the relevant website policies, terms of service, `robots.txt` rules, and applicable laws before scraping.

---

## Conclusion

This project demonstrates the complete lifecycle of a beginner-to-intermediate web scraping application. It starts by retrieving web pages with Python Requests, parses HTML using BeautifulSoup, extracts structured information, follows product and author links, handles pagination and duplicate data, retrieves a random Wikipedia article, and finally stores the collected information in CSV files. The resulting datasets can then be loaded into Pandas and queried using filtering, searching, sorting, counting, and statistical operations.

The project therefore goes beyond simple web scraping — it demonstrates the complete workflow:

`SCRAPE` → `EXTRACT` → `CLEAN` → `STORE` → `QUERY` → `ANALYZE` → `VISUALIZE` → `BUILD APPLICATIONS`
