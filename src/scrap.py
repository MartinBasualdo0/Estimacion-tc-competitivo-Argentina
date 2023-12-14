from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
import time

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

# def every_downloads_chrome(driver):
#     '''Para ver cuando terminan las descargas'''
#     if not driver.current_url.startswith("chrome://downloads"):
#         driver.get("chrome://downloads/")
#     return driver.execute_script("""
#         var items = document.querySelector('downloads-manager')
#             .shadowRoot.getElementById('downloadsList').items;
#         if (items.every(e => e.state === "COMPLETE"))
#             return items.map(e => e.fileUrl || e.file_url);
#         """)
    
def every_downloads_chrome():
    '''Check if all downloads are complete'''
    while True:
        carpeta_descarga=os.getcwd()+"\data"
        incomplete_downloads = [name for name in os.listdir(carpeta_descarga) if name.endswith('.tmp') or name.endswith('.crdownload')]
        if not incomplete_downloads:
            return True  # Return True when no more .crdownload files in the directory
        time.sleep(1)  # Wait for 1 second before checking again

def wait_for_downloads_to_complete(timeout:int):
    '''Wait for all downloads to complete with a timeout'''
    start_time = time.time()  # Save the start time

    while not every_downloads_chrome():  # Wait until all downloads are complete
        if time.time() - start_time > timeout:  # If the timeout has elapsed, break the loop
            print('Timeout elapsed, stopping downloads')
            break
        time.sleep(1)  # Wait for 1 second before checking again