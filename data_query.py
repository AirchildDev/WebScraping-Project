import pandas as pd


# Load scraped books
books = pd.read_csv("output/books.csv")

# Load scraped quote authors
authors = pd.read_csv("output/quote_authors.csv")

# Load Wikipedia page
wikipedia = pd.read_csv(
    "output/wikipedia_random_page.csv"
)


# BOOK QUERIES

print("\nBOOK DATA")
print("=" * 50)

# Display first 5 books
print(books.head())


# Number of books
print("\nTotal books:")
print(len(books))


# Show all columns
print("\nColumns:")
print(books.columns.tolist())


# Books that are in stock
print("\nBooks in stock:")
print(
    books[
        books["stock_status"] == "In stock"
    ][
        ["book_name", "price", "category"]
    ]
)


# Books with 5-star rating
print("\n5-star books:")
print(
    books[
        books["rating"] == 5
    ][
        ["book_name", "price", "category"]
    ]
)


# Books belonging to Poetry
print("\nPoetry books:")
print(
    books[
        books["category"] == "Poetry"
    ][
        ["book_name", "price"]
    ]
)


# AUTHOR QUERIES

print("\n\nAUTHOR DATA")
print("=" * 50)

print(authors.head())

print("\nTotal authors:")
print(len(authors))

print("\nAuthor names:")
print(authors["name"].tolist())


# WIKIPEDIA QUERY

print("\n\nWIKIPEDIA DATA")
print("=" * 50)

print(
    "Title:",
    wikipedia.loc[0, "title"]
)

print(
    "URL:",
    wikipedia.loc[0, "url"]
)