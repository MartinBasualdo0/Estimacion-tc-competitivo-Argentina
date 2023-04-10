import pandas as pd
from time import sleep
import src.constants as cs
from os.path import exists
# Para scrap
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import src.scrap as scrap

lista_cod_monedas=list(cs.DICT_PAISES.keys())
paises=list(cs.DICT_PAISES.values())

def leer_cotizaciones():
    cotizaciones=pd.read_excel('./data/cotizaciones 1997.xlsx', index_col=0)
    cotizaciones.index=pd.to_datetime(cotizaciones.index,format='%d/%m/%Y')
    return cotizaciones

def corrige_outliers(df:pd.DataFrame,n_pais:int):
    '''Falta corregir outliers por día. Algunas variaciones no tiene sentido'''
    df["diff"] = df[paises[n_pais]].diff().abs()
    df["diff_next"] = df[paises[n_pais]].diff(-1).abs()
    min_diff = df.groupby("Período")[["diff", "diff_next"]].min()
    df["diff_min"] = min_diff.min(axis=1)
    duplicates = df["Período"].duplicated(keep=False)
    # print(n_pais, df[duplicates])
    for idx, val in df[duplicates].iterrows():
        next_val = df.iloc[idx+1][paises[n_pais]]
        prev_val = df.iloc[idx-1][paises[n_pais]]
        min_val = min(prev_val, next_val, key=lambda x: abs(x-val[paises[n_pais]]))
        df.at[idx, paises[n_pais]] = min_val
    df = df.drop(["diff", "diff_next", "diff_min"], axis=1)
    return df

def get_cotizaciones(driver,n_pais:int):
    table_trs=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/table").get_attribute('outerHTML')
    soup = BeautifulSoup(table_trs, 'html.parser')
    df=pd.read_html(str(soup),thousands='.')[0]
    df.columns=['Período','del',paises[n_pais]]
    df.drop('del',axis=1,inplace=True)
    df[paises[n_pais]]=df[paises[n_pais]].apply(lambda x: x.replace(',','.')).astype(float)
    df = corrige_outliers(df, n_pais)
    df = df.set_index("Período")
    return df

def select_moneda(driver, moneda:str, ultima_cot:str):
    drop_downs=driver.find_elements(By.CLASS_NAME, "form-control")

    select_fecha=Select(drop_downs[0])
    select_fecha.select_by_value(ultima_cot) #fecha
    select_moneda=Select(drop_downs[1])
    select_moneda.select_by_value(moneda) #moneda

    boton=driver.find_element(By.CLASS_NAME, "btn-sm")
    boton.click()
    return 

def scrap_itcrm():
    return urllib.request.urlretrieve(cs.itcrm, "./data/ITCRMSerie.xlsx")

def scrap_cotizaciones(driver, ultima_cot:str):
    dfs=[]
    for n_pais,moneda in enumerate(lista_cod_monedas[0:]):
        max_intentos = 4
        intentos = 0  # Contador de intentos
        while intentos < max_intentos:
            try:
                driver.get(cs.bcra_monedas) 
                select_moneda(driver, moneda, ultima_cot)           
                cotizaciones_nuevas = get_cotizaciones(driver, n_pais)
                dfs.append(cotizaciones_nuevas)
                break  # Si no hay error, se sale del bucle while
            except Exception as e:
                print("La página del BCRA tiene sus fallas, reintentando...", intentos+1, "de",max_intentos)
                intentos += 1
                if intentos == max_intentos:
                    raise  # Si se llega al límite de intentos sin éxito, se genera un error
                else:
                    sleep(2)
    driver.quit()
    return dfs

def wrangling_cotizaciones(dfs:list[pd.DataFrame], existe:bool):
    cotizaciones_nuevas = dfs[0]
    for df in dfs[1:]:
        cotizaciones_nuevas = pd.merge(cotizaciones_nuevas, df, on='Período', how='outer')
    
    cotizaciones_nuevas.index = pd.to_datetime(cotizaciones_nuevas.index, format="%d/%m/%Y")
    
    cotizaciones_nuevas.Vietnam=cotizaciones_nuevas.Vietnam/1000
    if existe:
        cotizaciones = leer_cotizaciones()
        cotizaciones=pd.concat([cotizaciones,cotizaciones_nuevas]).reset_index(drop=False).drop_duplicates('Período')
        cotizaciones = cotizaciones.set_index("Período")
        cotizaciones = cotizaciones.sort_index()
        cotizaciones = cotizaciones.fillna(method='ffill')
        return cotizaciones.fillna(method='bfill')
    else:
        
        # cotizaciones_nuevas = cotizaciones_nuevas.drop_duplicates()
        cotizaciones_nuevas = cotizaciones_nuevas.sort_index()
        cotizaciones_nuevas = cotizaciones_nuevas.fillna(method='ffill')
        return cotizaciones_nuevas.fillna(method='bfill')
    
def genera_cotizaciones_usd(cotizaciones:pd.DataFrame):
    cotizaciones_usd=cotizaciones.copy()
    for pais in cotizaciones_usd.columns:
        cotizaciones_usd[pais]=cotizaciones['Estados Unidos']/cotizaciones[pais]
    cotizaciones_usd['Estados Unidos']=cotizaciones['Estados Unidos']
    cotizaciones_usd.rename({'Estados Unidos':'Argentina'},axis=1,inplace=True)
    return cotizaciones_usd
    
def writer_cotizaciones(cotizaciones:pd.DataFrame,cotizaciones_usd:pd.DataFrame):
    writer = pd.ExcelWriter(f'./data/cotizaciones 1997.xlsx', engine='xlsxwriter')
    cotizaciones.to_excel(writer, sheet_name='cotizaciones_ars')
    cotizaciones_usd.to_excel(writer, sheet_name='cotizaciones_usd')
    writer.close()



def main():
    driver = scrap.inicio_driver(cs.bcra_monedas)
    if exists('./data/cotizaciones 1997.xlsx'):
        print("Detectó xlsx de las cotizaciones. Actualizando...")
        cotizaciones = leer_cotizaciones()   
        ultima_cot=cotizaciones.index[-1].strftime('%Y.%m.%d')
        existe = True

    else:
        print("No detecto xlsx de las cotizaciones. Scrapeando...")
        ultima_cot='1997.01.02'
        existe = False
        
    scrap_itcrm()
    dfs = scrap_cotizaciones(driver=driver, ultima_cot=ultima_cot)
    cotizaciones = wrangling_cotizaciones(dfs, existe)
    cotizaciones = cotizaciones.drop_duplicates(keep=False)
    cotizaciones_usd = genera_cotizaciones_usd(cotizaciones)
    writer_cotizaciones(cotizaciones, cotizaciones_usd)
    print("Terminado scraping_bcra")
    return 


