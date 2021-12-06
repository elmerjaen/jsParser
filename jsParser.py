# Syntax Parser by Elmer Jaén

import re

keywords = r'''var\b|function\b|boolean\b|break\b|case\b|
        catch\b|continue\b|delete\b|do\b|else\b|finally\b|private\b'''

def get_tokens(a):

    token_list = [x.strip(' ') for x in a]
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

    # expresion regular para la sintaxis var de javascript
    p_var = re.compile(r"var[\s](?!"+keywords+")[a-zA-Z]\w+\s=\s(?!"+keywords+")[a-zA-Z]\w+")

    patterns = {
        "var": p_var,
    }

    for key, value in patterns.items():
        if value.fullmatch(js_string):
            print(value.fullmatch(js_string))
            return 1, key
    return 0,0