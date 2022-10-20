
# Estimación de un tipo de cambio de equilibrio macroeconómico

Autor: [MartinBasualdo0](https://twitter.com/MartinBasualdo0)

El presente código es el utilizado para crear los siguientes informes, para más información metodológica, consultar su último apartado. Por las dudas, el xlsx "Metodología en excel" tiene el paso a paso, especialmente para aquellas personas que se sientan más cómodas con dicho programa.

- [https://rpubs.com/martinbasualdo0/tc-equil-macro]()
- [https://www.alphacast.io/p/Martinbasualdo0/insights/2022-9-2-ViZoHd]()

El uso es sencillo, _app.py_ permite ejecutar los códigos necesarios para exportar los gráficos y tablas utilizadas en los informes. Los códigos se encuentran en la carpeta "src", los archivos exportados, en "output". Para una cuasi-explicación de los pasos realizados en python, la carpeta "jupyter" contiene los jupyter notebooks.

__A tener en cuenta__: se utiliza selenium, por lo que es necesario tener descargado el _chromedriver.exe acorde a la versión de tu google chrome. [https://chromedriver.chromium.org/downloads]()_

## Librerías

Librerías a instalar en el ambiente:

- pandas
- plotly
- selenium
- beautifulsoup4
- openpyxl

Comando: pip install pandas plotly selenium beautifulsoup4 requests openpyxl

Cualquier duda, estoy a su disposición
