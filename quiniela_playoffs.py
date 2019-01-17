equipos = [
    "patriots", 
    "baltimore", 
    "charguers", 
    "chifs", 
    "rams", 
    "saints", 
    "colts", 
    "texans", 
    "seahawks", 
    "cowboys", 
    "eagles", 
    "bears"
]
personas = ["ERICK", "JUYO", "ADRIAN", "ARTURO", "JONA", "ALDO"]
import random
from random import shuffle
shuffle(personas)
shuffle(equipos)
persona_equipo = {}
for persona in personas:
    persona_equipo[persona] = {
            "equipo_1": equipos.pop(random.randrange(0, len(equipos) )), 
            "equipo_2":equipos.pop(random.randrange(0, len(equipos) ))
        }

from beautifultable import BeautifulTable
table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_RIGHT, default_padding=3)

table.column_headers = ["NOMBRE", "EQUIPO_1", "EQUIPO_2"]
table.column_alignments['NOMBRE'] = BeautifulTable.ALIGN_LEFT

table.header_separator_char = '='
table.row_separator_char = ''
table.intersection_char = ''

for persona, equipos in persona_equipo.items():
    table.append_row([persona, equipos["equipo_1"], equipos["equipo_2"]])

print(table)
