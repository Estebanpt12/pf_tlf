# Importamos las bibliotecas necesarias
import string
import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()
root.geometry("650x450")
root.title("Analizador Léxico")

# Creamos el campo de texto para el código a analizar
codigo_texto = tk.Text(root,bg='#E1E1E1', height=10) 
codigo_texto.grid(row=0, column=0, pady=10)

# Creamos el campo de texto para la salida del análisis
salida_texto = tk.Text(root,bg='#E1E1E1', height=15)
salida_texto.grid(row=1, column=0)

# Definimos los operadores y su nombre correspondiente
diccionario_operadores = {
    'sumi': { 'nombre': 'suma'},
    'resti': { 'nombre': 'resta'},
    'multi': { 'nombre': 'multision'},
    'divi': { 'nombre': 'division'},
    'elevi': { 'nombre': 'potencia'},
    'rai': { 'nombre': 'raiz'},
    '%': { 'nombre': 'modulo'},
    '%%?': { 'nombre': 'operador relacional igual'},
    '!%?': { 'nombre': 'operador relacional diferente'},
    '>?': { 'nombre': 'operador relacional mayor'},
    '<?': {'nombre': 'operador relacional menor '},
    '>%?': {'nombre': 'operador relacional mayor o igual'},
    '<%?': {'nombre': 'operador relacional menor o igual'},
    'YY': {'nombre': 'Y logico'},
    'OO': {'nombre': 'O logico'},
    'NO': { 'nombre': 'NO logico'},
    '%=': { 'nombre': 'operador de asignacion simple'},
    '+%': { 'nombre': 'operador de asignacion y suma'},
    '-%': { 'nombre': 'operador de asignacion y resta'},
    '*%': { 'nombre': 'operador de asignacion y multiplicacion'},
    '/%': {'nombre': 'operador de asignacion y division'},
    '%%=': { 'nombre': 'operador de asignacion y modulo'},
    '[': {'nombre': 'llave de apertura'},
    'ñ': {'nombre': 'ñ de apertura'},
    '^': {'nombre': 'circunflejo apertura'},
    ']': { 'nombre': 'llave de cierre'},
    'ñ': {'nombre': 'ñ de cierre'},
    '^': {'nombre': 'corchete de cierre'},
    '$': {'nombre': 'terminal'},
    '|': {'nombre': 'separador de sentencias'},
    'enterito64': { 'nombre': 'variable entera'},
    'realsote64': { 'nombre': 'variable real'},
    'textil': { 'nombre': 'variable de array'},
    'caractersito': { 'nombre': 'variable de caracteres'},
    'MANGO': {'nombre': 'MANGO'},
    'identificadores': [
        {'nombre': 'identificador variable', 'prefijos': ['variavel']},
        {'nombre': 'identificador metodo', 'prefijos': ['novoMetodo']},
        {'nombre': 'identificador clase', 'prefijos': ['novoClasse']},
    ],
}

# Definimos las palabras reservadas
palabras_reservadas = [
    'si', 'siNo', 'mientras', 'por', 'porCada', 'hacerMientras','entonces','habilidade','abstrato','especies'
]

# Función para verificar si una palabra es un identificador
def es_identificador1(palabra):
    # Recorremos todos los identificadores en el diccionario de operadores
    for identificador in diccionario_operadores['identificadores']:
        # Verificamos si la palabra comienza con alguno de los prefijos del identificador actual
        if palabra.startswith(tuple(identificador['prefijos'])):
            # Si es así, retornamos el nombre del identificador
            return identificador['nombre']
    # Si la palabra no comienza con ninguno de los prefijos de los identificadores, retornamos None
    return None

# Función para verificar si una palabra es un identificador alfanumérico
def es_identificador(palabra):
    # Si el primer carácter de la palabra es un dígito, retornamos False
    # ya que los identificadores no pueden comenzar con un número
    if palabra[0] in string.digits:
        return False
    # Recorremos cada carácter en la palabra
    for char in palabra:
        # Si el carácter no es una letra, un número o un guión bajo, retornamos False
        # ya que los identificadores solo pueden contener estos caracteres
        if char not in string.ascii_letters + string.digits + '_':
            return False
    # Si todos los caracteres son válidos, retornamos True
    return True

# Función para verificar si una palabra es un número
def es_numero(palabra):
    try:
        # Intentamos convertir la palabra a un número flotante
        float(palabra)
        # Si la conversión es exitosa, la palabra es un número, por lo que retornamos True
        return True
    except ValueError:
        # Si la conversión falla (lo que lanza un ValueError), la palabra no es un número, por lo que retornamos False
        return False

# Función para verificar si una palabra es un número decimal
def es_decimal(palabra):
    try:
        # Intentamos convertir la palabra a un número flotante
        float(palabra)
        # Si la conversión es exitosa, verificamos si la palabra contiene exactamente un punto decimal
        # Si es así, la palabra es un número decimal, por lo que retornamos True
        return palabra.count('.') == 1
    except ValueError:
        # Si la conversión falla (lo que lanza un ValueError), la palabra no es un número decimal, por lo que retornamos False
        return False

def agregar_token(nombre, valor, tokens):
    # Imprime el valor y el nombre del token
    print(f"{valor} = {nombre}")
    # Agrega el token a la lista de tokens
    tokens.append((nombre, valor))

