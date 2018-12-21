import re
import requests
from bs4 import BeautifulSoup
import os
import time
import threading

delay_retrys = [30,10,30]

def get_retry(url, retry=0):
    try:
        return requests.get(url)
    except Exception as e:
        if len(delay_retrys) <= retry + 1:
            return None
        else:
            print("retry:", retry, delay_retrys[retry])
            time.sleep(delay_retrys[retry])
            return get_retry(url, retry=retry+1)

url_pokemons = "https://pokeapi.co/api/v2/pokemon/"
response = get_retry(url_pokemons)
if not response:
    raise Exception("revisa tu conexion a internet")

poke_json = response.json()
results = poke_json.get("results")[:802]

types = {
    "image/jpeg": "jpeg", 
    "image/png": "png", 
}

def batch_pokemon(start, end, hilo):
    print("Hilo", hilo, start, end, len(results))
    for pokemon in results[start:end]:
        name = pokemon.get("name")
        engines = {
        "google": "https://www.google.com/search?q={}&source=lnms&tbm=isch&bih=1080&biw=1920".format(name), 
        "yahoo": "https://mx.images.search.yahoo.com/search/images?p={}".format(name),
        } #  type: dict
        if not os.path.exists('./pruebas/{}'.format(name)):
            for engine, site in engines.items():
                response = get_retry(site)
                if response: # si el engine tiene respuesta
                    soup = BeautifulSoup(response.text, 'html.parser')
                    img_tags = soup.find_all('img')
                    urls = [img.get("src", "") for img in img_tags]
                    for idx, url in enumerate(urls):
                        if len(url) < 300 and len(url) > 20 and "https" in url:
                            response = get_retry(url)
                            if response and response.status_code in range(200,300): # si trajo la imagen y fue exitoso
                                ext = types.get(response.headers.get("Content-Type"))
                                if ext:
                                    filename = "{}{}_{}.{}".format(name, idx, engine, ext)
                                    print("HILO={}, ====== filename={}".format(hilo, filename))
                                    if filename:
                                        if not os.path.exists('./pruebas/{}'.format(name)):
                                            os.makedirs('./pruebas/{}'.format(name))
                                        with open("./pruebas/{}/{}".format(name, filename), 'wb') as f:
                                            f.write(response.content)

# levantar hilos para hacerlo mas rapido 

for i in range(32):
    inicio = i*25
    final = inicio + 25
    print("inicio={}, final={}".format(inicio, final))
    threading.Thread(target=batch_pokemon, args=(inicio,final, i)).start()

# import shutil
# # borrar los que no sirven wey
# for poke_borro in poke_json.get("results")[802:]:
#     name = (poke_borro.get("name"))
#     try:
#         shutil.rmtree('./pruebas/{}'.format(name))
#     except Exception as e:
#         print("error",e)

# for poke in poke_json.get("results")[:802]:
#     name = (poke.get("name"))
#     path = './validation/{}'.format(name)
#     onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#     if len(onlyfiles) > 30:
#         for file in onlyfiles[:20]:
#             os.remove(os.path.join(path, file))
for poke in poke_json.get("results")[:802]:
    name = (poke.get("name"))
    path = './validation/{}'.format(name)
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in onlyfiles:
        if file == ".DS_Store":
            print("si")
            os.remove(os.path.join(path, file))