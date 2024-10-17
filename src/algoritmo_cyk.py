def cyk(frase, gramatica):
    palabras = frase.lower().split()
    n = len(palabras)
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    # Inicializar la tabla con las palabras de entrada
    for i, palabra in enumerate(palabras):
        for no_terminal, producciones in gramatica.producciones.items():
            if [palabra] in producciones:
                tabla[i][i].add((no_terminal, palabra))

    # Llenar la tabla
    for longitud in range(2, n + 1):
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            for k in range(i, j):
                for no_terminal, producciones in gramatica.producciones.items():
                    for produccion in producciones:
                        if len(produccion) == 2:
                            B, C = produccion
                            for b in tabla[i][k]:
                                if b[0] == B:
                                    for c in tabla[k+1][j]:
                                        if c[0] == C:
                                            tabla[i][j].add((no_terminal, b, c))

    # Construir el árbol de análisis sintáctico
    def construir_arbol(celda):
        if isinstance(celda[1], str):
            return celda
        return (celda[0], construir_arbol(celda[1]), construir_arbol(celda[2]))

    # Verificar si el símbolo inicial está en la celda superior derecha
    for item in tabla[0][n-1]:
        if item[0] == 'S':
            return True, construir_arbol(item)
    
    return False, None
