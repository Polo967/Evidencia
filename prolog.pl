% --- Hechos: alumnos registrados ---
% alumno(Nombre, Semestre).
alumno(juan, 1).
alumno(ana, 3).
alumno(carlos, 3).

% --- Hechos: asignaturas por semestre ---
% asignatura(Semestre, NombreAsignatura).
asignatura(1, 'CALCULO DIFERENCIAL').
asignatura(1, 'FUNDAMENTOS DE PROGRAMACIÓN').
asignatura(3, 'CALCULO VECTORIAL').
asignatura(3, 'ESTRUCTURA DE DATOS').

% --- Hechos: calificaciones por alumno ---
% calificacion(NombreAlumno, Asignatura, Calificacion).
calificacion(juan, 'CALCULO DIFERENCIAL', 9).
calificacion(juan, 'FUNDAMENTOS DE PROGRAMACIÓN', 8).
calificacion(ana, 'CALCULO VECTORIAL', 6).
calificacion(ana, 'ESTRUCTURA DE DATOS', 7).
calificacion(carlos, 'CALCULO VECTORIAL', 10).
calificacion(carlos, 'ESTRUCTURA DE DATOS', 9).

% --- Reglas para saber si un alumno es regular ---
regular(Nombre) :-
    alumno(Nombre, _),
    findall(C, calificacion(Nombre, _, C), Calificaciones),
    Calificaciones \= [],
    forall(member(C, Calificaciones), C >= 7).

irregular(Nombre) :-
    alumno(Nombre, _),
    findall(C, calificacion(Nombre, _, C), Calificaciones),
    Calificaciones \= [],
    member(C, Calificaciones),
    C < 7.

% --- Regla para calcular promedio ---
promedio(Nombre, Promedio) :-
    findall(C, calificacion(Nombre, _, C), Calificaciones),
    Calificaciones \= [],
    sumlist(Calificaciones, Suma),
    length(Calificaciones, Total),
    Promedio is Suma / Total.

% --- Clasificación del desempeño del alumno ---
desempeno(Nombre, 'Excelente') :-
    promedio(Nombre, P), P >= 9, P =< 10.
desempeno(Nombre, 'Bueno') :-
    promedio(Nombre, P), P >= 8, P < 9.
desempeno(Nombre, 'Aceptable') :-
    promedio(Nombre, P), P >= 7, P < 8.
desempeno(Nombre, 'Insuficiente') :-
    promedio(Nombre, P), P < 7.

% --- Reprobados por semestre ---
reprobado_en_semestre(Semestre, Nombre) :-
    alumno(Nombre, Semestre),
    calificacion(Nombre, _, C),
    C < 7.
