import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.constants import dict_paises_importantes

def get_variacion_anualizada_tc(cotizaciones_usd:pd.DataFrame):
    monthly_cotizaciones_usd = cotizaciones_usd.groupby(pd.Grouper(freq='M')).mean()
    var_cotizaciones_usd = (monthly_cotizaciones_usd.pct_change(1)+1)**(365/30)-1
    return var_cotizaciones_usd

def get_indice_simple(cotizaciones_usd: pd.DataFrame, anio_base: str = '2019'):
    cotizaciones_2019 = cotizaciones_usd.loc[anio_base]
    media_diaria_2019 = cotizaciones_2019.mean()
    df = cotizaciones_usd / media_diaria_2019
    df = df * 100
    return df

def plot_variacion_anualizada_tc(cotizaciones_usd:pd.DataFrame, anio_desde:str="2019", mes_desde:str='01'):
    cotizaciones_usd = get_variacion_anualizada_tc(cotizaciones_usd)
    cotizaciones_usd = cotizaciones_usd[f'{anio_desde}-{mes_desde}':]
    fig = go.Figure()
    for pais,cotizacion in dict_paises_importantes.items():
        fig.add_trace(go.Scatter(x = cotizaciones_usd.index, y = cotizaciones_usd[pais], name = cotizacion))
    fig.update_layout(template = None, font_family="georgia", title_text = "Variación mensual anualizada del tc de los 3 principales socios comerciales")
    fig.update_yaxes(range=(-1,3), tickformat = ".2%")
    note = 'Fuente: BCRA'
    fig.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0)

    # Marca de agua
    fig.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="georgia", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return fig

def plot_evolucion_monedas(cotizaciones_usd:pd.DataFrame, anio_desde:str="2007",mes_desde:str="01"):
    cotizaciones_usd = cotizaciones_usd[f'{anio_desde}-{mes_desde}':]
    fig = go.Figure()
    for pais,cotizacion in dict_paises_importantes.items():
        fig.add_trace(go.Scatter(x = cotizaciones_usd.index, y = cotizaciones_usd[pais], name = cotizacion))
    fig.update_layout(template = None,font_family="georgia", title_text = "Evolución de las monedas de los tres principales socios comerciales")
    note = 'Fuente: BCRA'
    fig.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    fig.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return fig

def plot_indice_monedas(cotizaciones_usd:pd.DataFrame, anio_desde:str="2007",mes_desde:str="01", anio_base:str = "2019"):
    cotizaciones_usd = get_indice_simple(cotizaciones_usd, anio_base=anio_base)
    cotizaciones_usd = cotizaciones_usd[f'{anio_desde}-{mes_desde}':]
    fig = go.Figure()
    for pais,cotizacion in dict_paises_importantes.items():
        fig.add_trace(go.Scatter(x = cotizaciones_usd.index, y = cotizaciones_usd[pais], name = cotizacion))
    fig.update_layout(template = None,font_family="georgia",title_text = "Evolución de las monedas de los tres principales socios comerciales<br><sup>índice simple con base 2019=100",
                      height=600, width=900,)
    note = 'Fuente: BCRA'
    fig.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    fig.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    return fig

def plot_evolucion_ponderadores(ponderadores:pd.DataFrame):
    fig = go.Figure()
    for pais in ponderadores.columns:
        fig.add_trace(go.Scatter(x = ponderadores.index, y = ponderadores[pais], name = pais))
    fig.update_layout(template = None,title_text=f"Evolución de las ponderaciones publicadas por el BCRA <br><sup>Frecuencia mensual",
                    font_family = "georgia")
    note = 'Fuente: BCRA'
    fig.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                        xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    fig.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16),opacity=0.4,
                                        xref='paper', yref='paper', x=0.5, y=0.5)
    return fig

