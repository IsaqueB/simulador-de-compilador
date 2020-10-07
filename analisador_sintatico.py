import analisador_lexico

arquivo = open('arquivo.txt','r')
f = arquivo.read()
arquivo.close()
lista = analisador_lexico.identificador_tokens(f)

#Os métodos sempre retornam a posição token final de sua análise

def programa(text):
    pos = sequencia_de_comandos(text,0)
    if pos > 0:
        try:
            if (text[pos+1])["Valor do Atributo"] == "END":
                return True
            else:
                return erro("ESPERADO 'END'")
        except IndexError:
            erro("ESPERADO 'END'")
    elif pos == -1:
        return False
    else:
        return erro("ESPERADO SEQUENCIA DE COMANDOS")

def sequencia_de_comandos(text,pos):
    try:
        new_pos_aux = 0
        new_pos = comando(text,pos-1)
        if new_pos > new_pos_aux:
            try:
                while (text[new_pos+1])["Valor do Atributo"] == ';':
                    new_pos_aux = new_pos+1
                    new_pos = comando(text,new_pos+1)
            except IndexError:
                return erro("TAMANHO ERRADO. ESPERADO 'END' APOS SEQUENCIA DE COMANDOS")
            return new_pos
        else:
            return erro("ESPERADO COMANDO INICIAL EM SEQUENCIA DE COMANDOS")
    except IndexError:
        return erro("TAMANHO INVALIDO. ARQUIVO VAZIO")

def comando(text,pos):
    try:
        new_pos_aux = pos
        new_pos = rotulo(text,pos)
        if new_pos == -1:
            new_pos = new_pos_aux
        while new_pos > new_pos_aux:
            if (text[new_pos+1])["Valor do Atributo"] == ':':
                new_pos_aux = new_pos+1
                new_pos = rotulo(text,new_pos+1)
                if new_pos == -1:
                    new_pos = new_pos_aux
            else:
                return erro("ESPERADO ':'")
        if (text[new_pos+1])["Valor do Atributo"] == 'LET':
            new_pos = atribuicao(text,new_pos)
            return new_pos
        elif (text[new_pos+1])["Valor do Atributo"] == 'GO':
            new_pos = desvio(text,new_pos)
            return new_pos
        elif (text[new_pos+1])["Valor do Atributo"] == 'READ':
            new_pos = leitura(text,new_pos)
            return new_pos
        elif (text[new_pos+1])["Valor do Atributo"] == 'PRINT':
            new_pos = impressao(text,new_pos)
            return new_pos
        elif (text[new_pos+1])["Valor do Atributo"] == 'IF':
            new_pos = decisao(text,new_pos)
            return new_pos
        else:
            return erro("ESPERADO ATRIBUICAO | DESVIO | LEITURA | IMPRESSAO | DECISAO")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO ATRIBUICAO | DESVIO | LEITURA | IMPRESSAO | DECISAO")

