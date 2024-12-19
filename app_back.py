import API_app as ak

# ------ Nombre e imagen de 20 pokemones ------

def recuperar_nombre_e_img(en):

    if en is None:

        return None

    data = {}

    try:

        enlace = ak.requests.get(en)

        enlace_JSON = enlace.json()

        for i in enlace_JSON["results"]:

            temp = i["name"]

            info = ak.requests.get(i["url"])

            info_JSON = info.json()

            for a in info_JSON:

                if a == "sprites":

                    img = info_JSON[a]["other"]["official-artwork"]["front_default"]

                    data[temp] = img

                else:

                    pass

    
    except Exception as es:

        return f"Ha ocurrido un error inesperado al intentar recuperar las imagenes: {es}"
    
    return data


# ------ Estadisticas del pokemon ------

def recuperar_estadisticas(name, url):

    data = {}

    url_q = ak.requests.get(url)
    url_JOSN = url_q.json()

    try:

        for i in url_JOSN["results"]:

            if i["name"] != name:

                pass

            else:

                info = ak.requests.get(i["url"])

                info_JSON = info.json()

                estadisticas = info_JSON["stats"]
                
                for estadistica in estadisticas:

                    data[estadistica["stat"]["name"]] = estadistica["base_stat"]

    except Exception as es:

        return f"Ha ocurrido un error inseperado: {es}"
    
    return data

# ------ Tipo/s del pokemon ------

def recuperar_tipos(name, url):

    data = []

    url_q = ak.requests.get(url)
    url_JSON = url_q.json()

    try:

        for i in url_JSON["results"]:

            if i["name"] != name:

                pass

            else:

                info = ak.requests.get(i["url"])

                info_JSON = info.json()

                tipos = info_JSON["types"]

                for tipo in tipos:

                    data.append(tipo["type"]["name"])

    except Exception as es:

        return  f"Ha ocurrido un error inesperado: {es}"
    
    return data

# ------ Prueba ------

if __name__ == "__main__":

    print(recuperar_estadisticas(name="pikachu", url="https://pokeapi.co/api/v2/pokemon?offset=20&limit=20"))