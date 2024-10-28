import time
from gramatica_cfg import GramaticaCFG
from algoritmo_cyk import cyk
from cfg_to_cnf import CFGtoCNF

def format_parse_tree(tree, indent=0):
    if isinstance(tree, tuple):
        if len(tree) == 3:  # Node with two children
            root, left, right = tree
            result = "    " * indent + f"{root} ->\n"
            result += format_parse_tree(left, indent + 1)
            result += format_parse_tree(right, indent + 1)
            return result
        elif len(tree) == 2:  # Node with one child (terminal)
            root, value = tree
            return "    " * indent + f"{root} -> '{value}'\n"
    return ""

def main():
    gramatica = GramaticaCFG()
    
    # Convert grammar to CNF before processing
    converter = CFGtoCNF()
    print("\nGramática original:")
    for left, right_list in gramatica.producciones.items():
        for right in right_list:
            print(f"{left} -> {' '.join(right)}")
    
    # Convert to CNF
    cnf_grammar = converter.convert(gramatica.producciones)
    gramatica.produccionescle = cnf_grammar
    
    print("\nGramática en Forma Normal de Chomsky:")
    for left, right_list in cnf_grammar.items():
        for right in right_list:
            print(f"{left} -> {' '.join(right)}")
    
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

            print(f"La frase '{frase}' {'sí' if pertenece else 'no'} pertenece al lenguaje.")
            print(f"Tiempo de ejecución: {tiempo:.2f} ms")
            
            if pertenece:
                print("Parse Trees:")
                formatted_tree = format_parse_tree(arbol)
                print(formatted_tree)
            print()

if __name__ == "__main__":
    main()