def atribuicao(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == 'LET':
            if (text[pos+2])["Classe Gramátical"].lower() == 'identificador':
                if (text[pos+3])["Classe Gramátical"].lower() == 'sinal composto de atribuição':
                    new_pos = expressao(text,pos+3)
                    if new_pos > pos+3:
                        return new_pos
                    else:
                        return erro("ESPERADO EXPRESSAO")
                else:
                    return erro("ESPERADO ':='")
            else:
                return erro("ESPERADO IDENTIFICADOR 1")
        else:
            return erro("ESPERADO 'LET'")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO LET + IDENTIFICADOR + ':=' + EXPRESSAO")
def expressao(text,pos):
    try:
        new_pos = termo(text,pos)
        if new_pos > pos:
            try:
                while (((text[new_pos+1])["Valor do Atributo"] == '+') | ((text[new_pos+1])["Valor do Atributo"] == '-')):
                    new_pos = termo(text,new_pos+1)
                return new_pos
            except IndexError:
                pass
                #COMO O QUE ESTA DENTRO DO TRY NÃO É OBRIGATÓRIO, DEIXEI O PASS PARA QUE O ERRO OCORRA EM OUTRO LUGAR, PROVAVELMETNE QUANDO FOR BUSCAR O "END" NO FIM DO TEXTO
        else:
            return erro("ESPERADO TERMO")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO TERMO {('+'|'-') TERMO}")
def termo(text,pos):
    try:
        new_pos = fator(text,pos)
        if new_pos > pos:
            try:
                while (((text[new_pos+1])["Valor do Atributo"] == '*') | ((text[new_pos+1])["Valor do Atributo"] == '/')):
                    new_pos = fator(text,new_pos+1)
                return new_pos
            except IndexError:
                return pos
                #COMO O QUE ESTA DENTRO DO TRY NÃO É OBRIGATÓRIO, DEIXEI O PASS PARA QUE O ERRO OCORRA EM OUTRO LUGAR, PROVAVELMETNE QUANDO FOR BUSCAR O "END" NO FIM DO TEXTO
        else:
            return erro("ESPERADO FATOR")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO FATOR {('*'|'/') TERMO}")
def fator(text,pos):
    try:
        if (text[pos+1])["Classe Gramátical"].lower() == 'identificador':
            return pos+1
        elif (text[pos+1])["Classe Gramátical"].lower() == 'número':
            return pos+1
        elif (text[pos+1])["Valor do Atributo"] == '(':
            new_pos = expressao(text,pos+1)
            if new_pos > pos+1:
                if (text[new_pos+1])["Valor do Atributo"] == ')':
                    return new_pos+1
                else:
                    return erro("ESPERADO ')'")
            else:
                return erro("ESPERADO EXPRESSAO")
        else:
            return erro("ESPERADO IDENTIFICADOR | NUMERO | '(' EXPRESSAO ')'")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO IDENTIFICADOR | NUMERO | '(' EXPRESSAO ')'")
def desvio(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == 'GO':
            if (text[pos+2])["Valor do Atributo"] == 'TO':
                if (text[pos+4])["Valor do Atributo"] == 'OF':
                    if (text[pos+3])["Classe Gramátical"].lower() == "identificador":
                        new_pos = lista_de_rotulos(text,pos+4)
                        if new_pos > pos+4:
                            return new_pos
                        else:
                            return erro("ESPERADO 'OF'")
                    else:
                        return erro("ESPERADO LISTA DE ROTULOS")
                else:
                    new_pos = rotulo(text,pos+2)
                    if new_pos > pos+2:
                        return new_pos
                    else:
                        return erro("ESPERADO ROTULO | IDENTIFICADOR 'OF' LISTA DE ROTULOS")
            else:
                return erro("ESPERADO 'TO'")
        else:
            return erro("ESPERADO 'GO'")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO 'GO' 'TO' (ROTULO | IDENTIFICADOR 'OF' LISTA DE ROTULOS)")
def lista_de_rotulos(text,pos):
    try:
        new_pos_aux = pos
        new_pos = rotulo(text,pos+1)
        while new_pos > new_pos_aux:
            if (text[new_pos+1])["Valor do Atributo"] == ',':
                new_pos_aux = new_pos
                new_pos = rotulo(text,pos+1)
                if new_pos < new_pos_aux:
                    return erro("ESPERADO ROTULO APOS ','")
        return new_pos
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO ROTULO {',' ROTULO}")
def rotulo(text,pos):
    try:
        if (text[pos+1])["Classe Gramátical"].lower() == "identificador":
            return pos+1
        else:
            return -1
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO IDENTIFICADOR")
def leitura(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == 'READ':
            new_pos = lista_de_identificadores(text,pos+1)
            if new_pos > pos+1:
                return new_pos
            else:
                return erro("ESPERADO LISTA DE IDENTIFICADOR")
        else:
            return erro("ESPERADO READ")
    except IndexError:
        return erro("TAMANHO INVALIDO, ESPERADO 'READ' LISTA DE IDENTIFICADOR")
def lista_de_identificadores(text,pos):
    try:
        if (text[pos+1])["Classe Gramátical"].lower() == "identificador":
            new_pos_aux = pos
            new_pos = pos+1
            while (text[new_pos+1])["Valor do Atributo"] == ',':
                if (text[new_pos+2])["Classe Gramátical"].lower() == "identificador":
                    new_pos_aux = new_pos
                    new_pos += 2
                else:
                    new_pos = -1
            if new_pos > new_pos_aux:
                return new_pos
            else:
                return erro("ESPERADO IDENTIFICADOR APOS ','")
    except IndexError:
        pass
        #COMO O QUE ESTA DENTRO DO TRY NÃO É OBRIGATÓRIO, DEIXEI O PASS PARA QUE O ERRO OCORRA EM OUTRO LUGAR, PROVAVELMETNE QUANDO FOR BUSCAR O "END" NO FIM DO TEXTO
def impressao(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == 'PRINT':
            new_pos = lista_de_expressoes(text,pos+1)
            if new_pos > pos+1:
                return new_pos
            else:
                return erro("ESPERADO LISTA DE EXPRESSOES")
        else:
            return erro("ESPERADO PRINT")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO 'PRINT' LISTA DE EXPRESSOES")
def lista_de_expressoes(text,pos):
    try:
        new_pos_aux = pos
        new_pos = expressao(text,pos)
        while new_pos > new_pos_aux:
            if (text[new_pos+1])["Valor do Atributo"] == ',':
                new_pos_aux = new_pos+1
                new_pos = expressao(text,new_pos+1)
            else:
                if new_pos == -1:
                    return erro("ESPERADO EXPRESSAO APOS ','")
                else:
                    return new_pos
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO [EXPRESSAO {',' EXPRESSAO}]")

def decisao(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == 'IF':
            new_pos_aux = pos+1
            new_pos = comparacao(text,pos+1)
            if new_pos > new_pos_aux:
                if (text[new_pos+1])["Valor do Atributo"] == 'THEN':
                    new_pos_aux = new_pos+1
                    new_pos = comando(text,new_pos+1)
                    if new_pos > new_pos_aux:
                        if (text[new_pos+1])["Valor do Atributo"] == 'ELSE':
                            new_pos_aux = new_pos+1
                            new_pos = comando(text,new_pos+1)
                            if new_pos > new_pos_aux:
                                return new_pos
                            else:
                                return erro("ESPERADO COMANDO")
                        else:
                            return erro("ESPERADO 'ELSE' COMANDO")
                    else:
                        return erro("ESPERADO COMANDO 'ELSE' COMANDO")
                else:
                    return erro("ESPERADO 'THEN' COMANDO 'ELSE' COMANDO'")
            else:
                return erro("ESPERADO COMPARACAO 'THEN' COMANDO 'ELSE' COMANDO")
        else:
            return erro("ESPERADO 'IF' COMPARACAO 'THEN' COMANDO 'ELSE' COMANDO")
    except IndexError:
        return erro("TAMANHO INVALIDO. ESPERADO 'IF' COMPARACAO 'THEN' COMANDO 'ELSE' COMANDO")

def comparacao(text,pos):
    try:
        new_pos_aux = pos
        new_pos = expressao(text,pos)
        if new_pos > new_pos_aux:
            new_pos_aux = new_pos
            new_pos = operador_de_comparacao(text,new_pos)
            if new_pos > new_pos_aux:
                new_pos_aux = new_pos
                new_pos = expressao(text,new_pos)
                if new_pos > new_pos_aux:
                    return new_pos
                else:
                    return erro("ESPERADO EXPRESSAO")
            else:
                return erro("ESPERADO OPERADOR DE COMPARACAO EXPRESSAO")
        else:
            return erro("ESPERADO EXPRESSAO OPERADOR DE COMPARACAO EXPRESSAO")
    except IndexError:
        return erro("TAMANHO INVALIDO ESPERADO EXPRESSAO OPERADOR DE COMPARACAO EXPRESSAO")

def operador_de_comparacao(text,pos):
    try:
        if (text[pos+1])["Valor do Atributo"] == '>':
            return pos+1
        elif (text[pos+1])["Valor do Atributo"] == '=':
            return pos+1
        elif (text[pos+1])["Valor do Atributo"] == '<':
            return pos+1
        else:
            return erro("ESPERADO '>' | '=' | '<'")
    except IndexError:
        return erro("TAMANHO INVALIDO ESPERADO '>' | '=' | '<'")

def erro(texto):
    print(texto)
    return -1


a = programa(lista)
if(a):
    print("SUCESSO!")
