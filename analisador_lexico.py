import first

def identificador_tokens(texto):
    lista = []
    estado = 1
    st = ''
    linha = 1
    atual = 0
    while atual < len(texto):
        if estado == 1:
            if texto[atual] == ' ':
                atual+=1
            elif texto[atual] == '\n':
                linha+=1
                atual+=1
            elif texto[atual] == '%':
                estado = 6
            elif texto[atual].isalpha():
                estado = 2
            elif(texto[atual] == ':'):
                estado = 4
            elif texto[atual].isnumeric():
                estado = 3
            else:
                estado = 7
        elif estado == 2:
            if texto[atual].isalpha() | texto[atual].isnumeric():
                st = st + texto[atual]
                atual+=1
                if(atual == len(texto)):
                    if ((st == 'END') | (st == 'LET') | (st == 'GO') | (st == 'TO') | (st == 'OF') | (st == 'READ') | (st == 'PRINT') | (st == 'THEN') | (st == 'ELSE') | (st == 'IF')):
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Palavra Reservada','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1
                    else:
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Identificador','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1
            else:
                if(atual == len(texto)):
                    if ((st == 'END') | (st == 'LET') | (st == 'GO') | (st == 'TO') | (st == 'OF') | (st == 'READ') | (st == 'PRINT') | (st == 'THEN') | (st == 'ELSE') | (st == 'IF')):
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Palavra Reservada','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1
                    else:
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Identificador','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1
                        atual+=1
                else:
                    if ((st == 'END') | (st == 'LET') | (st == 'GO') | (st == 'TO') | (st == 'OF') | (st == 'READ') | (st == 'PRINT') | (st == 'THEN') | (st == 'ELSE') | (st == 'IF')):
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Palavra Reservada','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1
                    else:
                        Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Identificador','Linha':linha})
                        lista.append(Token)
                        st=''
                        estado=1

        elif estado == 3:
            if texto[atual].isnumeric():
                st=st+texto[atual]
                atual+=1
            else:
                if atual == len(texto):
                    Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Número','Linha':linha})
                    lista.append(Token)
                    st=''
                    estado=1
                else:
                    Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Número','Linha':linha})
                    lista.append(Token)
                    st = ''
                    estado = 1
        elif estado == 4:
            try:
                if texto[atual+1] == '=':
                    st = texto[atual]
                    estado = 5
                    atual+=1
                else:
                    st = texto[atual]
                    Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Sinal de Atribuição','Linha':linha})
                    lista.append(Token)
                    st = ''
                    estado = 1
                    atual+=1
            except IndexError:
                st = texto[atual]
                Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Sinal de Atribuição','Linha':linha})
                lista.append(Token)
                st = ''
                estado = 1
                atual+=1
        elif estado == 5:
            st = st + texto[atual]
            Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Sinal Composto de Atribuição','Linha':linha})
            lista.append(Token)
            st = ''
            estado = 1
            atual+=1
        elif estado == 6:
            if texto[atual] == '\n':
                linha+=1
                estado=1
                atual+=1
            else:
                atual+=1
        elif estado == 7:
            st = texto[atual]
            Token = dict({'Valor do Atributo':st,'Classe Gramátical':'Outro Caractere','Linha':linha})
            lista.append(Token)
            st = ''
            estado = 1
            atual+=1

    return lista
