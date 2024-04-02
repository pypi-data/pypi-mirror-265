# Hack4u Academy Python Library

Libreria para consultar cursos de la academia Hack4u.

## Cursos disponibles.

- Introducción a Linux [15 horas]
- Personalización de entorno en Linux [3 horas]
- Python Ofensivo [35 horas]
- Introducción al Hacking [53 horas]

## Instalación 

Instala el paquete con el gestor de paquetes `pip3`:

```python3
pip3 install hack4u_promixion
```

## Uso básico

### Listar todos los cursos

```python 
from hack4u_promixion import listarCursos

listarCursos()
```

### Listar curso por nombre

```python
from hack4u_promixion import listarCursoPorNombre

listarCursoPorNombre("Introducción a Linux")
```

### Calcular duración total de los cursos

```python3
from hack4u_promixion import duracionTotal 

print(f"La duración total de los cursos es de {duracionTotal()} horas.")
```




