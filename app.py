# Ejecutar todos los códigos. El resultado se ve en la carpeta "output"
import subprocess

program_list = ['scraping_bcra.py','brecha.py','tcreal.py','periodos_brecha.py']

for program in program_list:
    subprocess.call(['python', f'./src/{program}'])
    print("Finished:" + program)
    