# EVALUEITOR

Simulador de parcial para la asignatura de Diseno y Analisis de Algoritmos.
Hecho por un estudiante, para estudiantes. Sin IA, sin servidor, sin cuenta.
Este simulador trata de problemas random sobre el 1er y 2do parcial, donde solo tenes que identificar el algoritmo del problema y ponerlo, del cual si esta correcto, te dara por OK, sino KO, pasando un par de pruebas.

## Requisitos

- Python 3.8 o superior
- Windows (probado en Windows 10/11)
- No he testeado para Linux, aunque se me ocurrio hacerle un MakeFile, pero preferi .bat xD.

## Instalacion

Clona el repositorio y ejecuta el setup una sola vez:

    git clone https://github.com/TU_USUARIO/UR_evalueitor_app.git
    cd UR_evalueitor_app
    setup.bat

Esto crea un entorno virtual e instala las dependencias automaticamente.

## Uso

Para iniciar el examen:

    run.bat

Al arrancar la app:

1. Elige el modo de examen: Parcial 1, Parcial 2 o Modo Libre
2. Se generan 5 problemas aleatorios en la carpeta entregable/
3. Abre tu editor (VS Code, PyCharm...) y edita los archivos:
   - entregable/ex00/ex00.py
   - entregable/ex01/ex01.py
   - entregable/ex02/ex02.py
   - entregable/ex03/ex03.py
   - entregable/ex04/ex04.py
4. Lee el enunciado en la interfaz o en entregable/exXX/enunciado.txt
5. Escribe SOLO las funciones del algoritmo, sin main() ni input()
6. Pulsa el boton de evaluar para ver si pasas los tests
7. Las trazas de error se guardan en trazas/exXX.txt
8. Al terminar pulsa Entregar o Rendirse para ver las soluciones del profesor

## Normas

- Tiempo: 1 hora 30 minutos
- 5 problemas aleatorios por examen
- Escribe solo el algoritmo, sin main() ni input()
- Si incluyes main() o input() en tu codigo -> KO automatico
- Salir de la ventana durante el examen queda registrado como infraccion
- Las soluciones del profesor solo se muestran al entregar o rendirse
- Cada ejercicio vale 20 puntos. Se necesita un 60% para aprobar

## Estructura del proyecto

    evalueitor/
    ├── grademe.py          - App principal, ejecuta esto con run.bat
    ├── evaluator.py        - Motor de tests y comparacion con el profesor
    ├── antitramp.py        - Sistema anti-trampa
    ├── requirements.txt    - Dependencias
    ├── setup.bat           - Instalacion del entorno virtual
    ├── run.bat             - Ejecutar el examen
    ├── problems/           - Banco de problemas (no modificar)
    │   ├── ex00_bfs/
    │   ├── ex01_dfs/
    │   └── ...
    ├── entregable/         - Tus soluciones (se genera al iniciar el examen)
    └── trazas/             - Errores de cada test (se genera al evaluar)

## Añadir problemas

Para añadir un nuevo problema crea una carpeta en problems/ con esta estructura:

    problems/mi_algoritmo/
    ├── enunciado.txt
    ├── test_runner.py
    ├── test00.in
    ├── test00.out
    ├── test01.in
    ├── test01.out
    └── solutions/
        ├── solution_prof.py
        ├── solution_alt1.py
        └── solution_alt2.py

El test_runner.py importa el archivo del estudiante y llama a sus funciones directamente.
Ver cualquier test_runner.py existente como referencia.

## Algoritmos incluidos

#### Parcial 1 - Grafos y Greedy
##### Suele caer 2 de los siguientes, darle prioridad.
- BFS, DFS, Dijkstra, Prim, Kruskal
- TopSort, Lexical TopSort, Art Points


##### Suele caer 1 mayormente, algunas veces 2.

- Scheduling, Waiting Time, Coin Exchange
- Greedy Knapsack



#### Parcial 2 - Divide y Venceras y Backtracking

##### Suele caer uno de ellos, porque evalua todo el temario.
- BFS, DFS, Dijkstra, Prim, Kruskal
- Scheduling, Waiting Time, Coin Exchange, Greedy Knapsack
- TopSort, Lexical TopSort, Art Points


##### Darle prioridad a lo siguiente, caen 2 prob.
- Merge Sort, Quick Sort, Max Vector
- Mochila 0/1 BT, N-Queens
- Binary Search recursivo e iterativo
- Coloreo de Grafos

## Contribuir

> Este proyecto esta bajo una licencia restrictiva.
> Se permite su ejecucion para fines de evaluacion academica,
> pero esta prohibida su copia, modificacion sin
> autorizacion del autor.
> Contacto: LinkedIn - Sergio Alejandro
