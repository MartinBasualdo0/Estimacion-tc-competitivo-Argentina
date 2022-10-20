# %%
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %% [markdown]
# China: datos faltantes antes de 02/01/2006

# %%
cotizaciones = pd.read_excel('./data/cotizaciones 1997.xlsx', sheet_name=0)
cotizaciones_usd = pd.read_excel('./data/cotizaciones 1997.xlsx', sheet_name=1)
lista_paises = cotizaciones_usd.columns[1:-3]

var_cotizaciones_usd = cotizaciones_usd.copy()
var_cotizaciones_usd=var_cotizaciones_usd.groupby(['anio','mes'],as_index=False).mean()
var_cotizaciones_usd['Período']=pd.to_datetime('1/'+var_cotizaciones_usd.mes.astype(str)+'/'+var_cotizaciones_usd.anio.astype(str), format='%d/%m/%Y')
# var_cotizaciones_usd=var_cotizaciones_usd.fillna(method='bfill')
for i in range(len(lista_paises)):
    var_cotizaciones_usd[lista_paises[i]
                         ] = var_cotizaciones_usd[lista_paises[i]].pct_change(12)

var_cotizaciones_usd.drop(['mes','anio'],axis=1,inplace=True)
cotizaciones_usd.drop(['dia','mes','anio'],axis=1,inplace=True)

var_cotizaciones_usd

# %%
def plot_tasa_deva(df=var_cotizaciones_usd, anio='2007', mes='01', dia='01'):
    idx = df[df.Período == f'{str(anio)}-{str(mes)}-{str(dia)}'].index[0]
    var_cotizaciones_usd = df[df.index >= idx].reset_index(drop=True)

    x = var_cotizaciones_usd["Período"]
    # Datos
    cotizaciones_plot = go.Figure()
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Real", x=x, y=var_cotizaciones_usd["Brasil"], mode="lines"))
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Yuan", x=x, y=var_cotizaciones_usd["China"], mode="lines"))
    # cotizaciones_plot.add_trace(go.Scatter(name = "ARS-USD", x=x, y=var_cotizaciones_usd["Argentina"], mode = "lines"))
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Euro", x=x, y=var_cotizaciones_usd["Zona Euro"], mode="lines"))

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True)
    # cotizaciones_plot.update_yaxes(title_text="Tasa de devaluación", tickformat= ',.0%')
    cotizaciones_plot.update_yaxes(
        title_text="Tasa de devaluación", tickformat=',.0%')
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    height=600, width=1000,
                                    template='none',
                                    title_text=f"Tasa de devaluación de las monedas de los tres principales socios comerciales <br><sup>Variación interanual con frecuencia mensual",
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.36, orientation='h'))

    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return cotizaciones_plot


def evolucion_monedas(df=cotizaciones_usd, anio='2006', mes='01', dia='01'):
    idx = df[df.Período == f'{str(anio)}-{str(mes)}-{str(dia)}'].index[0]
    cotizaciones_usd = df[df.index >= idx].reset_index(drop=True)
    x = cotizaciones_usd["Período"]

    # Datos
    cotizaciones_plot = go.Figure()
    cotizaciones_plot.add_trace(go.Scatter(name=f"Brasil", x=x, y=cotizaciones_usd["Brasil"], mode="lines"))
    cotizaciones_plot.add_trace(go.Scatter(name=f"China", x=x, y=cotizaciones_usd["China"], mode="lines"))
    cotizaciones_plot.add_trace(go.Scatter(name=f"Euro", x=x, y=cotizaciones_usd["Zona Euro"], mode="lines"))

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True)
    # cotizaciones_plot.update_yaxes(title_text="Tasa de devaluación")
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    height=600, width=1000,
                                    template='none',
                                    title_text=f"Evolución de las paridades con el USD de los tres principales socios comerciales <br><sup>Frecuencia diaria",
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.36, orientation='h'))

    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return cotizaciones_plot


