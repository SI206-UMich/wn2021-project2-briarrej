from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), 'r') as file:
        fileData = file.read()
    #print(fileData)
    soup = BeautifulSoup(fileData, 'html.parser')
    titles = soup.find_all('a', class_ = "bookTitle")
    titleNames = []
    for title in titles:
        titleNames.append(title.text.strip())
    authors = soup.find_all('a', class_ = "authorName")
    authorNames = []
    for author in authors:
        authorNames.append(author.text.strip())
    bookTuples = []
    for item in range(len(titles)):
        bookTuples.append((titleNames[item], authorNames[item]))
    return bookTuples


def get_search_links():
    #creating the object
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    info = requests.get(url)
    soup = BeautifulSoup(info.content, 'html.parser')
    bookNames = soup.find_all('a', class_ = 'bookTitle')
    list = []
    for title in bookNames:
        link = title.get('href')
        #print(link)
        if link.startswith('/book/show/'):
            list.append("https://www.goodreads.com" + link)
    #print(list[0])
    return list[:10]


    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    #pass


def get_book_summary(book_url):
    #creating the object
    info = requests.get(book_url)
    soup = BeautifulSoup(info.text, 'html.parser')
    #print(soup)
    try:
        title = soup.find('h1', class_ = 'gr-h1 gr-h1--serif')
        title = title.text.strip()
        #print(title)
        pages = soup.find('span', itemprop = 'numberOfPages')
        pages = int(pages.text.strip()[:3])
        #print(pages)
        author = soup.find('span', itemprop = 'name')
        author = author.text.strip()

    except:
        title = ""
        author = ""
        pages = 0
    #print(title, author, pages)
    return (title, author, pages)

    
    
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    #pass


def summarize_best_books(filepath):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as file:
        filedata = file.read()
    soup = BeautifulSoup(filedata, 'html.parser')
    category = soup.find_all('h4')
    catList = []
    for item in category:
        catList.append(item.text.strip())
    #print(catList)

    bookList = []
    bookTitles = soup.find_all('div', class_ = "category__winnerImageContainer")
    #print(bookTitles)
    for title in bookTitles:
        for name in title.find_all('img', alt = True):
            item = name['alt']
            bookList.append(item)
    #print(bookList)       
    urlList = []
    urls = soup.find_all('div', class_ = 'category clearFix')
    for url in urls:
        urlList.append(url.find('a')['href'])
    #print(urlList)
    listOfTups = []
    for item in range(len(urlList)):
        tup = (catList[item], bookList[item], urlList[item])
        listOfTups.append(tup)
    return listOfTups

    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    pass


def write_csv(data, filename):
    
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Book Title', 'Author Name'])
        for i in data:
            f.writerow(i)
    #pass


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        search = get_titles_from_search_results('search_results.htm')
        # call get_titles_from_search_results() on search_results.htm and save to a local variable

        self.assertEqual(len(search), 20)
        # check that the number of titles extracted is correct (20 titles)

        self.assertEqual(type(search), list)
        # check that the variable you saved after calling the function is a list

        for item in search:
            self.assertEqual(type(item), tuple)
        # check that each item in the list is a tuple

        self.assertEqual(search[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the first book and author tuple is correct (open search_results.htm and find it)

        self.assertEqual(search[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        # check that the last title is correct (open search_results.htm and find it)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertEqual(type(url), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertIn("https://www.goodreads.com/book/show/", url)


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
        # check that each item in the list is a tuple
        for item in summaries:
            self.assertEqual(type(item), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(item), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(item[1]), str)
            self.assertEqual(type(item[0]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(item[2]), int)
        # check that the first book in the search has 337 pages
        #print(summaries[1][2])
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summarize = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(summarize), 20)
            # assert each item in the list of best books is a tuple
        for item in summarize:
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summarize[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summarize[-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020') )

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        results = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(results, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = []
        with open('test.csv') as f:
            csvFile = csv.reader(f)
            for line in csvFile:
                csv_lines.append(line)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book Title', 'Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison'])


if __name__ == '__main__':
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



