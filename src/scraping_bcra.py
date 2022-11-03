# %%
import pandas as pd
from datetime import date
import time
from time import sleep
import sys
import os
from os.path import exists
from glob import glob #para eliminar archivos dentro de carpeta
from datetime import datetime
# Para scrap
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

# %%
if exists('./data/ITCRMSerie.xlsx'):
    os.remove('./data/ITCRMSerie.xlsx')

# %%
#Scrap
link='https://bcra.gob.ar/PublicacionesEstadisticas/Evolucion_moneda.asp'
itcrm='https://www.bcra.gob.ar/PublicacionesEstadisticas/Indices_tipo_cambio_multilateral.asp'
# Descargar los datos de la web

path='./selenium/chromedriver.exe'
# carpeta_descarga=os.getcwd()+'/data'
carpeta_descarga=os.getcwd()+'\data'
#Con getcwd() se encuentra el path absoluto

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : carpeta_descarga,
        "directory_upgrade": True}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(path,options=chrome_options)

driver.get(itcrm)
itcrm_href=driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[1]/p[4]/a')
itcrm_href.click()
driver.get(link)
driver.maximize_window()

# %% [markdown]
# Si existe el archivo con cotizaciones -> descarga una actualizacion
# 
# Si no existe -> descarga toda la tabla

# %%
dict_paises={'12': 'Brasil',
 '17': 'Canadá',
 '11': 'Chile',
 '2': 'Estados Unidos',
 '33': 'México',
 '10': 'Uruguay',
 '83': 'China',
 '40': 'India',
 '19': 'Japón',
 '1': 'Reino Unido',
 '5': 'Suiza',
 '98': 'Zona Euro',
 '320': 'Vietnam'}

# %%
if exists('./data/cotizaciones 1997.xlsx'):
    cotizaciones=pd.read_excel('./data/cotizaciones 1997.xlsx')
    cotizaciones.Período=pd.to_datetime(cotizaciones.Período,format='%d/%m/%Y')
    ultima_cot=cotizaciones.Período.iloc[-1].strftime('%Y.%m.%d')
    lista_cod_monedas=list(dict_paises.keys())
    paises=list(dict_paises.values())
    cotizaciones.Período=cotizaciones.Período.apply(lambda x: x.strftime('%d/%m/%Y'))
else:
    lista_cod_monedas=list(dict_paises.keys())
    ultima_cot='1997.01.02'
    paises=list(dict_paises.values())
    
def get_primera_tabla(link=link,ultima_cot=ultima_cot,cod_moneda=lista_cod_monedas[0]):
    driver.get(link)

    drop_downs=driver.find_elements(By.CLASS_NAME, "form-control")

    select_fecha=Select(drop_downs[0])
    select_fecha.select_by_value(ultima_cot) #fecha
    select_moneda=Select(drop_downs[1])
    select_moneda.select_by_value(lista_cod_monedas[0]) #brasil

    boton=driver.find_element(By.CLASS_NAME, "btn-sm")
    boton.click()

    table_trs=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/table").get_attribute('outerHTML')
    soup = BeautifulSoup(table_trs, 'html.parser')
    df=pd.read_html(str(soup),thousands='.')[0]
    df.columns=['Período','del',paises[0]]
    df.drop('del',axis=1,inplace=True)
    df[paises[0]]=df[paises[0]].apply(lambda x: x.replace(',','.')).astype(float)
    return df
def get_primera_tabla_actualizada(link=link,ultima_cot=ultima_cot,cod_moneda=lista_cod_monedas[0]):
    driver.get(link)

    drop_downs=driver.find_elements(By.CLASS_NAME, "form-control")

    select_fecha=Select(drop_downs[0])
    select_fecha.select_by_value(ultima_cot) #fecha
    select_moneda=Select(drop_downs[1])
    select_moneda.select_by_value(lista_cod_monedas[0]) #brasil

    boton=driver.find_element(By.CLASS_NAME, "btn-sm")
    boton.click()

    table_trs=driver.find_elements(By.XPATH,"/html/body/div/div[2]/div/div/div/table/tbody/tr")
    value_list = []
    for row in table_trs:
        value_list.append({
            'Período':row.find_elements(By.TAG_NAME, "td")[0].text,
            paises[0]:row.find_elements(By.TAG_NAME, "td")[2].text
        })
    df=pd.DataFrame(value_list)
    df[paises[0]]=df[paises[0]].apply(lambda x: float(x.replace(',','.')))
    return df

