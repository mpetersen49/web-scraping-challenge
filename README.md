# web-scraping-challenge
## File Contents

`**mission_to_mars.ipynb**`
- jupyter notebook file to set scrape code

`**scrape_mars.py**`
- python script to run scrape code with button push on webpage

`**app.py**`
- python script to run flask server

`**index.html**`
- html file to create and format webpage

## Description of Usage

A flask server is initiated by running `app.py`. This renders `index.html` to create and run a webpage in localhost. A button is provided on the page to run a web scrape. The button runs `scrape_mars.py` which scrapes websites to gather data. The data is entered into a MongoDB database by `app.py` and is returned to the webpage using jinja2 syntax.
