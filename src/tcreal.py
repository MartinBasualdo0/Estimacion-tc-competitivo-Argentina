import pandas as pd
import os
from os.path import exists
from glob import glob #para eliminar archivos dentro de carpeta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import plotly.graph_objects as go
import src.constants as cs    
import src.scrap as scrap
import time

def scrap_ipc(driver):
    try: 
        os.remove(glob('./data/sh_ipc*')[0])
        print('Actualizando IPC')
    except:
        print('Descargando IPC')
    xls_div = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-color2')))
    hrefs=[]
    for element in xls_div:
        elemento=element.get_attribute('href')
        if elemento != None:
            hrefs.append(elemento)
    ip_indec = hrefs[0]
    driver.get(ip_indec)
    # paths = WebDriverWait(driver, 300, 1).until(scrap.every_downloads_chrome)
    scrap.wait_for_downloads_to_complete(timeout=100)
    time.sleep(10)
    driver.quit()
    
def get_ipc_gral():
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

    ipc_gral = pd.concat([ipc_geres,ipc_indec])
    ipc_gral.Período = pd.to_datetime(ipc_gral.Período, format="%d/%m/%Y")
    ipc_gral = ipc_gral.set_index("Período")
    ipc_gral = ipc_gral.resample('M').mean()
    return ipc_gral

def get_tc_mensual():
    cotizaciones=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=2,index_col=0)
    tc=cotizaciones[['Estados Unidos']].rename({'Estados Unidos':'dolar'},axis=1)
    tc = tc.resample('M').mean()
    return tc

def calcula_deva_real():
    tc = get_tc_mensual()
    ipc_gral = get_ipc_gral()
    deva_real=ipc_gral.merge(tc,left_index=True, right_index=True,how='left')
    deva_real.inflacion=deva_real.inflacion*(100/deva_real.inflacion.iloc[-1])
    deva_real['tc_real_hoy']=deva_real.dolar/deva_real.inflacion*100
    return deva_real

def devaluacion_real_plot():
    df = calcula_deva_real()
    x = df.index
    ultimo_mes=df.index[-1].strftime('%m/%Y')

    # Datos
    cotizaciones_plot = go.Figure()
    cotizaciones_plot.add_trace(go.Scatter(name=f"TC real", x=x, y=df["tc_real_hoy"], mode="lines",line_width=3))
    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True,dtick="M24")
    # cotizaciones_plot.update_yaxes(title_text="Tasa de devaluación")
    cotizaciones_plot.update_layout(separators=",.", font_family="georgia",
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

def writer_tcreal():
    tc_real = calcula_deva_real()
    writer = pd.ExcelWriter(f'./output/Tc a precios de hoy.xlsx', engine='xlsxwriter')
    tc_real.to_excel(writer, sheet_name='tc', index=True)
    writer.close()
    
def main():
    driver = scrap.inicio_driver(cs.indec_ipc_link)
    scrap_ipc(driver)
    devaluacion_real_plot().write_html('./output/devaluacion_argentina.html')
    writer_tcreal()
    print("Terminado tcreal")
    