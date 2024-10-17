class GramaticaCFG:
    def __init__(self):
        self.producciones = {
            'S': [['NP', 'VP']],
            'VP': [['V', 'NP'], ['VP', 'PP']],
            'PP': [['P', 'NP']],
            'NP': [['Det', 'N'], ['he'], ['she']],
            'V': [['cooks'], ['drinks'], ['eats'], ['cuts']],
            'P': [['in'], ['with']],
            'N': [['cat'], ['dog'], ['beer'], ['cake'], ['juice'], ['meat'], ['soup'], ['fork'], ['knife'], ['oven'], ['spoon'], ['water']],
            'Det': [['a'], ['the']]
        }

    def simbolos_no_terminales(self):
        return list(self.producciones.keys())

    def simbolos_terminales(self):
        terminales = set()
        for producciones in self.producciones.values():
            for produccion in producciones:
                for simbolo in produccion:
                    if simbolo not in self.producciones:
                        terminales.add(simbolo)
        return list(terminales)
