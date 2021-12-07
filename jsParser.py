# Syntax Parser by Elmer Jaén

import re

keywords = r'''var\b|if\b|else\b|return\b|function\b|continue\b|boolean\b|break\b|case\b'''

def get_tokens(a):

    token_list = [x.strip(' |\n') for x in a]
    p_keywords = re.compile(keywords)
    p_var = re.compile('(\w+)(?<!['+keywords+']|[\d+])')
    p_numbers = re.compile('\d+')
    p_special_characters = re.compile('\W')

    t = {}
    tokens = {
        "Palabras reservadas:": p_keywords,
        "Variables:": p_var,
        "Números:": p_numbers,
        "Caracteres especiales:": p_special_characters
    }

    for key, value in tokens.items():
        for i in token_list:
            if value.match(i):
                if key not in t:
                    t[key] = list()
                t[key].append(i)
    return t

def evaluate_sql(js_string):

    variable = '[a-zA-Z](\w+)*'
    a = '([a-zA-Z](\w+)*|\d+)'    

    # regex para un statement
    # La cadena a evaluar debe empezar por la palabra reservada var,
    # seguido de un espacio, seguido de una palabra que no empiece por número
    # y que no sea keyword, seguido de un espacio, seguido del caracter =,
    # (seguido de espacio, seguido de: una letra o palabra que no empiece por número
    # y que no sea keyword, o un número).
    # Lo que está dentro del paréntesis puede aparecer 0 o más veces.
    # La cadena debe terminar en ;
    # Ejemplo: var nombre = elmer;
    
    statement = r"(var\s)*(?!"+keywords+")"+variable+"\s=\s(?!"+keywords+")("+variable+"|\d+)(\s(\+|\*|-|/)\s(?!"+keywords+")("+variable+"|\d+))*;"
    p_statement = re.compile(statement)

    # regex para condicional if-else (más simple)
    p_condition = re.compile(r"""if\s\((?!"""+keywords+""")\w+\s
                                (==|!=|>(=)*|<(=)*)\s(?!"""+keywords+""")\w+\){
                                (\\n\s{4}"""+statement+""")+\\n}
                                (\selse\s{(\\n\s{4}"""+statement+""")+\\n})*""", re.X)

    # regex para ciclo for
    p_for = re.compile(r"""for\s\((var\s)*(?!"""+keywords+""")"""+variable+"""\s=\s
                            (?!"""+keywords+""")"""+a+""";\s
                            (?!"""+keywords+""")"""+variable+"""\s(<(=)*|>(=)*)\s
                            (?!"""+keywords+""")"""+a+""";\s
                            (?!"""+keywords+""")"""+variable+"""(\\+\\+|--)\){

                            (\\n\s{4}("""+statement+"""|break;|continue;))+\\n}""", re.X)

    patterns = {
        "condicional": p_condition,
        "declarativa": p_statement,
        "for": p_for
    }

    for key, value in patterns.items():
        if value.fullmatch(js_string):
            print(value.fullmatch(js_string))
            return 1, key
    return 0,0