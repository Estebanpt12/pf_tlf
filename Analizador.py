import string
import tkinter as tk

class LexicalAnalyzer:
    def __init__(self):
        self.operators = {
            'sumi': {'name': 'addition'},
            'resti': {'name': 'subtraction'},
            'multi': {'name': 'multiplication'},
            'divi': {'name': 'division'},
            'elevi': {'name': 'exponentiation'},
            'rai': {'name': 'root'},
            '%': {'name': 'modulo'},
            '%%?': {'name': 'relational operator equal'},
            '!%?': {'name': 'relational operator not equal'},
            '>?': {'name': 'relational operator greater'},
            '<?': {'name': 'relational operator less'},
            '>%?': {'name': 'relational operator greater or equal'},
            '<%?': {'name': 'relational operator less or equal'},
            'YY': {'name': 'logical AND'},
            'OO': {'name': 'logical OR'},
            'NO': {'name': 'logical NOT'},
            '%=': {'name': 'simple assignment operator'},
            '+%': {'name': 'assignment with addition'},
            '-%': {'name': 'assignment with subtraction'},
            '*%': {'name': 'assignment with multiplication'},
            '/%': {'name': 'assignment with division'},
            '%%=': {'name': 'assignment with modulo'},
            '[': {'name': 'opening bracket'},
            'ñ': {'name': 'opening ñ'},
            '^': {'name': 'opening circumflex'},
            ']': {'name': 'closing bracket'},
            'ñ': {'name': 'closing ñ'},
            '^': {'name': 'closing circumflex'},
            '$': {'name': 'terminal'},
            '|': {'name': 'statement separator'},
            'enterito64': {'name': 'integer variable'},
            'realsote64': {'name': 'real variable'},
            'textil': {'name': 'array variable'},
            'caractersito': {'name': 'character variable'},
            'MANGO': {'name': 'MANGO'},
            'identifiers': [
                {'name': 'variable identifier', 'prefixes': ['variavel']},
                {'name': 'method identifier', 'prefixes': ['novoMetodo']},
                {'name': 'class identifier', 'prefixes': ['novoClasse']},
            ],
        }

        self.reserved_words = [
            'si', 'siNo', 'mientras', 'por', 'porCada', 'hacerMientras', 'entonces', 'habilidade', 'abstrato', 'especies'
        ]

    def is_identifier_by_prefix(self, word):
        """Check if the word is an identifier by its prefix."""
        for identifier in self.operators['identifiers']:
            if word.startswith(tuple(identifier['prefixes'])):
                return identifier['name']
        return None

    def is_alphanumeric_identifier(self, word):
        """Check if the word is a valid alphanumeric identifier."""
        if word[0] in string.digits:
            return False
        for char in word:
            if char not in string.ascii_letters + string.digits + '_':
                return False
        return True

    def is_number(self, word):
        """Check if the word is a valid number."""
        try:
            float(word)
            return True
        except ValueError:
            return False

    def is_decimal(self, word):
        """Check if the word is a valid decimal number."""
        try:
            float(word)
            return word.count('.') == 1
        except ValueError:
            return False

    def add_token(self, name, value, tokens):
        """Add a token to the list and print it."""
        print(f"{value} = {name}")
        tokens.append((name, value))

    def add_word(self, word, tokens):
        """Add a word as a token to the list of tokens."""
        if not word:
            return

        if word.startswith('#'):
            self.add_token('COMMENT', word, tokens)
            return

        identifier = self.is_identifier_by_prefix(word)
        if identifier:
            self.add_token(identifier, word, tokens)
            return

        if word in self.operators:
            operator_info = self.operators[word]
            self.add_token(operator_info['name'], word, tokens)
            return

        if word in self.reserved_words:
            self.add_token('RESERVED WORD', word, tokens)
            return

        if self.is_number(word):
            if self.is_decimal(word):
                self.add_token('REAL', word, tokens)
            else:
                self.add_token('INTEGER', word, tokens)
            return

        if self.is_alphanumeric_identifier(word):
            self.add_token('IDENTIFIER', word, tokens)
            return

        if word == '%':
            previous_token = tokens[-1] if tokens else None
            if previous_token and self.is_alphanumeric_identifier(previous_token[1]):
                self.add_token('hash variable', word, tokens)
            else:
                self.add_token('modulo', word, tokens)
            return

        self.add_token('UNRECOGNIZED', word, tokens)

    def analyze_lexically(self, code):
        """Perform lexical analysis on the given code."""
        word = ''
        tokens = []
        is_comment = False
        is_string = False

        for char in code:
            if char == '\n':
                if is_comment:
                    self.add_token('COMMENT', word, tokens)
                    word = ''
                    is_comment = False
                continue

            if char == '#':
                is_comment = True

            if is_comment:
                word += char
                continue

            if char == '"':
                if is_string:
                    self.add_token('STRING', word, tokens)
                    word = ''
                    is_string = False
                else:
                    self.add_word(word, tokens)
                    word = ''
                    is_string = True
                self.add_token('QUOTES', char, tokens)
                continue

            if is_string:
                word += char
                continue

            if char in string.whitespace:
                self.add_word(word, tokens)
                word = ''
            elif char.isalnum() or char == '_' or char == '.':
                word += char
            elif char in string.punctuation:
                self.add_word(word, tokens)
                word = ''
                if char != '.':
                    self.add_word(char, tokens)
            else:
                self.add_word(word, tokens)
                word = ''

        self.add_word(word, tokens)
        return tokens

class LexicalAnalyzerApp:
    def __init__(self, root):
        self.analyzer = LexicalAnalyzer()
        self.root = root
        self.root.geometry("650x450")
        self.root.title("Lexical Analyzer")

        # Create the text field for input code
        self.input_text = tk.Text(self.root, bg='#E1E1E1', height=10)
        self.input_text.grid(row=0, column=0, pady=10)

        # Create the text field for output tokens
        self.output_text = tk.Text(self.root, bg='#E1E1E1', height=15)
        self.output_text.grid(row=1, column=0)

        # Create the analyze button
        self.analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_code)
        self.analyze_button.grid(row=0, column=0, sticky="e")

    def analyze_code(self):
        """Analyze the code in the input text field and display the tokens in the output text field."""
        code = self.input_text.get("1.0", "end")
        tokens = self.analyzer.analyze_lexically(code)
        output = ""
        for token in tokens:
            name, value = token
            output += f"{value} = {name}\n"
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", output)

if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerApp(root)
    root.mainloop()
