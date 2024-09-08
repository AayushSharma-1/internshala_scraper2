# Internshala Internship Scraper

This application scrapes internship listings from Internshala based on user-selected categories. It extracts key information such as the title, company name, location, duration, and stipend for each internship and displays the data in an interactive table.

## Features

- **Category Selection**: Choose from different internship categories using the sidebar.
- **Number of Pages**: Adjust the number of Internshala pages to scrape.
- **Data Display**: View the scraped internship details in a well-structured, interactive table.
  
## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/internshala-scraper.git
   cd internshala-scraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure to download the `category1.txt` file (containing internship categories) and place it in the same directory as the application script.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. In the sidebar, select the categories of internships you want to scrape.

3. Set the number of pages you want to scrape from Internshala.

4. The data will be displayed in a table format with information about each internship:
   - **Title**
   - **Company Name**
   - **Location**
   - **Duration**
   - **Stipend**

## Files

- **app.py**: Main Streamlit application file.
- **category1.txt**: Text file containing a list of internship categories to select from.

## Dependencies

- `pandas`
- `streamlit`
- `requests`
- `beautifulsoup4`
- `re`

You can install these dependencies by running:
```bash
pip install pandas streamlit requests beautifulsoup4
```

## Notes

- Ensure a stable internet connection to retrieve data from Internshala.
- The scraper fetches a maximum number of pages as set by the user, so scraping too many pages may take time.
