from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    ##### start first scrape ####
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = "https://redplanetscience.com"
    browser.visit(url)


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    article = soup.find('div', class_='list_text')
        
    latest_news_title = article.find('div', class_='content_title').text
    latest_news_text = article.find('div', class_='article_teaser_body').text
    
    #### end first scrape ####

    #### start second scrape ####
    base_url = "https://spaceimages-mars.com/"
    browser.visit(base_url)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    image = soup.find('div', class_='fancybox-inner')
    image_url = image.find('img')['src']
    featured_image_url = f"{base_url}{image_url}"
    # print(featured_image_url)

    #### end second scrape ####

    #### start third scrape ####
    facts_url ="https://galaxyfacts-mars.com/"
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = df.columns.get_level_values(0)
    # df


    df.columns = df.iloc[0, :]
    df.loc[-1] = ['Description', '', '']
    df.index = df.index + 1
    df = df.sort_index()
    df.set_index('Mars - Earth Comparison', inplace=True)
    df.index.name = None
    # df

    html_table = df.to_html(classes="table table-striped")
    #html_table.replace('\n', '')
    # html_table

    #### end third scrape ####

    #### start fourth scrape ####
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)


    hemisphere_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    hemisphere_img_urls = []

    for x in range(0, 4):
        
        browser.links.find_by_partial_text(hemisphere_list[x]).click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        
        div = soup.find('div', class_='wide-image-wrapper')
        
        img_link = div.find('img', class_='wide-image')['src']
        img_url = f'{hemisphere_url}{img_link}'
        
        hemisphere_dict = {'title': title,
                        'img_url': img_url}
        
        hemisphere_img_urls.append(hemisphere_dict)
        
        browser.links.find_by_partial_text('Back').click()
        
    # hemisphere_img_urls

    browser.quit()
    #### end fourth scrape ####

    # create final dictionary to load to mongoDB
    mars_data = {'latest_news_title': latest_news_title,
                 'latest_news_text': latest_news_text,
                 'featured_img_url': featured_image_url,
                 'html_table': html_table,
                 'hemisphere_img_urls': hemisphere_img_urls}    

    return mars_data