# Función para agregar una palabra como un token a la lista de tokens
def agregar_palabra(palabra, tokens):
    # Si la palabra está vacía, no hacemos nada
    if not palabra:
        return

    # Si la palabra comienza con '#', es un comentario, así que la agregamos como tal
    if palabra.startswith('#'):
        agregar_token('COMENTARIO', palabra, tokens)
        return

    # Verificamos si la palabra es un identificador
    identificador = es_identificador1(palabra)
    if identificador:
        # Si es un identificador, la agregamos como tal
        agregar_token(identificador, palabra, tokens)
        return

    # Verificamos si la palabra es un operador
    if palabra in diccionario_operadores:
        # Si es un operador, obtenemos su información y la agregamos como tal
        info_operador = diccionario_operadores[palabra]
        agregar_token(info_operador['nombre'], palabra, tokens)
        return

    # Verificamos si la palabra es una palabra reservada
    if palabra in palabras_reservadas:
        # Si es una palabra reservada, la agregamos como tal
        agregar_token('PALABRA RESERVADA', palabra, tokens)
        return

    # Verificamos si la palabra es un número
    if es_numero(palabra):
        # Si es un número, verificamos si es un número decimal
        if es_decimal(palabra):
            # Si es un número decimal, la agregamos como tal
            agregar_token('REAL', palabra, tokens)
        else:
            # Si no es un número decimal, es un número entero, así que la agregamos como tal
            agregar_token('ENTERO', palabra, tokens)
        return

    # Verificamos si la palabra es un identificador alfanumérico
    if es_identificador(palabra):
        # Si es un identificador alfanumérico, la agregamos como tal
        agregar_token('IDENTIFICADOR', palabra, tokens)
        return

    # Verificamos si la palabra es un '%'
    if palabra == '%':
        # Si es un '%', verificamos si el token anterior es un identificador
        siguiente_token = tokens[-1] if tokens else None
        if siguiente_token and es_identificador(siguiente_token[1]):
            # Si el token anterior es un identificador, la palabra es una variable de hash, así que la agregamos como tal
            agregar_token('variable de hash', palabra, tokens)
        else:
            # Si el token anterior no es un identificador, la palabra es un módulo, así que la agregamos como tal
            agregar_token('modulo', palabra, tokens)
        return

    # Si la palabra no cumple con ninguna de las condiciones anteriores, no la reconocemos, así que la agregamos como tal
    agregar_token('NO RECONOCIDO', palabra, tokens)

# Función para realizar el análisis léxico
def lexico(codigo):
    palabra = ''  # Almacena la palabra actual que se está analizando
    tokens = []  # Almacena los tokens encontrados
    comentario = False  # Indica si estamos en medio de un comentario
    cadena = False  # Indica si estamos en medio de una cadena

    # Recorremos cada carácter en el código
    for c in codigo:
        # Si encontramos un salto de línea
        if c == '\n':
            # Si estamos en medio de un comentario, lo agregamos como un token
            if comentario:
                agregar_token('COMENTARIO', palabra, tokens)
                palabra = ''
                comentario = False
            continue
        # Si encontramos un '#', comenzamos un comentario
        if c == '#':
            comentario = True
        # Si estamos en medio de un comentario, agregamos el carácter a la palabra
        if comentario:
            palabra += c
            continue
        # Si encontramos un '"', comenzamos o terminamos una cadena
        if c == '"':
            # Si estamos en medio de una cadena, la agregamos como un token
            if cadena:
                agregar_token('CADENA', palabra, tokens)
                palabra = ''
                cadena = False
            else:
                agregar_palabra(palabra, tokens)
                palabra = ''
                cadena = True
            agregar_token('COMILLAS', c, tokens)
            continue
        # Si estamos en medio de una cadena, agregamos el carácter a la palabra
        if cadena:
            palabra += c
            continue
        # Si encontramos un espacio en blanco, terminamos la palabra actual y la agregamos como un token
        if c in string.whitespace:
            agregar_palabra(palabra, tokens)
            palabra = ''
        # Si encontramos un carácter alfanumérico, un '_' o un '.', lo agregamos a la palabra
        elif c.isalnum() or c == '_' or c == '.':
            palabra += c
        # Si encontramos un carácter de puntuación, terminamos la palabra actual y la agregamos como un token
        elif c in string.punctuation:
            agregar_palabra(palabra, tokens)
            palabra = ''
            # Si el carácter de puntuación no es un '.', lo agregamos como un token
            if c != '.':
                agregar_palabra(c, tokens)
        else:
            agregar_palabra(palabra, tokens)
            palabra = ''

    # Agregamos la última palabra como un token
    agregar_palabra(palabra, tokens)

    # Retornamos la lista de tokens
    return tokens

# Función para analizar el código
def analizar():
    # Obtiene el código del widget de texto
    codigo = codigo_texto.get("1.0", "end")
    # Obtiene los tokens del código utilizando la función lexico
    tokens = lexico(codigo)
    # Inicializa una cadena vacía para la salida
    salida = ""
    # Itera sobre cada token
    for token in tokens:
        # Desempaqueta el token en nombre y valor
        nombre, valor = token
        # Agrega el valor y el nombre del token a la salida
        salida += f"{valor} = {nombre}\n"
    # Borra el contenido actual del widget de texto de salida
    salida_texto.delete("1.0", "end") 
    # Inserta la salida en el widget de texto de salida
    salida_texto.insert("1.0", salida)

# Crea un botón con el texto "Analizar" que, cuando se presiona, llama a la función analizar
boton = tk.Button(root, text="Analizar", command=analizar)
# Coloca el botón en la cuadrícula en la fila 0, columna 0, alineado a la derecha
boton.grid(row=0, column=0, sticky="e")

# Inicia el bucle principal de Tkinter
root.mainloop()

# Ejemplo de uso de la función lexico
codigo = '''xyz:= xyz + 1 + @
si y > 57
      a := (35 + b1 b2
fin si 
my variable class'''

# Llama a la función lexico con el código de ejemplo
lexico(codigo)