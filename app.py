print("Inicio del programa. Duración aproximada: 4 minutos")
import src.scraping_bcra as sbcra
import src.brecha as bre
import src.periodos_brecha as pbre
import src.tcreal as tcr

sbcra.main()
print("Scrap BCRA terminado")
bre.main()
print("Brecha terminado")
pbre.main()
print("Períodos brecha terminado")
tcr.main()
print("Terminado tipo de cambio real")
print("Programa terminado")
    