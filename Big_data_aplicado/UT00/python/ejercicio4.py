asignaturas = {
    "Matemáticas": ["Ana", "Carlos", "Luis", "María", "Jorge"],
    "Física": ["Elena", "Luis", "Juan", "Sofía"],
    "Programación": ["Ana", "Carlos", "Sofía", "Jorge", "Pedro"],
    "Historia": ["María", "Juan", "Elena", "Ana"],
    "Inglés": ["Carlos", "Sofía", "Jorge", "María"],
}

salir = False
while not salir:
    print("1. Listar estudiantes de una asignatura")
    print("2. Matricular estudiante")
    print("3. Dar de baja a un estudiante")
    print("4- Salir")
    op = input("Seleccione una opción: ")

    match op:
        case "1":
            asig =input("Introduzca la asignatura: ")
            alumnos = asignaturas.get(asig)
            for a in alumnos:
                print( f" {a}")

        case "2":
            alumno = input("Introduzca el nombre del estudiante: ")
            asig = input("Introduzca el nombre de la asignatura: ")
            if asig in asignaturas:
                asignaturas[asig].append(alumno)
            else:
                asignaturas[asig] = [alumno]
        
        case "3":
            alumno = input("Introduzca el nombre del estudiante a dar de baja: ")
            asig = input("Introduzca el nombre de la asignaturas a dar de bajo: ")
            asignaturas[asig].remove(alumno)

        case _:
            salir = True
