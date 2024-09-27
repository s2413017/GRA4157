import requests
from bs4 import BeautifulSoup
import pandas as pd

# INITIAL SCRAPE: We fetch the top gainers table from Yahoo Finance
result = requests.get("https://finance.yahoo.com/markets/stocks/gainers/") # Data is saved in the variable result
assert(result.status_code==200)

# PARSE: Parse the result content
soup = BeautifulSoup(result.content, "lxml")

# FIND TABLE: Find the top gainers table
table = soup.find("table")  # Find the first table on the page

# EXTRACT ROWS: Extract table rows while skipping the header row
rows = table.find_all("tr")[1:] # While inspecting the webpage we can see that all the rows start with code <tr>

# DATA CLEANUP: Scrape the data from the rows and store it in a logical list
yahoo_data = [] # Prepare a list to store the scraped data

for row in rows:
    cols = row.find_all("td")  # Extract each cell in the row
    symbol_and_company = cols[0].text.strip().split(" ")  # Symbol and company are in the same cell: We make a list of all the parts
    symbol = symbol_and_company[0]  # First part is the symbol
    company = " ".join(symbol_and_company[1:])  # All next parts are the company, so we join them together
    price = float(cols[2].text.strip().replace("+", "")) # Third part is the price: We need to remove the + sign and transform it into a float value
    yahoo_data.append({"Symbol": symbol, "Company": company, "Price": price}) # Append the extracted data in dictionary form to a list

# FUNCTION: 
def analysis(data):

    print("\nTop Gainers Data (First 5 rows):") # Display the first few rows of the data
    print(data.head()) # Function that returns first 5 rows of the DataFrame

    highest_price = data.loc[data["Price"].idxmax()] # Find the company with the highest stock price
    print("\nCompany with the highest stock price: ", highest_price["Company"], "\n") # Display the company with the highest price

# CALL FUNCTION: Run the analysis function to display table and the company with the highest price
analysis(pd.DataFrame(yahoo_data))