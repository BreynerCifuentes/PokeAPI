import app_back as bk
import API_app as ak
import flet as ft
import time

def main(page: ft.Page):

    page.window_resizable = False
    page.window_max_height = 700
    page.window_max_width = 500

    page.update()
    
    # ------ Contenedores ------

    contenedor_pokemones = ft.Container(
        content=ft.Column(
            controls=[
            ],

            scroll="auto"
        ),

        bgcolor="#695C6B",
        padding=ft.padding.only(left=40, right=40),
        margin=ft.margin.only(right=10, left=10),
        expand=True,
        border_radius=20
    )

    # ------ Botones ------

    boton_siguiente = ft.TextButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda _: Siguiente(e=None), icon_color="#3E363F")
    boton_anteror = ft.TextButton(icon=ft.icons.ARROW_BACK_IOS, on_click=lambda _: Retroceder(e=None), icon_color="#3E363F")

    # ------ Navegador ------

    navegar = ak.Navegacion() # Se crea una instancia de la clase Navegacion

    # ------ Contador ------

    contador = 0

    # ------ Funciones ------

    def actualizar(e):

        contenedor_pokemones.content.controls.clear()

        recorrer_pokemones()

        page.update()


    def recorrer_pokemones(e=None):

        pokemones = bk.recuperar_nombre_e_img(navegar.nodo_actual.valor)

        url_acutal = navegar.nodo_actual.valor

        if pokemones is None: # Si no hay pokemones en la pagina actual

            return None

        for pokemon in pokemones: # Recorre el diccionario de pokemones

            imagen = ft.Image(
                src=pokemones[pokemon],
                width=100,
                height=100
            )

            nombre = ft.Container(
                ft.Column(
                    [
                        ft.Text(value=pokemon, color="#413942")
                    ]
                ),

                border_radius=20,
                bgcolor="#FFFCE8",
                padding=ft.padding.only(left=4, right=4)
            )

            contenedor_pokemones.content.controls.append(ft.Container(
                ft.Column(
                    [
                        ft.TextButton(content=ft.Column(
                            [
                                imagen,
                                nombre
                            ]
                        ),
                        style=ft.ButtonStyle(bgcolor="#FFFCE8", overlay_color="#413942"),
                        on_click=lambda e=None, img=imagen, pokemon=pokemon, url=url_acutal: seleccionar_pokemon(e=e, img=img, pokemon=pokemon, url=url))
                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ))


    def seleccionar_pokemon(e, img, pokemon, url):

        tipo = bk.recuperar_tipos(name=pokemon, url=url) # Se recupera el tipo del pokemon
        estadisticas = bk.recuperar_estadisticas(name=pokemon, url=url) # Se recuperan las estadisticas del pokemon

        img.width = 200
        img.height = 200

        alerta = ft.AlertDialog(
            modal=True,
            bgcolor="#FFFCE8",
            content=ft.Container(
                ft.Column(
                    [   

                        # --- Imagen, nombre y estadisticas del pokemon ---

                        img,
                        ft.Text(value=pokemon, style=ft.TextStyle(size=20, color="#413942", weight=ft.FontWeight.BOLD)),
                        ft.Text(value=tipo, color="#413942"),
                        ft.Text(value=f"hp: {estadisticas['hp']}", color="#413942"),
                        ft.Text(value=f"attack: {estadisticas['attack']}", color="#413942"),
                        ft.Text(value=f"defense: {estadisticas['defense']}", color="#413942"),
                        ft.Text(value=f"special-attack: {estadisticas['special-attack']}", color="#413942"),
                        ft.Text(value=f"special-defese: {estadisticas['special-defense']}", color="#413942"),
                        ft.Text(value=f"speed: {estadisticas['speed']}", color="#413942")

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),

            actions=[ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [   

                                # --- Boton de regreso ---

                                ft.TextButton(icon=ft.icons.ARROW_BACK_IOS, icon_color="#3E363F", on_click=lambda _: (
                                    setattr(alerta, "open", False),
                                    reestablecer_img_tamano_pokemon(e=None, img=img), # Se reestablece el tamaño de la imagen
                                    page.update()
                                ))

                            ]
                        )
                    ]
                )
            )]
        )

        page.overlay.append(alerta) # Se agrega la alerta a la pagina
        alerta.open = True # Se abre la alerta
        page.update()


    def reestablecer_img_tamano_pokemon(e, img):

        img.width = 100
        img.height = 100

    # --- Funciones de navegacion ---

    def Siguiente(e):

        alerta_cargando(e=None, senal=True)  
        
        time.sleep(0.5)

        nonlocal contador # Variable no local para poder modificarla

        navegar.avanzar()

        contador += 1

        actualizar(e=None)

        time.sleep(0.5)

        alerta_cargando(e=None, senal=False)

    def Retroceder(e):

        nonlocal contador # Variable no local para poder modificarla

        if contador > 0:

            alerta_cargando(e=None, senal=True)

            time.sleep(0.5)

            navegar.retroceder()

            contador -= 1

            actualizar(e=None)

            time.sleep(0.5)

            alerta_cargando(e=None, senal=False)


        else:

            print("La pagina a la que intentas acceder no existe")  

    # ------ Alertas ------

    def alerta_cargando(e, senal):

        if senal == False:

            global alerta # Variable global para poder modificarla

            alerta.open = False # Se cierra la alerta
            page.update()

        else:

            alerta = ft.AlertDialog(
                modal=True,
                bgcolor="#FFFCE8",      
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Text(value="Cargando", style=ft.TextStyle(size=20, color="#413942", weight=ft.FontWeight.BOLD)),
                        ],

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),

                    width=50,
                    height=50,
                    padding=ft.padding.only(top=20)
                )
            )

            page.overlay.append(alerta) # Se agrega la alerta a la pagina
            alerta.open = True # Se abre la alerta
            page.update()

    # ------ Ventanas ------
  
    def ventanas(ruta):

        page.views.clear()
        recorrer_pokemones() # Se recorren los pokemones de la pagina actual
        page.views.append(
            ft.View(
                "/Pokemones",
                [
                    ft.Container(

                        ft.Column(
                            [

                                ft.Container(

                                    ft.Column(
                                        [
                                            ft.Container(

                                                ft.Row(
                                                    [
                                                        ft.Text(value="Poke API")
                                                    ],

                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            )
                                        ]
                                    ),

                                    bgcolor="#DD403A",
                                    padding=ft.padding.only(top=10)
                                ),

                                contenedor_pokemones, # Contenedor de los pokemones

                                ft.Container(
                                    ft.Column(
                                        [

                                            ft.Container(
                                                ft.Row(
                                                    [
                                                        boton_anteror,
                                                        boton_siguiente
                                                    ],

                                                    alignment=ft.MainAxisAlignment.CENTER
                                                )
                                            )
                                        ]
                                    ),

                                    bgcolor="#DD403A"
                                )
                            ],

                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),

                        bgcolor="#413942",
                        margin=ft.margin.only(bottom=10),
                        expand=True,
                        border_radius=20
                    )
                ]
            )
        )

        page.update()

    # ------ Inicializacion ------

    page.on_route_change = ventanas # Se ejecuta la funcion ventanas cuando la ruta cambia
    page.go(page.route)

ft.app(target=main)