def plot_brecha(itcrm:pd.DataFrame,cotizaciones:pd.DataFrame,ponderadores:pd.DataFrame,
                anio_desde='2003', mes_desde='01'):
    tc_equilibrio = get_tc_equilibrio(itcrm, cotizaciones, ponderadores)
    itcr_objetivo = get_promedio_2002_2007(itcrm)
    df = tc_equilibrio.copy()
    df = df[f'{str(anio_desde)}-{str(mes_desde)}':]
    x = df.index
    ultima_fecha = tc_equilibrio.iloc[-1].name
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
    cotizaciones_plot.update_layout(separators=",.", font_family="georgia",
                                    margin ={'b': 50,'l':50,'r':15},
                                    height=600, width=900,
                                    template='none',
                                    title_text=f"Tipo de cambio nominal de equilibrio macroeconómico {str(anio_desde)}-{str(ultima_fecha.year)}<br><sup>Tipo de cambio que dejaría al ITCRM igual al promedio jul/02-dic/06: {str(round(itcr_objetivo,1)).replace('.',',')}",
                                    title_font=dict(size=20),
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.15, orientation='h'))

    # Flechas
    cotizaciones_plot.add_annotation(x=ultima_fecha, y=ultimo_tc_equil, align="left",
                                     text='$'+str(ultimo_tc_equil).replace('.', ','), showarrow=True, arrowhead=1)
    cotizaciones_plot.add_annotation(ax=0, ay=35, x=ultima_fecha, y=ultimo_tc_may, align="left",
                                     text='$'+str(ultimo_tc_may).replace('.', ','), showarrow=True, arrowhead=1)
    
    #Regímnes cambiarios
    anio_desde=int(anio_desde)
    if anio_desde<2007: cotizaciones_plot.add_vline(x="2006-12-12", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_desde<2012: cotizaciones_plot.add_vline(x="2011-10-28", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_desde<2016:cotizaciones_plot.add_vline(x="2015-12-17", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_desde<2019:cotizaciones_plot.add_vline(x="2018-09-26", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_desde<2020:cotizaciones_plot.add_vline(x="2019-09-01", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
    if anio_desde<2004:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC "competitivo y estable"',
        font=dict(size=13), font_family="georgia",x='2004-12-1', y=200)
    if anio_desde<2009:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Inicio intervención INDEC',
        font=dict(size=13), font_family="georgia",x='2009-7-1', y=300)
    if anio_desde<2013:cotizaciones_plot.add_annotation(showarrow=False, text=f'CEPO cambiario<br>INDEC intervenido',
        font=dict(size=13), font_family="georgia",x='2013-11-1', y=600)
    if anio_desde<2017:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC flotante<br>"Flotación sucia"',
        font=dict(size=13), font_family="georgia",x='2017-5-1', y=200)
    if anio_desde<2019:cotizaciones_plot.add_annotation(showarrow=False, text=f"Bandas cambiarias",
        font=dict(size=13), font_family="georgia",x='2019-03-1', y=400,textangle=90)
    if anio_desde<2021:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Con CEPO',
        font=dict(size=13), font_family="georgia",x='2021-9-1', y=600) 
    
    # Nota al pie
    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)

    cotizaciones_plot.add_annotation(showarrow=False, text=f"Devaluación requerida al {ultima_fecha.strftime('%d/%m/%y')}:<br>{'{:.1%}'.format(ultima_brecha).replace('.',',')}", font=dict(size=14), font_family="georgia",
                                     # xref='paper', yref='paper',
                                     x='2019-05-30', y=700)
    return cotizaciones_plot


def get_ponderaciones_diarias(ponderadores:pd.DataFrame, itcrm:pd.DataFrame):
    ponderadores_diario = ponderadores.copy()
    ponderadores_diario = ponderadores_diario.resample('D').ffill()
    ponderadores_diario = ponderadores_diario.merge(itcrm.index.to_frame(), left_index=True, right_index=True, how="right")
    ponderadores_diario = ponderadores_diario.fillna(method='ffill').drop("Período",axis=1)
    return ponderadores_diario

def get_cotizaciones_diarias(cotizaciones:pd.DataFrame, itcrm:pd.DataFrame):
    cotizaciones_final = cotizaciones.copy()
    cotizaciones_final = cotizaciones_final.drop_duplicates()
    cotizaciones_final = cotizaciones_final.merge(itcrm.index.to_frame(), left_index=True, right_index=True, how="right")
    cotizaciones_final = cotizaciones_final.fillna(method='ffill').drop("Período",axis=1)
    return cotizaciones_final

def get_canastas(cotizaciones:pd.DataFrame, itcrm:pd.DataFrame):
    df = get_cotizaciones_diarias(cotizaciones, itcrm)
    canastas = df.copy()

    for i,pais in enumerate(df.columns):
        canastas[pais] = itcrm[itcrm.columns[i+1]] / \
            df[pais]
    return canastas

def get_productoria_original(itcrm:pd.DataFrame, cotizaciones:pd.DataFrame, ponderadores:pd.DataFrame):
    cotizaciones_final = get_cotizaciones_diarias(cotizaciones, itcrm)
    canastas = get_canastas(cotizaciones, itcrm)
    ponderadores_diario = get_ponderaciones_diarias(ponderadores, itcrm)
    productoria_original = pd.DataFrame()
    productoria_original.index = itcrm.index

    for i,pais in enumerate(canastas.columns):
        productoria_original[pais] = ((cotizaciones_final[pais]
                                        # / cotizaciones_final["Estados Unidos"]
                                        * canastas[pais]
                                        #  / itcrm_rezago[itcrm_rezago.columns[i+2]]
                                        /itcrm[itcrm.columns[i+1]].shift()
                                        )**(ponderadores_diario[pais]/100))

    productoria_original['productoria'] = productoria_original.product(axis=1)

    productoria_original = productoria_original.dropna()
    return productoria_original

