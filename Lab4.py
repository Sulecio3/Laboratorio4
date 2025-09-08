import tkinter as tk
class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        return self.nombre + " - " + self.institucion


class BandaEscolar(Participante):
    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = ""
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        categoria = categoria.strip().lower()
        categoria = categoria.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

        categorias_validas = {
            "primaria": "Primaria",
            "basico": "Básico",
            "diversificado": "Diversificado"
        }

        if categoria in categorias_validas:
            self._categoria = categorias_validas[categoria]
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
            texto += " | Total: " + str(self.total) + " | Promedio: " + str(round(self.promedio, 2))
        return texto


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self, banda):
        if banda._categoria == "Inválida":
            return "Categoría inválida"
        if banda.nombre in self.bandas:
            return "Ya existe una banda con ese nombre"
        self.bandas[banda.nombre] = banda
        return "Banda inscrita con éxito"

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda in self.bandas:
            self.bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        print("\n Listado de bandas")
        for clave, valor in self.bandas.items():
            print(clave, valor)

    def ranking(self):
        ranking_ordenado = sorted(self.bandas.items(),key=lambda item: item[1].total, reverse=True)
        for i, (nombre_banda, puntaje) in enumerate(ranking_ordenado):
            print(f"- {i} Banda: {nombre_banda}, puntaje: {puntaje} ")


concurso = Concurso("Concurso de Bandas", "2025-09-15")


def inscribir_banda():
    ventana_inscribir = tk.Toplevel(ventana)
    ventana_inscribir.title("Inscribir Banda")
    ventana_inscribir.geometry("400x300")

    tk.Label(ventana_inscribir, text="Nombre de la Banda:").pack()
    entry_nombre = tk.Entry(ventana_inscribir)
    entry_nombre.pack()

    tk.Label(ventana_inscribir, text="Institución:").pack()
    entry_institucion = tk.Entry(ventana_inscribir)
    entry_institucion.pack()

    tk.Label(ventana_inscribir, text="Categoría (Primaria, Básico, Diversificado):").pack()
    entry_categoria = tk.Entry(ventana_inscribir)
    entry_categoria.pack()

    mensaje = tk.Label(ventana_inscribir, text="")
    mensaje.pack()

    def guardar_banda():
        nombre = entry_nombre.get().strip()
        institucion = entry_institucion.get().strip()
        categoria = entry_categoria.get().strip()

        if nombre and institucion and categoria:
            banda = BandaEscolar(nombre, institucion, categoria)
            resultado = concurso.inscribir_banda(banda)
            if "éxito" in resultado:
                mensaje.config(text=resultado, fg="green")
            else:
                mensaje.config(text=resultado, fg="red")
        else:
            mensaje.config(text="Complete todos los campos", fg="red")

    tk.Button(ventana_inscribir, text="Guardar", command=guardar_banda).pack(pady=10)


def registrar_evaluacion():
    ventana_eval = tk.Toplevel(ventana)
    ventana_eval.title("Registrar Evaluación")
    ventana_eval.geometry("400x400")

    tk.Label(ventana_eval, text="Nombre de la Banda:").pack()
    entry_nombre = tk.Entry(ventana_eval)
    entry_nombre.pack()

    criterios = ["ritmo", "uniformidad", "coreografía", "alineación", "puntualidad"]
    entradas = {}
    for crit in criterios:
        tk.Label(ventana_eval, text=crit + ":").pack()
        entrada = tk.Entry(ventana_eval)
        entrada.pack()
        entradas[crit] = entrada

    mensaje = tk.Label(ventana_eval, text="")
    mensaje.pack()

    def guardar_evaluacion():
        nombre = entry_nombre.get().strip()
        puntajes = {}
        try:
            for crit in criterios:
                valor = int(entradas[crit].get())
                if 0 <= valor <= 10:
                    puntajes[crit] = valor
                else:
                    raise ValueError
        except ValueError:
            mensaje.config(text="Todos los puntajes deben ser números entre 0 y 10", fg="red")
            return

        if nombre in concurso.bandas:
            concurso.registrar_evaluacion(nombre, puntajes)
            mensaje.config(text="Evaluación guardada con éxito", fg="green")
        else:
            mensaje.config(text="Banda no encontrada", fg="red")

    tk.Button(ventana_eval, text="Guardar Evaluación", command=guardar_evaluacion).pack(pady=10)

def listar_bandas():
    ventana_listar = tk.Toplevel(ventana)
    ventana_listar.title("Listado de Bandas")
    ventana_listar.geometry("400x400")

    mensaje = tk.Label(ventana_listar, text="")
    mensaje.pack(pady=10)

    texto = ""
    if concurso.bandas:
        for banda in concurso.bandas.values():
            texto += banda.mostrar_info() + "\n"
        mensaje.config(text=texto)
    else:
        mensaje.config(text="No hay bandas inscritas")

def ranking():
    ventana_ranking = tk.Toplevel(ventana)
    ventana_ranking.title("Ranking de bandas")
    ventana_ranking.geometry("400x400")

    mensaje = tk.Label(ventana_ranking, text="")
    mensaje.pack(pady=50)

    if not concurso.bandas:
        mensaje.config(text="No existen bandas inscritas")
        return

    ranking_ordenado = sorted(concurso.bandas.items(), key=lambda item: item[1].total, reverse=True)
    texto = ""
    for i, (nombre_banda, banda) in enumerate(ranking_ordenado, start=1):
        texto += f"- {i}, Banda: {nombre_banda}, Puntaje: {banda.total}\n"

    mensaje.config(text=texto)



ventana = tk.Tk()
ventana.title("Concurso de Bandas - Quetzaltenango")
ventana.geometry("500x300")

barra_menu = tk.Menu(ventana)
menu_opciones = tk.Menu(barra_menu, tearoff=0)
menu_opciones.add_command(label="Inscribir Banda", command=inscribir_banda)
menu_opciones.add_command(label="Registrar Evaluación", command=registrar_evaluacion)
menu_opciones.add_command(label="Listado de bandas", command=listar_bandas)
menu_opciones.add_command(label="Mostrar ranking", command=ranking)
menu_opciones.add_separator()
menu_opciones.add_command(label="Salir", command=ventana.quit)
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
