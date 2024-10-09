import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from newspaper import Article


API_KEY = 'AIzaSyD-kvDePLDKBwXuQYnziuoGrB8iYtP5UDg'
SEARCH_ENGINE_ID = 'a0999913925dd4eca'
query = 'meta llama grant'

def get_search_results(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num=3"
    response = requests.get(url)
    data = response.json()
    return data['items']

results = get_search_results(query)
for item in results:
    print(item['link'])
"""
def crawl(url):
    if url in visited_urls:
        return
    visited_urls.add(url)

    html_content = get_page_content(url)
    processed_text, links = process_content(html_content, url)
    webpage_contents.append({'link': url, 'content': processed_text})

    for link in links:
        if link.startswith('http') and link not in visited_urls:
            crawl(link)
"""
    
def get_page_content(url):
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.binary_location = '/usr/bin/google-chrome'

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    content = driver.page_source
    driver.quit()
    return content

def process_content(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    # Exclude footer links
    footer = soup.find('footer')
    footer_links = set()
    
    for element in soup(['header', 'footer']):
        element.decompose()
        
    for class_name in ['sidebar', 'advertisement', 'ad', 'cookie-banner']:
        for element in soup.find_all(class_=class_name):
            element.decompose()
    
    if footer:
        footer_links = {urljoin(base_url, a['href']) for a in footer.find_all('a', href=True)}

    # Modify hyperlinks and collect non-footer links
    all_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if full_url not in footer_links:
            link_text = a.get_text()
            a.string = f"{link_text}[{full_url}]"
            all_links.append(full_url)

    text = soup.get_text()
    return text.replace("\r", "").replace("\n", "")

def write_all_webpage_contents_to_txt(webpage_contents, file_name, delimiter="\n\n---\n\n"):
    """
    Writes all the webpage contents to a single text file, optionally including URLs, separated by a delimiter.

    Args:
    - webpage_contents: List of dictionaries, each containing 'link' and 'content'.
    - file_name: Name of the output text file.
    - include_urls: Boolean indicating whether to include the URLs in the file.
    - delimiter: String to separate each webpage's content (default is "\n\n---\n\n").
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        for page in webpage_contents:
            f.write(page)
            f.write(delimiter)


def research_shallow(query):
    search_results = get_search_results(query)
    results_content = get_results_content(search_results)
    write_all_webpage_contents_to_txt(results_content, query + ' research.txt')
     

def get_results_content(search_results):
    results_content = []
    for result in search_results:
        link = result['link']
        html_content = get_page_content(link)
        processed_text = process_content(html_content, link)
        results_content.append(processed_text)
        
    return results_content
        
research_shallow('pythagorean theorem')
