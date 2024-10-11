import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import os

#SEARCH_ENGINE_ID = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
#API_KEY = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_API_KEY')
SEARCH_ENGINE_ID = "a0999913925dd4eca"
API_KEY = "AIzaSyCVHviPTcwR2qmwHqsprMZGNBl8XjgDW8k"

def get_search_results(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&num=3"
    response = requests.get(url)
    data = response.json()
    return data['items']

def get_page_content(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')  # Use /tmp instead of /dev/shm
    chrome_options.add_argument('--remote-debugging-port=9222')  # Debugging port to avoid errors
    chrome_options.add_argument('--disable-gpu')  # Disable GPU to avoid issues in headless mode
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable software rasterizer to avoid crashes
    chrome_options.add_argument('--window-size=1280x1696')

    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    # Set the binary location to the installed Chromium
    chrome_options.binary_location = '/usr/bin/google-chrome'

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Your Selenium code here
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
    #write_all_webpage_contents_to_txt(results_content, query + ' research.txt')
    return '\n\n\n\n'.join(results_content)
    
     

def get_results_content(search_results):
    results_content = []
    for result in search_results:
        link = result['link']
        html_content = get_page_content(link)
        processed_text = process_content(html_content, link)
        results_content.append(processed_text)
        
    return results_content

def lambda_handler(event, context):
    # Extract the query parameter from the event
    query = event.get('queryStringParameters', {}).get('query')
    
    # Log the query
    print(f"Received query: {query}")
    
    # Use the research_shallow function to get the search result
    try:
        result = research_shallow(query)
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


#Useless modification so Docker thinks I updated it