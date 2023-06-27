import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# df_equilibrio=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=4)
# itcrm=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=0)

# prom_inicio = itcrm[itcrm.Período == '01/07/2002'].index[0]
# prom_final = itcrm[itcrm.Período == '01/01/2007'].index[0]
# promedio_2002_2007 = itcrm[(itcrm.index >= prom_inicio) & (
#     itcrm.index < prom_final)].mean(numeric_only=True)[0]

def plot_brecha(df:pd.DataFrame, promedio:int,fecha_ini='2003-01-01',fecha_fin=None):
    idx = df[df.Período ==fecha_ini].index[0]
    df = df[df.index >= idx].reset_index(drop=True)
    if fecha_fin: 
        idx_fin=df[df.Período == fecha_fin].index[0]
        df = df[df.index <= idx_fin].reset_index(drop=True)
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
    cotizaciones_plot.update_layout(separators=",.", font_family="georgia",
                                    margin ={'b': 50,'l':50,'r':15},
                                    height=600, width=900,
                                    template='none',
                                    title_text=f"Tipo de cambio nominal de equilibrio macroeconómico {str(fecha_ini[:4])}-{str(ultima_fecha.year)}<br><sup>Tipo de cambio que dejaría al ITCRM igual al promedio jul/02-dic/06: {str(round(promedio,1)).replace('.',',')}",
                                    title_font=dict(size=20),
                                    legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.15, orientation='h'))

    # Flechas
    cotizaciones_plot.add_annotation(x=ultima_fecha, y=ultimo_tc_equil, align="left",
                                     text='$'+str(ultimo_tc_equil).replace('.', ','), showarrow=True, arrowhead=1)
    cotizaciones_plot.add_annotation(ax=0, ay=35, x=ultima_fecha, y=ultimo_tc_may, align="left",
                                     text='$'+str(ultimo_tc_may).replace('.', ','), showarrow=True, arrowhead=1)
    
    #Regímnes cambiarios
    fecha_ini=int(fecha_ini[:4])
    if fecha_fin:
        fecha_fin=int(fecha_fin[:4])
        if fecha_ini<2007 and fecha_fin>2006: cotizaciones_plot.add_vline(x="2006-12-12", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        if fecha_ini<2012 and fecha_fin>2011: cotizaciones_plot.add_vline(x="2011-10-28", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        if fecha_ini<2016 and fecha_fin>2015:cotizaciones_plot.add_vline(x="2015-12-17", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        if fecha_ini<2018 and fecha_fin>2018:cotizaciones_plot.add_vline(x="2018-09-26", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        if fecha_ini<2020 and fecha_fin>2019:cotizaciones_plot.add_vline(x="2019-09-01", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        if fecha_ini<2004 and fecha_fin>2004:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC "competitivo y estable"',
            font=dict(size=13), font_family="georgia", xref='paper', yref='paper', x=0.5, y=0.8)
        if fecha_ini<2009 and fecha_fin>2009:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Inicio intervención INDEC',
            font=dict(size=13), font_family="georgia", x='2009-7-1', y=5.55)
        if fecha_ini<2013 and fecha_fin>2013:cotizaciones_plot.add_annotation(showarrow=False, text=f'CEPO cambiario<br>INDEC intervenido',
            font=dict(size=13), font_family="georgia", x='2014-01-1', y=20)
        if fecha_ini<2017 and fecha_fin>2019:cotizaciones_plot.add_annotation(showarrow=False, text=f'TC flotante<br>"Flotación sucia"',
            font=dict(size=13), font_family="georgia", x='2017-5-1', y=75)
        if fecha_ini<2017 and fecha_fin>2019:cotizaciones_plot.add_annotation(showarrow=False, text=f"Bandas cambiarias",
            font=dict(size=13), font_family="georgia",x='2019-03-1', y=75)
        if fecha_ini<2021 and fecha_fin>2021:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Con CEPO',
            font=dict(size=13), font_family="georgia", x='2021-9-1', y=250)
    else:
        if fecha_ini<2021:cotizaciones_plot.add_annotation(showarrow=False, text=f'Apreciación cambiaria<br>Con CEPO',
            font=dict(size=13), font_family="georgia",  x='2021-4-1', y=250)
        if fecha_ini<2020:cotizaciones_plot.add_vline(x="2019-09-01", line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        
    
    # Nota al pie
    note = 'Fuente: BCRA'
    cotizaciones_plot.add_annotation(showarrow=False, text=note, font=dict(size=12), xref='paper', x=0.1, yref='paper', y=-0.1,
                                     xanchor='right', yanchor='auto', xshift=0, yshift=0,)

    # Marca de agua
    cotizaciones_plot.add_annotation(showarrow=False, text='@MartinBasualdo0', font=dict(size=16), font_family="arial", opacity=0.4,
                                     xref='paper', yref='paper', x=0.5, y=0.5)
    if not fecha_fin:
        cotizaciones_plot.add_annotation(showarrow=False, text=f"Devaluación requerida al {ultima_fecha.strftime('%d/%m/%y')}:<br>{'{:.1%}'.format(ultima_brecha).replace('.',',')}", font=dict(size=14), font_family="georgia",
                                     # xref='paper', yref='paper',
                                     x='2021-4-1', y=200)
    return cotizaciones_plot


def main():
    df_equilibrio=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=4)
    itcrm=pd.read_excel('./output/ITCRM historico.xlsx',sheet_name=0)

    prom_inicio = itcrm[itcrm.Período == '01/07/2002'].index[0]
    prom_final = itcrm[itcrm.Período == '01/01/2007'].index[0]
    promedio_2002_2007 = itcrm[(itcrm.index >= prom_inicio) & (
    itcrm.index < prom_final)].mean(numeric_only=True)[0]
    plot_brecha(df_equilibrio, promedio_2002_2007,fecha_ini='2003-01-01',
            fecha_fin='2007-03-01'
            ).write_html('./output/2003-2007.html')

    plot_brecha(df_equilibrio, promedio_2002_2007,fecha_ini='2006-9-01',
                fecha_fin='2012-3-01'
                ).write_html('./output/2006-2012.html')


    plot_brecha(df_equilibrio, promedio_2002_2007,fecha_ini='2011-09-01',
                fecha_fin='2016-03-01',
                ).write_html('./output/2011-2016.html')

    plot_brecha(df_equilibrio, promedio_2002_2007,fecha_ini='2015-10-15',
                fecha_fin='2020-1-01',
                ).write_html('./output/2015-2020.html')

    plot_brecha(df_equilibrio, promedio_2002_2007,fecha_ini='2019-6-15'
                ).write_html('./output/2019-hoy.html')

