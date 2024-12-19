import requests
from flask import Flask

# ------ Llamadas ------

url = "https://pokeapi.co/api/v2/pokemon?offset=0&limit=20"
req = requests.get(url)
req_pokemones = req

# ------ JSON ------

req_pokemones_json = req_pokemones.json()

# ------ Navegar ------

class Nodo:

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class Navegacion:

    def __init__(self):

        self.nodo_actual = Nodo(valor=url)

    def avanzar(self):

        try:

            #print("avanzar| etapa 1 completada")

            current = self.nodo_actual # Nodo actual (url)

            url_actual = self.nodo_actual.valor

            #print("avanzar| etapa 2 completada")

            diccionario = requests.get(url_actual)

            diccionario_JSON = diccionario.json()

            #print("avanzar| etapa 3 completada")

            self.nodo_actual.valor = diccionario_JSON["next"]

            #print("avanzar| etapa 4 completada")

            self.nodo_actual.anterior = url_actual

            #print("avanzar| etapa 5 completada")

            siguiente = requests.get(self.nodo_actual.valor)

            siguiente_JSON = siguiente.json()

            #print("avanzar| etapa 6 completada")

            self.nodo_actual.siguiente = siguiente_JSON["next"]

            #print("avanzar| etapa 7 completada")

        except Exception as es:

            print(f"Ha ocurrido un error al intentar avanzar: {es}")
        
        return self.nodo_actual.valor

    def retroceder(self):

        try:  
            
            #print("retroceder| etapa 1 completada")

            current = self.nodo_actual # Nodo actual (url)

            #print("retroceder| etapa 2 completada")

            self.nodo_actual.valor = current.anterior

            #print("retroceder| etapa 3 completada")

            diccionario = requests.get(self.nodo_actual.valor)

            diccionario_JSON = diccionario.json()

            #print("retroceder| etapa 4 completada")

            self.nodo_actual.anterior = diccionario_JSON["previous"]

            #print("retroceder| etapa 5 completada")

            self.nodo_actual.siguiente = diccionario_JSON["next"]

            #print("retroceder| etapa 6 completada")

        except Exception as es:

            print(f"Ha ocurrido un error al intentar retroceder: {es}")

            return None

        return self.nodo_actual.valor
    
    def __str__(self):
        
        return self.nodo_actual.valor

# ------ App ------

app = Flask(__name__)

# ------ Enlaces ------

@app.route("/pokemones")
def funcion_get():
    return req_pokemones_json

# ------ Mostrar las llamadas en tipo JSON------

if __name__ == "__main__":
    app.run(debug=True)