def get_productoria_equilibrio(itcrm:pd.DataFrame, cotizaciones:pd.DataFrame, ponderadores:pd.DataFrame):
    canastas = get_canastas(cotizaciones, itcrm)
    cotizaciones_final = get_cotizaciones_diarias(cotizaciones, itcrm)
    ponderadores_diario = get_ponderaciones_diarias(ponderadores, itcrm)
    productoria_equilibrio = pd.DataFrame()
    productoria_equilibrio.index = itcrm.index

    for i,pais in enumerate(canastas.columns):
        productoria_equilibrio[pais] = ((cotizaciones_final[pais]
                                        / cotizaciones_final["Estados Unidos"]
                                        * canastas[pais]
                                        /itcrm[itcrm.columns[i+1]].shift())
                                        **(ponderadores_diario[pais]/100))

    productoria_equilibrio['productoria'] = productoria_equilibrio.product(axis=1)

    productoria_equilibrio = productoria_equilibrio.dropna()
    return productoria_equilibrio

def get_promedio_2002_2007(itcrm:pd.DataFrame):
    promedio_2002_2007 = itcrm['2002-07-01':'2007-01-01'][itcrm.columns[0]].mean()
    return promedio_2002_2007

def get_tc_equilibrio(itcrm:pd.DataFrame, cotizaciones:pd.DataFrame, ponderadores:pd.DataFrame):
    productoria_equilibrio = get_productoria_equilibrio(itcrm, cotizaciones, ponderadores)
    itcr_buscado = get_promedio_2002_2007(itcrm)
    cotizaciones_final = get_cotizaciones_diarias(cotizaciones, itcrm)
    tc_equilibrio = pd.DataFrame()
    tc_equilibrio.index = itcrm.index

    tc_equilibrio['tc_equilibrio'] = 1 / \
        (productoria_equilibrio.productoria
        *itcrm['ITCRM '].shift()
        /itcr_buscado)
    tc_equilibrio['tc_oficial_mayorista'] = cotizaciones_final["Estados Unidos"]
    tc_equilibrio['brecha'] = tc_equilibrio.tc_equilibrio / \
        tc_equilibrio.tc_oficial_mayorista-1
        
    tc_equilibrio = tc_equilibrio.dropna()
    return tc_equilibrio

def writer_brecha_itcrm(ponderadores:pd.DataFrame, cotizaciones:pd.DataFrame, itcrm:pd.DataFrame):
    ponderadores_diario = get_ponderaciones_diarias(ponderadores, itcrm)
    cotizaciones_final = get_cotizaciones_diarias(cotizaciones, itcrm)
    canastas = get_canastas(cotizaciones, itcrm)
    productoria_original = get_productoria_original(itcrm,cotizaciones, ponderadores)
    productoria_equilibrio = get_productoria_equilibrio(itcrm, cotizaciones, ponderadores)
    tc_equilibrio = get_tc_equilibrio(itcrm, cotizaciones, ponderadores)
    
    writer = pd.ExcelWriter(f'./output/ITCRM historico.xlsx', engine='xlsxwriter')
    itcrm.to_excel(writer, sheet_name='ITCRM', index=True)
    ponderadores_diario.to_excel(
        writer, sheet_name='ponderaciones', index=True)
    cotizaciones_final.to_excel(writer, sheet_name='cotizaciones', index=True)
    canastas.to_excel(writer, sheet_name='canastas', index=True)
    tc_equilibrio.to_excel(writer, sheet_name='tc_equilibrio', index=True)
    productoria_original.to_excel(writer, sheet_name='productoria_original', index=True)
    productoria_equilibrio.to_excel(writer, sheet_name='productoria_equilibrio', index=True)
    writer.close()

def main():
    
    cotizaciones_excel = pd.read_excel('./data/cotizaciones 1997.xlsx', sheet_name=[0,1], index_col=0)
    cotizaciones=cotizaciones_excel[0]
    cotizaciones_usd = cotizaciones_excel[1]
    itcrm_excel = pd.read_excel('./data/ITCRMSerie.xlsx', header=1, skipfooter=4, index_col="Período", sheet_name=[0, 2])
    itcrm = itcrm_excel[0]
    ponderadores = itcrm_excel[2]
    itcrm.index = pd.to_datetime(itcrm.index, format='%d/%m/%Y')
    ponderadores.index = pd.to_datetime(ponderadores.index, format='%d/%m/%Y')

    writer_brecha_itcrm(ponderadores, cotizaciones, itcrm)     
    plot_brecha(itcrm,cotizaciones,ponderadores,anio_desde="2003").write_html('./output/grafico_brecha.html')
    plot_indice_monedas(cotizaciones_usd,anio_desde='2019').write_html('./output/indice_monedas.html')
    plot_variacion_anualizada_tc(cotizaciones_usd).write_html('./output/grafico_devaluacion_socios.html')
    print("Terminado cálculo de la brecha")

