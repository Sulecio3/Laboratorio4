import tkinter as tk

class Participante:
    def _init_(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        return self.nombre + " - " + self.institucion

class BandaEscolar(Participante):
    def __init__(self, nombre, institucion, categoria):
        super()._init_(nombre, institucion)
        self._categoria = ""
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria in ["Primaria", "Básico", "Diversificado"]:
            self._categoria = categoria
        else:
            self._categoria = "Inválida"

    def registrar_puntajes(self, puntajes):
        criterios = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]
        if all(crit in puntajes for crit in criterios):
            if all(0 <= puntajes[crit] <= 10 for crit in criterios):
                self._puntajes = puntajes

    @property
    def total(self):
        if self._puntajes:
            return sum(self._puntajes.values())
        return 0

    @property
    def promedio(self):
        if self._puntajes:
            return self.total / len(self._puntajes)
        return 0

    def mostrar_info(self):
        texto = self.nombre + " - " + self.institucion + " | " + self._categoria
        if self._puntajes:
            texto += " | Total: " + str(self.total) + " | Promedio: " + str((self.promedio, 2))
        return texto

class Concurso:
    def _init_(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self, banda):
        if banda.nombre not in self.bandas:
            self.bandas[banda.nombre] = banda

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda in self.bandas:
            self.bandas[nombre_banda].registrar_puntajes(puntajes)

concurso = Concurso("Concurso de Bandas", "2025-09-15")

def inscribir_banda():
    print("Se abrió la ventana: Inscribir Banda")
    ventana_inscribir = tk.Toplevel(ventana)
    ventana_inscribir.title("Inscribir Banda")
    ventana_inscribir.geometry("400x300")

def registrar_evaluacion():
    print("Se abrió la ventana: Registrar Evaluación")
    ventana_eval = tk.Toplevel(ventana)
    ventana_eval.title("Registrar Evaluación")
    ventana_eval.geometry("400x300")

def listar_bandas():
    print("Se abrió la ventana: Listado de Bandas")
    ventana_listado = tk.Toplevel(ventana)
    ventana_listado.title("Listado de Bandas")
    ventana_listado.geometry("400x300")

def ver_ranking():
    print("Se abrió la ventana: Ranking Final")
    ventana_ranking = tk.Toplevel(ventana)
    ventana_ranking.title("Ranking Final")
    ventana_ranking.geometry("400x300")

def salir():
    print("Aplicación cerrada")
    ventana.quit()

ventana = tk.Tk()
ventana.title("Concurso de Bandas - Quetzaltenango")
ventana.geometry("500x300")

barra_menu = tk.Menu(ventana)

menu_opciones = tk.Menu(barra_menu, tearoff=0)
menu_opciones.add_command(label="Inscribir Banda", command=inscribir_banda)
menu_opciones.add_command(label="Registrar Evaluación", command=registrar_evaluacion)
menu_opciones.add_command(label="Listar Bandas", command=listar_bandas)
menu_opciones.add_command(label="Ver Ranking", command=ver_ranking)
menu_opciones.add_separator()
menu_opciones.add_command(label="Salir", command=salir)

barra_menu.add_cascade(label="Opciones", menu=menu_opciones)

ventana.config(menu=barra_menu)

etiqueta = tk.Label(
    ventana,
    text="Sistema de Inscripción y Evaluación de Bandas Escolares\nDesfile 15 de Septiembre - Quetzaltenango",
    font=("Arial", 12, "bold"),
    justify="center"
)
etiqueta.pack(pady=50)

ventana.mainloop()
