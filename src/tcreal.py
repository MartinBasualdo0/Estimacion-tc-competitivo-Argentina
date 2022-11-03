# %%
import pandas as pd
import os
from os.path import exists
from glob import glob #para eliminar archivos dentro de carpeta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
#graficos
import plotly.graph_objects as go

# %%
try: 
    os.remove(glob('./data/sh_ipc*')[0])
    print('actualizando archivo')
except:
    print('No esta descargado el archivo, no problema')

# %%
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

# %%
#Scrap
indec = 'https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31'
# Descargar los datos de la web

path='./selenium/chromedriver.exe'
carpeta_descarga=os.getcwd()+'\data'
#Con getcwd() se encuentra el path absoluto

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : carpeta_descarga,
        "directory_upgrade": True}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(path,options=chrome_options)

driver.get(indec)

WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-color2')))
xls_div=driver.find_elements(By.CLASS_NAME, 'a-color2')
hrefs=[]
for element in xls_div:
    elemento=element.get_attribute('href')
    if elemento != None:
        hrefs.append(elemento)
ip_indec = hrefs[1]
driver.get(ip_indec)
paths = WebDriverWait(driver, 300, 1).until(every_downloads_chrome)
driver.quit()



# %%
ipc_indec=(pd.read_excel(glob('./data/sh_ipc*')[0],skipfooter=5,header=5,sheet_name=2)
.T.reset_index()
.rename({'index':'Período',3:'inflacion'},axis=1))[['Período','inflacion']][1:].reset_index(drop=True)
ipc_indec.Período=pd.to_datetime(ipc_indec.Período).apply(lambda x: x.strftime('%d/%m/%Y'))
ipc_indec

ipc_geres=(pd.read_excel('./data/inflacion nivel general_ GERES.xlsx',header=2)
.rename({'NIVEL (dic 2001=100)':'inflacion'},axis=1))[['Período','inflacion']]
ipc_geres.Período=pd.to_datetime(ipc_geres.Período).apply(lambda x: x.strftime('%d/%m/%Y'))
#Cambio de base a 2001
coef=ipc_geres[ipc_geres.Período=='01/12/2016'].inflacion.values[0]/ipc_indec.inflacion[0]
ipc_indec.inflacion=ipc_indec.inflacion*coef

# ipc_gral=ipc_geres.append(ipc_indec)
ipc_gral=pd.concat([ipc_geres,ipc_indec])



# %%
cotizaciones=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=2)
tc=cotizaciones[['Período','Estados Unidos']].rename({'Estados Unidos':'dolar'},axis=1)
tc

# %%
deva_real=ipc_gral.merge(tc,on="Período",how='left')
deva_real.inflacion=deva_real.inflacion*(100/deva_real.inflacion.iloc[-1])
deva_real['tc_real_hoy']=deva_real.dolar/deva_real.inflacion*100
deva_real=deva_real.drop_duplicates('Período')

deva_real

# %%
def devaluacion_real_plot(df=deva_real):
    deva_real.Período=pd.to_datetime(deva_real.Período,format='%d/%m/%Y')
    x = deva_real["Período"]
    ultimo_mes=deva_real.Período.iloc[-1].strftime('%m/%Y')

    # Datos
    cotizaciones_plot = go.Figure()
    cotizaciones_plot.add_trace(go.Scatter(name=f"TC real", x=x, y=deva_real["tc_real_hoy"], mode="lines",line_width=3))
    # cotizaciones_plot.add_trace(go.Scatter(name=f"China", x=x, y=deva_real["China"], mode="lines"))
    # cotizaciones_plot.add_trace(go.Scatter(name=f"Euro", x=x, y=deva_real["Zona Euro"], mode="lines"))

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True,dtick="M24")
    # cotizaciones_plot.update_yaxes(title_text="Tasa de devaluación")
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    margin ={'b': 70,'l':50,'r':15},
                                    height=600, width=900,
                                    template='none',
                                    title_text=f"Evolución del tipo de cambio (real)<br>A pesos del {ultimo_mes}",
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.36, orientation='h'))

    note = 'Fuente: BCRA, INDEC, GERES'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.2, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)
    note_2=('El dato de inflación fue calculado como un promedio simple entre los IPC "confiables" (San Luis, CABA, Santa Fe) y los reportados por las consultoras')

    cotizaciones_plot.add_annotation(showarrow=False, text=note_2, font=dict(size=12), xref='paper', x=.949, yref='paper', y=-0.15,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return cotizaciones_plot

devaluacion_real_plot()

# %%
devaluacion_real_plot().write_html('./output/devaluacion_argentina.html')

# %%
writer = pd.ExcelWriter(f'./output/Tc a precios de hoy.xlsx', engine='xlsxwriter')
deva_real.to_excel(writer, sheet_name='tc', index=False)
writer.save()