if exists('./data/cotizaciones 1997.xlsx'):
     
    cotizaciones_nuevas=get_primera_tabla_actualizada()

    for i in range(1,len(lista_cod_monedas)):
        for x in range(0,4):
            try:  
                driver.get(link)
                drop_downs=driver.find_elements(By.CLASS_NAME, "form-control")

                select_fecha=Select(drop_downs[0])
                select_fecha.select_by_value(ultima_cot) #fecha
                select_moneda=Select(drop_downs[1])
                select_moneda.select_by_value(lista_cod_monedas[i]) #moneda

                boton=driver.find_element(By.CLASS_NAME, "btn-sm")
                boton.click()
                
                table_trs=driver.find_elements(By.XPATH,"/html/body/div/div[2]/div/div/div/table/tbody/tr")
                value_list = []
                for row in table_trs:
                    value_list.append({
                        'Período':row.find_elements(By.TAG_NAME, "td")[0].text,
                        paises[i]:row.find_elements(By.TAG_NAME, "td")[2].text
                        })
                df=pd.DataFrame(value_list)
                df[paises[i]]=df[paises[i]].apply(lambda x: float(x.replace(',','.')))
                cotizaciones_nuevas=cotizaciones_nuevas.merge(df,on='Período')
                IndexError = None
            except Exception as IndexError:
                pass
        
            if IndexError:
                sleep(2)
            else:
                break
    driver.quit()
    cotizaciones_nuevas.Vietnam=cotizaciones_nuevas.Vietnam/1000
    cotizaciones=pd.concat([cotizaciones,cotizaciones_nuevas]).drop_duplicates('Período').reset_index(drop=True)
    
else:
    for x in range(0,4):
        try:
            cotizaciones=get_primera_tabla()

            for i in range(1,len(lista_cod_monedas)):
                driver.get(link)
                drop_downs=driver.find_elements(By.CLASS_NAME, "form-control")

                select_fecha=Select(drop_downs[0])
                select_fecha.select_by_value(ultima_cot) #fecha
                select_moneda=Select(drop_downs[1])
                select_moneda.select_by_value(lista_cod_monedas[i]) #moneda

                boton=driver.find_element(By.CLASS_NAME, "btn-sm")
                boton.click()
                
                table_trs=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/table").get_attribute('outerHTML')
                soup = BeautifulSoup(table_trs, 'html.parser')
                df=pd.read_html(str(soup),thousands='.')[0]
                df.columns=['Período','del',paises[i]]
                df.drop('del',axis=1,inplace=True)
                df[paises[i]]=df[paises[i]].apply(lambda x: x.replace(',','.')).astype(float)
                cotizaciones=cotizaciones.merge(df,on='Período',how='left')
                IndexError = None
                
        except Exception as IndexError:
            pass
        
        if IndexError:
            sleep(2)
        else:
            break
    driver.quit()
    cotizaciones.Vietnam=cotizaciones.Vietnam/1000
    

# %% [markdown]
# Outliers y datos repetidos:

# %%
cotizaciones[cotizaciones.Período=='24/04/2001'].México
cotizaciones.loc[cotizaciones.index==1281, 'México'] = 0.107990
cotizaciones=cotizaciones.drop_duplicates('Período',keep='first')
cotizaciones.Período=pd.to_datetime(cotizaciones['Período'],format='%d/%m/%Y')

# %%
# cotizaciones=cotizaciones.drop_duplicates('Período')
fin = cotizaciones.Período.iloc[-1].strftime('%m/%d/%Y')
inicio = cotizaciones.Período[0].strftime('%m/%d/%Y')
cotizaciones.Período=cotizaciones.Período.apply(lambda x: x.strftime('%d/%m/%Y'))


monthDates = pd.DataFrame({
    'Período': pd.date_range(start=inicio, end=fin, freq='d').strftime('%d/%m/%Y')
})
cotizaciones=monthDates.merge(cotizaciones,how='outer',on='Período')
cotizaciones=(cotizaciones.drop_duplicates('Período').reset_index(drop=True)
)


# %%
cotizaciones_usd=cotizaciones.copy()
for i in range(len(paises)):
  cotizaciones_usd[paises[i]]=cotizaciones['Estados Unidos']/cotizaciones[paises[i]]
  
cotizaciones=cotizaciones.fillna(method='ffill')
cotizaciones_usd=cotizaciones_usd.fillna(method='ffill')

# %%
cotizaciones_usd=cotizaciones.copy()
for i in range(len(paises)):
  cotizaciones_usd[paises[i]]=cotizaciones['Estados Unidos']/cotizaciones[paises[i]]
cotizaciones_usd['Estados Unidos']=cotizaciones['Estados Unidos']
cotizaciones_usd.rename({'Estados Unidos':'Argentina'},axis=1,inplace=True)
cotizaciones_usd=cotizaciones_usd.drop_duplicates('Período')
cotizaciones_usd['Período'] = pd.to_datetime(cotizaciones_usd['Período'], format='%d/%m/%Y')
cotizaciones_usd['dia']=cotizaciones_usd.Período.apply(lambda x: x.day)
cotizaciones_usd['mes']=cotizaciones_usd.Período.apply(lambda x: x.month)
cotizaciones_usd['anio']=cotizaciones_usd.Período.apply(lambda x: x.year)
cotizaciones_usd



