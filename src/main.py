import time
from gramatica_cfg import GramaticaCFG
from algoritmo_cyk import cyk

def main():
    gramatica = GramaticaCFG()

    print("1. Ejemplos de cadenas aceptadas semánticamente correctas:")
    frases_correctas = [
        "She eats a cake with a fork",
        "The dog drinks the water",
        "He cuts the meat with a knife",
        "The cat drinks juice",
        "The cook eats a soup"
    ]

    print("\n2. Ejemplos de cadenas aceptadas semánticamente incorrectas:")
    frases_incorrectas_semanticamente = [
        "The fork eats the dog",
        "He drinks the knife",
        "The spoon cuts the cake",
        "She drinks the meat",
        "The oven eats the soup"
    ]

    print("\n3. Ejemplos de cadenas no aceptadas por la gramática:")
    frases_no_aceptadas = [
        "The cat the dog",
        "Eats quickly she",
        "Drinks the water cake",
        "The water dog with eats",
        "A drinks cake the"
    ]

    todas_las_frases = frases_correctas + frases_incorrectas_semanticamente + frases_no_aceptadas

    for i, grupo_frases in enumerate([frases_correctas, frases_incorrectas_semanticamente, frases_no_aceptadas], 1):
        print(f"\nGrupo {i}:")
        for frase in grupo_frases:
            inicio = time.time()
            pertenece, arbol = cyk(frase, gramatica)
            fin = time.time()
            tiempo = (fin - inicio) * 1000
  # Convertir a milisegundos

            print(f"La frase '{frase}' {'sí' if pertenece else 'no'} pertenece al lenguaje.")
            print(f"Tiempo de ejecución: {tiempo:.2f} ms")
            
            if pertenece:
                print("Árbol de análisis sintáctico:")
                print(arbol)
            print()

if __name__ == "__main__":
    main()
