import tkinter as tk
from tkinter import filedialog

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("TLF")

        # Crear un botón para seleccionar un archivo
        self.boton_seleccionar_archivo = tk.Button(root, text="Select File", command=self.seleccionar_archivo)
        self.boton_seleccionar_archivo.pack(pady=10)

        # Crear una etiqueta para mostrar el archivo seleccionado
        self.etiqueta_archivo = tk.Label(root, text="The file has not been selected")
        self.etiqueta_archivo.pack(pady=10)

        # Crear un cuadro de texto grande
        self.cuadro_texto = tk.Text(root, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
        self.cuadro_texto.pack(pady=10)

        # Definir operadores y palabras reservadas
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

    def seleccionar_archivo(self):
        #Abrir archivo
        archivo = filedialog.askopenfilename()
        if archivo:
            #Etiqueta de abrir el archivo
            self.etiqueta_archivo.config(text=f"Selected File: {archivo}")
            #Se abre el archivo
            with open(archivo, 'r') as file:
                contenido = file.read()
                self.mostrar_palabras_con_posicion(contenido)

    def mostrar_palabras_con_posicion(self, texto):
        #Se habilita para escribir el cuadro de texto
        self.cuadro_texto.config(state=tk.NORMAL)
        #Se borra lo que hay en el cuadro de texto
        self.cuadro_texto.delete(1.0, tk.END)
        lineas = texto.splitlines()
        #Se recorren las lineas
        for fila, linea in enumerate(lineas):
            #Si empieza por # es un comentario de linea
            if linea.startswith('#'):
                self.cuadro_texto.insert(tk.END, f"{linea} (Row: {fila + 1}) - Line Comment\n")
            else:
                palabras = linea.split()
                columna = 0
                ultimo_identificador = None
                for palabra in palabras:
                    # Encontrar la columna correcta donde comienza la palabra
                    columna = linea.index(palabra, columna)
                    #Se calcula la posicion
                    posicion = f"(Row: {fila + 1}, Column: {columna + 1})"
                    descripcion = self.clasificar_palabra(palabra, ultimo_identificador)
                    if "Identifier" in descripcion:
                        ultimo_identificador = palabra
                    else:
                        ultimo_identificador = None
                    self.cuadro_texto.insert(tk.END, f"{palabra} {posicion} - {descripcion}\n")
                    # Mover la columna para el siguiente ciclo
                    columna += len(palabra)
        self.cuadro_texto.config(state=tk.DISABLED)

    def clasificar_palabra(self, palabra, ultimo_identificador):
        if self.es_error_numero_entero(palabra):
            return "Error Integer"
        elif self.es_numero_entero(palabra):
            return "Integer"
        elif self.es_numero_decimal(palabra):
            return "Decimal"
        elif self.es_error_numero_decimal(palabra):
            return "Error Decimal"
        elif self.es_caracter(palabra):
            return "Char"
        elif self.es_error_string(palabra):
            return "Error String"
        elif self.es_string(palabra):
            return "String"
        if ultimo_identificador is not None:
            return f"Name of the previous identifier"
        if palabra in self.reserved_words:
            return "Reserved Word"
        elif palabra in self.operators:
            return f"Operator: {self.operators[palabra]['name']}"
        else:
            for identifier in self.operators['identifiers']:
                for prefix in identifier['prefixes']:
                    if palabra.startswith(prefix):
                        return f"Identifier: {identifier['name']}"
            return "Unidentified"

    def es_string(self, palabra):
        # Verificar si la palabra empieza y termina con "&" y si el segundo y el penúltimo caracter son letras mayúsculas o minúsculas
        return len(palabra) >= 4 and palabra.startswith('&') and palabra.endswith('&') and palabra[1].isalpha() and palabra[-2].isalpha()
    
    def es_error_string(self, palabra):
        # Verificar si la palabra empieza y termina con "&" y si el segundo y el penúltimo caracter son letras mayúsculas o minúsculas
        return (len(palabra) >= 4 and not palabra.startswith('&') and palabra.endswith('&') and palabra[1].isalpha() and palabra[-2].isalpha()) or (len(palabra) >= 4 and palabra.startswith('&') and not palabra.endswith('&') and palabra[1].isalpha() and palabra[-2].isalpha()) or (len(palabra) >= 4 and palabra.endswith('&') and palabra.startswith('&') and not palabra[1].isalpha() and palabra[-2].isalpha()) or (len(palabra) >= 4 and palabra.startswith('&') and palabra[1].isalpha() and not palabra[-2].isalpha() and palabra.endswith('&'))

    def es_caracter(self, palabra):
        # Verificar si la palabra tiene longitud 1, si es un carácter ASCII, y si no es el numeral #
        return len(palabra) == 1 and 32 <= ord(palabra) <= 126 and palabra != '#'

    def es_numero_decimal(self, palabra):
        # Verificar si la palabra comienza y termina con "#" y si contiene exactamente una "@" en su interior
        partes = palabra.split("@")
        return palabra.startswith('#') and palabra.endswith('#') and len(partes) == 2 and partes[0][1:].isdigit() and partes[1][:-1].isdigit()
    
    def es_error_numero_decimal(self, palabra):
        # Verificar si la palabra comienza y termina con "#" y si contiene exactamente una "@" en su interior
        partes = palabra.split("@")
        return (palabra.startswith('#') and not palabra.endswith('#') and len(partes) == 2 and partes[0][1:].isdigit() and partes[1][:-1].isdigit()) or (not palabra.startswith('#') and palabra.endswith('#') and len(partes) == 2 and partes[0][1:].isdigit() and partes[1][:-1].isdigit())
        
    def es_numero_entero(self, palabra):
        # Verificar si la palabra comienza y termina con "#" y si el contenido entre los numerales consiste en caracteres numéricos
        return palabra.startswith('#') and palabra.endswith('#') and palabra[1:-1].isdigit()
    
    def es_error_numero_entero(self, palabra):
        # Verificar si la palabra es un numero con error si el contenido entre los numerales consiste en caracteres numéricos
        return (palabra.startswith('#') and not palabra.endswith('#') and palabra[1:-1].isdigit()) or (not palabra.startswith('#') and palabra.endswith('#') and palabra[1:-1].isdigit())

    def escribir_texto(self, texto):
        self.cuadro_texto.insert(tk.END, texto)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)    
    root.mainloop()
