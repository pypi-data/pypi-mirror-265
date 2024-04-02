from .cursos import cursos

def duracionTotal():

    return sum(curso.duracion for curso in cursos)


