# jsParser by Elmer Jaén, Louis Aguilar, Omar Flores

import re

keywords = r'''var\b|let\b|if\b|else\b|for\b|break\b|
            continue\b|function\b|const\b|boolean\b|case\b'''

def get_tokens(a):

    token_list = [x.strip(' |\n') for x in a]
    p_keywords = re.compile(keywords)
    p_var = re.compile('(?!'+keywords+')[a-zA-Z]|_(\w+)*')
    p_numbers = re.compile('\d+')
    p_operators = re.compile('\+|\*|-|/|=')
    p_special_characters = re.compile('(?!\+|\*|-|/|=)\W')

    t = {}
    tokens = {
        "Palabras reservadas:": p_keywords,
        "Variables:": p_var,
        "Números:": p_numbers,
        "Operadores matemáticos:": p_operators,
        "Caracteres especiales:": p_special_characters
    }

    for key, value in tokens.items():
        for i in token_list:
            if value.match(i):
                if key not in t:
                    t[key] = list()
                if i not in t[key]:
                    t[key].append(i)
    return t

def check_string(js_string):

    variable = '([a-zA-Z]|_)(\w+)*'
    a = '([a-zA-Z](\w+)*|\d+)'    

    # regex para un statement
    # La cadena a evaluar empieza por la palabra reservada var o let (no obligatorio),
    # seguido de un espacio, seguido de una palabra que no empiece por número
    # y que no sea keyword, seguido de un espacio, seguido del caracter =,
    # (seguido de espacio, seguido de: una letra o palabra que no empiece por número
    # y que no sea keyword, o un número).
    # Lo que está dentro del paréntesis puede aparecer 0 o más veces.
    # La cadena debe terminar en ;
    # Ejemplo: var nombre = elmer;
    
    #regex para declarar una variable
    p_declare = re.compile(r"(var|let)\s"+variable+";")

    # regex para asignar un valor a una variable
    statement = r"((var\s|let\s)?(?!"+keywords+")"+variable+"\s=\s(?!"+keywords+")"+a+"(\s(\+|\*|-|/)\s(?!"+keywords+")"+a+")*;\\n?)+"
    p_statement = re.compile(statement)

    # regex para condicional if-else
    p_condition = re.compile(r"""if\s\((?!"""+keywords+""")\w+\s
                                (==|!=|>=?|<=?)\s(?!"""+keywords+""")\w+\){
                                (\\n\s{4}"""+statement+""")+\\n}
                                (\selse\s{(\\n\s{4}"""+statement+""")+\\n})?""", re.X)

    # regex para ciclo for
    p_for = re.compile(r"""for\s\((var\s)?(?!"""+keywords+""")"""+variable+"""\s=\s
                            (?!"""+keywords+""")"""+a+""";\s
                            (?!"""+keywords+""")"""+variable+"""\s(<=?|>=?)\s
                            (?!"""+keywords+""")"""+a+""";\s
                            (?!"""+keywords+""")"""+variable+"""(\+\+|--)\){
                            (\\n\s{4}("""+statement+"""|break;|continue;))+\\n}""", re.X)

    patterns = {
        "declarativa": p_declare,
        "de asignación": p_statement,
        "condicional": p_condition,
        "for": p_for
    }

    for key, value in patterns.items():
        if value.fullmatch(js_string):
            print(value.fullmatch(js_string))
            return 1, key
    return 0,0