def indice_monedas(df=cotizaciones_usd, anio='2006', mes='01', dia='01'):
    idx = df[df.Período == f'{str(anio)}-{str(mes)}-{str(dia)}'].index[0]
    df = df[df.index >= idx].reset_index(drop=True)
    lista_paises=df.columns[1:]
    var_cotizaciones_usd = df.copy()
    base = var_cotizaciones_usd[var_cotizaciones_usd.Período == '2019-01-01'].index[0]
    for i in range(len(lista_paises)):
        var_cotizaciones_usd[lista_paises[i]] = var_cotizaciones_usd[lista_paises[i]
                                                                     ]/var_cotizaciones_usd[lista_paises[i]].iloc[base]*100
    # var_cotizaciones_usd.dropna(inplace=True)

    x = var_cotizaciones_usd["Período"]

    # Datos
    cotizaciones_plot = go.Figure()
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Real", x=x, y=var_cotizaciones_usd["Brasil"], mode="lines"))
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Yuan", x=x, y=var_cotizaciones_usd["China"], mode="lines"))
    # cotizaciones_plot.add_trace(go.Scatter(name = "ARS-USD", x=x, y=var_cotizaciones_usd["Argentina"], mode = "lines"))
    cotizaciones_plot.add_trace(go.Scatter(
        name="USD-Euro", x=x, y=var_cotizaciones_usd["Zona Euro"], mode="lines"))

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True)
    # cotizaciones_plot.update_yaxes(title_text="Tasa de devaluación", tickformat= ',.0%')
    cotizaciones_plot.update_yaxes(
        title_text="Base enero 2019=100")
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    margin ={'b': 50,'l':50,'r':15},
                                    height=600, width=900,
                                    template='none',
                                    title_text=f"Evolución de las monedas de los tres principales socios comerciales <br><sup>índice simple con base enero 2019=100",
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.3, orientation='h'))

    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.09,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return cotizaciones_plot


# plot_tasa_deva(anio=1999)

evolucion_monedas(anio=2021,mes=1)

indice_monedas(anio=2007)


# %%
cotizaciones_usd=cotizaciones_usd.fillna(method='bfill')
cotizaciones=cotizaciones.fillna(method='bfill')

# %%
itcrm = pd.read_excel('./data/ITCRMSerie.xlsx', header=1, skipfooter=4)

ponderadores = pd.read_excel('./data/ITCRMSerie.xlsx', sheet_name=2, header=1)
ponderadores.Período = pd.to_datetime(
    ponderadores['Período'], format='%d/%m/%Y')


def evolucion_ponderaciones():
    x = ponderadores["Período"]

    # Datos
    cotizaciones_plot = go.Figure()
    for index, pais in enumerate(ponderadores.columns[1:]):
        cotizaciones_plot.add_trace(go.Scatter(
            name=f"{pais}", x=x, y=ponderadores[pais], mode="lines"))

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True)
    cotizaciones_plot.update_yaxes(title_text="Ponderaciones %")
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    height=600, width=1000,
                                    template='none',
                                    title_text=f"Evolución de las ponderaciones publicadas por el BCRA <br><sup>Frecuencia mensual",
                                    legend=dict(yanchor="top", y=-.05, xanchor="left", x=0.36, orientation='h'))

    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return cotizaciones_plot


# %%
# Tipo de cambio real

fin = itcrm.Período.iloc[-1].strftime('%m/%d/%Y')
inicio = itcrm.Período[0].strftime('%m/%d/%Y')
ponderadores.Período = ponderadores.Período.apply(
    lambda x: x.strftime('%d/%m/%Y'))
itcrm.Período = itcrm.Período.apply(lambda x: x.strftime('%d/%m/%Y'))

monthDates = pd.DataFrame({
    'Período': pd.date_range(start=inicio, end=fin, freq='d').strftime('%d/%m/%Y')
})

ponderaciones_completo = (monthDates[['Período']].merge(ponderadores, on='Período', how='left').fillna(method='ffill')
                          .merge(itcrm[['Período']], on='Período', how='right'))

# ponderaciones_completo[ponderaciones_completo.Período=='01/01/2004']
ponderaciones_completo


# %%
cotizaciones_final = (ponderaciones_completo[['Período']].merge(cotizaciones, on='Período', how='left')
                     .fillna(method='ffill')
                     .drop_duplicates('Período', ignore_index=True)
                     )

indice = cotizaciones_final[cotizaciones_final.Período ==
                           cotizaciones.Período.iloc[0]].index
cotizaciones_final = cotizaciones_final[cotizaciones_final.index >= indice[0]].reset_index(
    drop=True)


# %%
ponderaciones_final = cotizaciones_final[['Período']].merge(
    ponderaciones_completo, on='Período')
itcrm_final = cotizaciones_final[['Período']].merge(itcrm, on='Período')

# Canasta_t=itcr_t/cotiz_t

canastas = pd.DataFrame()
canastas['Período'] = itcrm_final.Período
lista_paises = ponderaciones_final.columns[1:]

