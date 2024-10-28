class CFGtoCNF:
    def __init__(self):
        self.new_var_counter = 0
        self.unit_productions = set()
        self.result_productions = {}

    def _generate_new_var(self):
        """Generate a new unique variable name."""
        self.new_var_counter += 1
        return f"X{self.new_var_counter}"

    def _eliminate_epsilon_productions(self, productions):
        """Eliminate ε-productions (A -> ε)."""
        result = productions.copy()
        nullable = set()
        
        # Find all nullable variables
        changed = True
        while changed:
            changed = False
            for left, right_list in result.items():
                if left not in nullable:
                    for right in right_list:
                        if len(right) == 0 or all(symbol in nullable for symbol in right):
                            nullable.add(left)
                            changed = True
                            break

        # Generate new productions without nullable variables
        new_productions = {}
        for left, right_list in result.items():
            new_productions[left] = []
            for right in right_list:
                if len(right) > 0:  # Skip ε-productions
                    # Generate all possible combinations without nullable variables
                    combinations = [[]]
                    for symbol in right:
                        new_combinations = []
                        for combo in combinations:
                            new_combinations.append(combo + [symbol])
                            if symbol in nullable:
                                new_combinations.append(combo)
                        combinations = new_combinations
                    
                    # Add all non-empty combinations
                    for combo in combinations:
                        if combo and combo not in new_productions[left]:
                            new_productions[left].append(combo)

        return new_productions

    def _eliminate_unit_productions(self, productions):
        """Eliminate unit productions (A -> B)."""
        result = {left: [] for left in productions}
        self.unit_productions = set()
        
        # Collect all unit productions
        for left, right_list in productions.items():
            for right in right_list:
                if len(right) == 1 and isinstance(right[0], str) and right[0].isupper():
                    self.unit_productions.add((left, right[0]))
                else:
                    result[left].append(right)

        # Find transitive closure
        changed = True
        while changed:
            changed = False
            new_units = set()
            for a, b in self.unit_productions:
                for c, d in self.unit_productions:
                    if b == c and (a, d) not in self.unit_productions:
                        new_units.add((a, d))
                        changed = True
            self.unit_productions.update(new_units)

        # Replace unit productions
        for (left, right) in self.unit_productions:
            if right in productions:
                for prod in productions[right]:
                    if prod not in result[left]:
                        result[left].append(prod)

        return result

    def _convert_terminal_productions(self, productions):
        """Convert productions with mixed terminals and non-terminals."""
        result = productions.copy()
        terminal_vars = {}
        
        for left, right_list in list(productions.items()):
            new_right_list = []
            for right in right_list:
                new_right = []
                needs_conversion = False
                
                # Check if production needs conversion
                if len(right) >= 2 and left != "Det":  # Avoid conversion for 'Det'
                    for symbol in right:
                        if not isinstance(symbol, str) or (isinstance(symbol, str) and not symbol.isupper()):
                            needs_conversion = True
                            break
                
                if needs_conversion:
                    for symbol in right:
                        if not isinstance(symbol, str) or (isinstance(symbol, str) and not symbol.isupper()):
                            if symbol not in terminal_vars:
                                new_var = self._generate_new_var()
                                terminal_vars[symbol] = new_var
                                result[new_var] = [[symbol]]
                            new_right.append(terminal_vars[symbol])
                        else:
                            new_right.append(symbol)
                    new_right_list.append(new_right)
                else:
                    new_right_list.append(right)
            
            result[left] = new_right_list
        
        return result

    def _break_long_productions(self, productions):
        """Break productions with more than two symbols on the right-hand side."""
        result = {left: [] for left in productions}
        
        for left, right_list in productions.items():
            for right in right_list:
                if len(right) > 2:
                    # Create new variables and break the production
                    current_left = left
                    remaining = right[:]
                    while len(remaining) > 2:
                        new_var = self._generate_new_var()
                        result[current_left].append([remaining[0], new_var])
                        current_left = new_var
                        remaining = remaining[1:]
                    result[current_left].append(remaining)
                else:
                    result[left].append(right)
        
        return result

    def convert(self, productions):
        """Convert CFG to CNF."""
        # Step 1: Eliminate ε-productions
        result = self._eliminate_epsilon_productions(productions)
        
        # Step 2: Eliminate unit productions
        result = self._eliminate_unit_productions(result)
        
        # Step 3: Convert productions with terminals
        result = self._convert_terminal_productions(result)
        
        # Step 4: Break long productions
        result = self._break_long_productions(result)
        
        return result
