import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Contraseña por defecto en WAMP
    database="calificaciones_escuela"
)
cursor = conn.cursor()

# Asignaturas por semestre
asignaturas_por_semestre = {
    1: ["CALCULO DIFERENCIAL", "FUNDAMENTOS DE PROGRAMACIÓN", "TALLER DE ETICA", "MATEMATICAS DISCRETAS", "TALLER DE ADMINISTRACION", "FUNDAMENTOS DE INVESTIGACION"],
    2: ["CALCULO INTEGRAL", "PROGRAMACION ORIENTADA A OBJETOS", "CONTABILIDAD FINANCIERA", "QUIMICA", "ALGEBRA LINEAL", "PROBABILIDAD Y ESTADISTICA"],
    3: ["CALCULO VECTORIAL", "ESTRUCTURA DE DATOS", "CULTURA EMPRESARIAL", "INVESTIGACION DE OPERACIONES", "DESARROLLO SUSTENTABLE", "FISICA GENERAL"],
    4: ["ECUACIONES DIFERENCIALES", "METODOS NUMERICOS", "TOPICOS AVANZADOS DE PROGRAMACION", "FUNDAMENTOS DE BASE DE DATOS", "SIMULACION", "PRINCIPIOS ELECTRICOS Y APLICACIONES DIGITALES"],
    5: ["GRAFICACION", "FUNDAMENTOS DE TELECOMUNICACIONES", "SISTEMAS OPERATIVOS", "TALLER DE BASE DE DATOS", "FUNDAMENTOS DE INGENIERIA DE SOFTWARE", "ARQUITECTURA DE COMPUTADORAS"],
    6: ["LENGUAJES Y AUTOMATAS", "REDES DE COMPUTADORAS", "TALLER DE SISTEMAS OPERATIVOS", "ADMINISTRACIÓN DE BASE DE DATOS", "INGENIERIA DE SOFTWARE", "LENGUAJE DE INTERFAZ"],
    7: ["LENGUAJES Y AUTOMATAS II", "CONMUTACION Y ENRUTAMIENTO DE REDES DE DATOS", "TALLER DE INVESTIGACION I", "GESTION DE PROYECTOS DE SOFTWARE", "SISTEMAS PROGRAMABLES", "CIBERSEGURIDAD"],
    8: ["PROGRAMACION LOGICA Y FUNCIONAL", "ADMINISTRACION DE REDES", "TALLER DE INVESTIGACION II", "PROGRAMACION WEB", "ANÁLISIS Y MODELADO DE DATOS", "SISTEMAS AUTONOMOS"],
    9: ["INTELIGENCIA ARTIFICIAL", "RESIDENCIA PROFESIONAL", "SERVICIO SOCIAL", "REDES NEURONALES ARTIFICIALES", "ALGORITMOS EVOLUTIVOS"]
}

def registrar_alumno():
    nombre = input("Ingrese el nombre del alumno: ")
    semestre = int(input("Ingrese el semestre (1-9): "))
    if 1 <= semestre <= 9:
        cursor.execute("INSERT INTO alumno (nombre, semestre) VALUES (%s, %s)", (nombre, semestre))
        conn.commit()
        print(f"Alumno '{nombre}' registrado.")
    else:
        print("Semestre inválido.")

def registrar_calificaciones():
    nombre = input("Ingrese el nombre del alumno: ")
    cursor.execute("SELECT id, semestre FROM alumno WHERE nombre = %s", (nombre,))
    alumno = cursor.fetchone()
    if not alumno:
        print("Alumno no encontrado.")
        return
    semestre = alumno[1]
    asignaturas = asignaturas_por_semestre.get(semestre, [])
    for asignatura in asignaturas:
        while True:
            try:
                calificacion = int(input(f"{asignatura} (0-10): "))
                if 0 <= calificacion <= 10:
                    break
                else:
                    print("Debe ser de 0 a 10.")
            except ValueError:
                print("Ingrese un número válido.")
        cursor.execute("INSERT INTO calificacion (alumno_id, asignatura, calificacion) VALUES (%s, %s, %s)", 
                       (alumno[0], asignatura, calificacion))
        conn.commit()
    print("Calificaciones registradas.")

def consultar_alumno():
    nombre = input("Ingrese el nombre del alumno: ")
    cursor.execute("SELECT id FROM alumno WHERE nombre = %s", (nombre,))
    alumno = cursor.fetchone()
    if not alumno:
        print("Alumno no encontrado.")
        return
    cursor.execute("SELECT calificacion FROM calificacion WHERE alumno_id = %s", (alumno[0],))
    calificaciones = [c[0] for c in cursor.fetchall()]
    if not calificaciones:
        print("No tiene calificaciones.")
        return
    estado = "regular" if all(c >= 7 for c in calificaciones) else "irregular"
    print(f"Alumno {estado}.")

def consultar_reprobados():
    semestre = input("Semestre (1-9) o 'todos': ")
    if semestre.lower() == "todos":
        cursor.execute("SELECT COUNT(DISTINCT alumno_id) FROM calificacion WHERE calificacion < 7")
        print("Total reprobados:", cursor.fetchone()[0])
    else:
        try:
            semestre = int(semestre)
            cursor.execute("""
                SELECT COUNT(DISTINCT c.alumno_id)
                FROM calificacion c
                INNER JOIN alumno a ON c.alumno_id = a.id
                WHERE a.semestre = %s AND c.calificacion < 7
            """, (semestre,))
            print(f"Reprobados en semestre {semestre}: {cursor.fetchone()[0]}")
        except:
            print("Entrada inválida.")

def ver_status_alumno():
    nombre = input("Ingrese el nombre del alumno: ")
    cursor.execute("SELECT id FROM alumno WHERE nombre = %s", (nombre,))
    alumno = cursor.fetchone()
    if not alumno:
        print("Alumno no encontrado.")
        return
    cursor.execute("SELECT calificacion FROM calificacion WHERE alumno_id = %s", (alumno[0],))
    calificaciones = [c[0] for c in cursor.fetchall()]
    if not calificaciones:
        print("Sin calificaciones.")
        return
    promedio = sum(calificaciones) / len(calificaciones)
    if 7 <= promedio < 8:
        status = "Aceptable"
    elif 8 <= promedio < 9:
        status = "Bueno"
    elif 9 <= promedio <= 10:
        status = "Excelente"
    else:
        status = "Insuficiente"
    print(f"Promedio: {promedio:.2f} → Desempeño: {status}")

def menu():
    while True:
        print("\n📚 Menú Académico")
        print("1. Registrar Alumno")
        print("2. Registrar Calificaciones")
        print("3. Consultar Alumno (Regular/Irregular)")
        print("4. Consultar Reprobados")
        print("5. Ver Status de Alumno")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_alumno()
        elif opcion == "2":
            registrar_calificaciones()
        elif opcion == "3":
            consultar_alumno()
        elif opcion == "4":
            consultar_reprobados()
        elif opcion == "5":
            ver_status_alumno()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

menu()
conn.close()