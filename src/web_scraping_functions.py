
from selenium import webdriver
# to simplify management of binary drivers for different browsers import chromedriver_binary 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def getPage(url):
    # This function show a basic way to make a get requests used Selenium
    # First line to to avoid this error:
    # WebDriverException: Message: 'chromedriver' executable needs to be available in the path.
    # driver.execute_script(..) to scroll the page in Selenium untill the bottom
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")
    driver.quit()
    return soup