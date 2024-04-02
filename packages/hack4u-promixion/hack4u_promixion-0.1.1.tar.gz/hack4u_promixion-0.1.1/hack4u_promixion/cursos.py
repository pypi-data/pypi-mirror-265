class Cursos:

    def __init__(self, nombre, duracion, link):

        self.nombre = nombre
        self.duracion = duracion
        self.link = link

    def __repr__(self):

        return f"El curso '{self.nombre}', tiene una duración de [{self.duracion}] horas ({self.link})"

cursos = [
        Cursos("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
        Cursos("Personalización de entorno en Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
        Cursos("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/"),
        Cursos("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def listarCursos():

    for curso in cursos:
        print(curso)

def listarCursoPorNombre(nombre):

    for curso in cursos:
        if curso.nombre == nombre:
            return curso

    return None




