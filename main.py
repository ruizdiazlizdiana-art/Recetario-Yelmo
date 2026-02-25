from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import os

# Interfaz gráfica (Kivy Language)
KV = '''
ScreenManager:
    MenuScreen:
    VerScreen:
    AgregarScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 0.97, 0.86, 1  # Color crema
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: '🍞 Mis Recetas Yelmo 🍞'
            font_size: '24sp'
            color: 0.54, 0.27, 0.07, 1
            size_hint_y: 0.15
        ScrollView:
            BoxLayout:
                id: lista_recetas
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
        Button:
            text: '➕ Agregar Receta'
            size_hint_y: 0.15
            background_color: 0.6, 0.98, 0.6, 1
            on_release: app.root.current = 'agregar'

<VerScreen>:
    name: 'ver'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 0.97, 0.86, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            id: titulo_receta
            text: 'Título'
            font_size: '22sp'
            color: 0.54, 0.27, 0.07, 1
            size_hint_y: 0.1
        ScrollView:
            Label:
                id: texto_receta
                text: 'Contenido...'
                color: 0, 0, 0, 1
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        BoxLayout:
            size_hint_y: 0.15
            spacing: 10
            Button:
                text: '⬅ Volver'
                on_release: app.root.current = 'menu'
            Button:
                text: '❌ Borrar'
                background_color: 1, 0.6, 0.6, 1
                on_release: app.borrar_receta()

<AgregarScreen>:
    name: 'agregar'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 0.97, 0.86, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Nueva Receta'
            font_size: '22sp'
            color: 0.54, 0.27, 0.07, 1
            size_hint_y: 0.1
        TextInput:
            id: input_titulo
            hint_text: 'Nombre del pan...'
            size_hint_y: 0.1
        TextInput:
            id: input_contenido
            hint_text: 'Ingredientes y pasos...'
        BoxLayout:
            size_hint_y: 0.15
            spacing: 10
            Button:
                text: 'Cancelar'
                on_release: app.root.current = 'menu'
            Button:
                text: '💾 Guardar'
                background_color: 0.6, 0.98, 0.6, 1
                on_release: app.guardar_receta()
'''

class MenuScreen(Screen): pass
class VerScreen(Screen): pass
class AgregarScreen(Screen): pass

class RecetarioApp(App):
    def build(self):
        # Archivo donde se guarda la data en el celular
        self.ruta_datos = os.path.join(self.user_data_dir, 'mis_recetas.json')
        self.recetas = self.cargar_datos()
        
        # Si está vacío, cargamos 3 básicas
        if not self.recetas:
            self.recetas = {
                "Pan Blanco Nube Real": "1 kg\n- Leche en polvo\n- Aceite\n- 12g levadura fresca\nPrograma: Básico",
                "Pan Integral Malta": "1 kg\n- Leche\n- Malta y miel\n- 12g levadura fresca\nPrograma: Integral",
                "Masa Pizza Integral": "Masa básica\nPrograma: Función 10 (Masa)"
            }
            self.guardar_datos()

        self.sm = Builder.load_string(KV)
        return self.sm

    def on_start(self):
        self.actualizar_lista()

    def cargar_datos(self):
        if os.path.exists(self.ruta_datos):
            with open(self.ruta_datos, 'r') as f:
                return json.load(f)
        return {}

    def guardar_datos(self):
        with open(self.ruta_datos, 'w') as f:
            json.dump(self.recetas, f)

    def actualizar_lista(self):
        caja_lista = self.sm.get_screen('menu').ids.lista_recetas
        caja_lista.clear_widgets()
        from kivy.uix.button import Button
        for titulo in self.recetas.keys():
            btn = Button(text=titulo, size_hint_y=None, height=120, background_color=(0.96, 0.87, 0.7, 1), color=(0,0,0,1))
            btn.bind(on_release=lambda instance, t=titulo: self.ver_receta(t))
            caja_lista.add_widget(btn)

    def ver_receta(self, titulo):
        pantalla_ver = self.sm.get_screen('ver')
        pantalla_ver.ids.titulo_receta.text = titulo
        pantalla_ver.ids.texto_receta.text = self.recetas[titulo]
        self.receta_actual = titulo
        self.sm.current = 'ver'

    def guardar_receta(self):
        pantalla_agregar = self.sm.get_screen('agregar')
        titulo = pantalla_agregar.ids.input_titulo.text
        contenido = pantalla_agregar.ids.input_contenido.text
        if titulo and contenido:
            self.recetas[titulo] = contenido
            self.guardar_datos()
            self.actualizar_lista()
            pantalla_agregar.ids.input_titulo.text = ''
            pantalla_agregar.ids.input_contenido.text = ''
            self.sm.current = 'menu'

    def borrar_receta(self):
        if self.receta_actual in self.recetas:
            del self.recetas[self.receta_actual]
            self.guardar_datos()
            self.actualizar_lista()
            self.sm.current = 'menu'

if __name__ == '__main__':
    RecetarioApp().run()