for i in range(len(lista_paises)):
    canastas[lista_paises[i]] = itcrm_final[itcrm_final.columns[i+2]] / \
        cotizaciones_final[cotizaciones_final.columns[i+1]]
canastas


# %%
indice = itcrm[itcrm.Período == cotizaciones.Período.iloc[0]].index-1
itcrm_rezago = itcrm[(itcrm.index >= indice[0]) & (
    itcrm.index <= itcrm.index[-2])].reset_index(drop=True)

itcrm_rezago


# %%
cotizaciones_final[cotizaciones_final.columns[0+1]]

# %% [markdown]
# ### Productoria
# 
# Primero calculo la original, que parte del paso para calcular el itcrm

# %%
productoria_original = pd.DataFrame()
productoria_original['Período'] = itcrm_final.Período

for i in range(len(lista_paises)):
    productoria_original[lista_paises[i]] = ((cotizaciones_final[cotizaciones_final.columns[i+1]]
                                    # / cotizaciones_final["Estados Unidos"]
                                     * canastas[canastas.columns[i+1]]
                                     / itcrm_rezago[itcrm_rezago.columns[i+2]]
                                     )**(ponderaciones_final[ponderaciones_final.columns[i+1]]/100))

productoria_original['productoria'] = productoria_original[productoria_original.columns[1:]
                                         ].product(axis=1)

productoria_original

# %%
productoria_equilibrio = pd.DataFrame()
productoria_equilibrio['Período'] = itcrm_final.Período

for i in range(len(lista_paises)):
    productoria_equilibrio[lista_paises[i]] = ((cotizaciones_final[cotizaciones_final.columns[i+1]]
                                    / cotizaciones_final["Estados Unidos"]
                                     * canastas[canastas.columns[i+1]]
                                     / itcrm_rezago[itcrm_rezago.columns[i+2]])
                                    **(ponderaciones_final[ponderaciones_final.columns[i+1]]/100))

productoria_equilibrio['productoria'] = productoria_equilibrio[productoria_equilibrio.columns[1:]
                                         ].product(axis=1)

productoria_equilibrio

# %%
# Tipo de cambio de equilibrio = 1/(productoria_t*ITCRM_rezagado/promedio)
prom_inicio = itcrm[itcrm.Período == '01/07/2002'].index[0]
prom_final = itcrm[itcrm.Período == '01/01/2007'].index[0]
promedio_2002_2007 = itcrm[(itcrm.index >= prom_inicio) & (
    itcrm.index < prom_final)].mean()[0]

tc_equilibrio = pd.DataFrame()
tc_equilibrio['Período'] = itcrm_final.Período

tc_equilibrio['tc_equilibrio'] = 1 / \
    (productoria_equilibrio.productoria*itcrm_rezago['ITCRM ']/promedio_2002_2007)
tc_equilibrio['tc_oficial_mayorista'] = cotizaciones_final["Estados Unidos"]
tc_equilibrio['Período'] = pd.to_datetime(
    tc_equilibrio['Período'], format='%d/%m/%Y')
tc_equilibrio['brecha'] = tc_equilibrio.tc_equilibrio / \
    tc_equilibrio.tc_oficial_mayorista-1

tc_equilibrio


# %%
idx = tc_equilibrio[tc_equilibrio.Período == '2006-01-01'].index[0]
tc_equilibrio[tc_equilibrio.index >= idx]

