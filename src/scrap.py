from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os

def inicio_driver(link:str):
    service = Service(ChromeDriverManager().install())
    carpeta_descarga=os.getcwd()+"\data"
    prefs = {'download.default_directory' : carpeta_descarga,
        "directory_upgrade": True}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(link)
    driver.maximize_window()
    return driver

def every_downloads_chrome(driver):
    '''Para ver cuando terminan las descargas'''
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