# %%
def plot_brecha(df=tc_equilibrio, anio_ini='2003', mes='01', dia='01'):
    idx = df[df.Período == f'{str(anio_ini)}-{str(mes)}-{str(dia)}'].index[0]
    df = df[df.index >= idx].reset_index(drop=True)
    x = df["Período"]
    ultima_fecha = df.Período.iloc[-1]
    ultimo_tc_equil = round(df.tc_equilibrio.iloc[-1], 2)
    ultimo_tc_may = df.tc_oficial_mayorista.iloc[-1]
    ultima_brecha = df.brecha.iloc[-1]

    # Datos
    cotizaciones_plot = make_subplots(specs=[[{"secondary_y": True}]])
    cotizaciones_plot.add_trace(go.Scatter(
        name="Tipo de cambio de equilibro", x=x, y=df["tc_equilibrio"], mode="lines"), secondary_y=False)
    cotizaciones_plot.add_trace(go.Scatter(name="Tipo de cambio oficial mayorista",
                                x=x, y=df["tc_oficial_mayorista"], mode="lines"), secondary_y=False)
    cotizaciones_plot.add_trace(go.Scatter(
        name="Brecha (der)", x=x, y=df["brecha"], mode="lines"), secondary_y=True)

    # Propiedades
    cotizaciones_plot.update_xaxes(showgrid=True)
    cotizaciones_plot.update_yaxes(
        title_text="Cotizaciones", secondary_y=False, zeroline=False)
    cotizaciones_plot.update_yaxes(
        title_text="Brecha (devaluación requerida)", tickformat=',.0%', secondary_y=True)
    cotizaciones_plot.update_layout(separators=",.", font_family="Georgia",
                                    margin ={'b': 50,'l':50,'r':15},
                                    height=600, width=900,
                                    template='none',
                                    title_text=f"Tipo de cambio nominal de equilibrio macroeconómico {str(anio_ini)}-{str(ultima_fecha.year)}<br><sup>Tipo de cambio que dejaría al ITCRM igual al promedio jul/02-dic/06: {str(round(promedio_2002_2007,1)).replace('.',',')}",
                                    title_font=dict(size=20),
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.15, orientation='h'))

    # Flechas
    cotizaciones_plot.add_annotation(x=ultima_fecha, y=ultimo_tc_equil, align="left",
                                     text='$'+str(ultimo_tc_equil).replace('.', ','), showarrow=True, arrowhead=1)
    cotizaciones_plot.add_annotation(ax=0, ay=35, x=ultima_fecha, y=ultimo_tc_may, align="left",
                                     text='$'+str(ultimo_tc_may).replace('.', ','), showarrow=True, arrowhead=1)
    
    #Regímnes cambiarios
    anio_ini=int(anio_ini)
    if anio_ini<2007: cotizaciones_plot.add_vline(x="2006-12-12", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_ini<2012: cotizaciones_plot.add_vline(x="2011-10-28", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_ini<2016:cotizaciones_plot.add_vline(x="2015-12-17", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_ini<2019:cotizaciones_plot.add_vline(x="2018-09-26", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_ini<2020:cotizaciones_plot.add_vline(x="2019-09-01", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_ini<2004:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC competitivo y estable<br>"Crawling peg"',
        font=dict(size=13), font_family="georgia",x='2004-12-1', y=75)
    if anio_ini<2009:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Inicio intervención INDEC',
        font=dict(size=13), font_family="georgia",x='2009-7-1', y=200)
    if anio_ini<2013:cotizaciones_plot.add_annotation(showarrow=False, text=f'CEPO cambiario<br>INDEC intervenido',
        font=dict(size=13), font_family="georgia",x='2013-11-1', y=250)
    if anio_ini<2017:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC flotante<br>"Flotación sucia"',
        font=dict(size=13), font_family="georgia",x='2017-5-1', y=75)
    if anio_ini<2019:cotizaciones_plot.add_annotation(showarrow=False, text=f"Bandas cambiarias",
        font=dict(size=13), font_family="georgia",x='2019-03-1', y=175,textangle=90)
    if anio_ini<2021:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Con CEPO',
        font=dict(size=13), font_family="georgia",x='2021-9-1', y=50) 
    
    # Nota al pie
    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)

    cotizaciones_plot.add_annotation(showarrow=False, text=f"Devaluación requerida al {ultima_fecha.strftime('%d/%m/%y')}:<br>{'{:.1%}'.format(ultima_brecha).replace('.',',')}", font=dict(size=14), font_family="georgia",
                                     # xref='paper', yref='paper',
                                     x='2019-05-30', y=250)
    return cotizaciones_plot



# %%
writer = pd.ExcelWriter(f'./output/ITCRM historico.xlsx', engine='xlsxwriter')
itcrm.to_excel(writer, sheet_name='ITCRM', index=False)
ponderaciones_completo.to_excel(
    writer, sheet_name='ponderaciones', index=False)
cotizaciones_final.to_excel(writer, sheet_name='cotizaciones', index=False)
canastas.to_excel(writer, sheet_name='canastas', index=False)
tc_equilibrio.to_excel(writer, sheet_name='tc_equilibrio', index=False)
writer.save()


# %%
plot_brecha(anio_ini=2003).write_html('./output/grafico_brecha.html')
indice_monedas(anio=2007).write_html('./output/indice_monedas.html')
plot_tasa_deva(anio=2007).write_html('./output/grafico_devaluacion_socios.html')


