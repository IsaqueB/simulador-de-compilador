#PRIMEIRAMENTE SEPARAR EM TOKENS
def criar_all_tokens(text):
    all_tokens = []
    indice = 0
    token = ""
    while indice < len(text):
        try:
            if text[indice] == "<": #Encontrou um termo
                try:
                    token = ""
                    while(text[indice] != ">"):
                        token = token + text[indice]
                        indice += 1
                    if(text[indice] == ">"):
                        token = token + text[indice]
                        all_tokens.append(token)
                        indice += 1
                    else:
                        raise Exception
                except IndexError:
                    return "Erro na gramática, termo sem '>'"
                except:
                    print("Esperado '>'")
                    break
            elif text[indice] == ":":
                try:
                    token = text[indice]
                    indice+=1
                    if text[indice] == ":":
                        token = token + text[indice]
                        indice+=1
                        if text[indice] == "=":
                            token = token + text[indice]
                            all_tokens.append(token)
                            indice+=1
                        else:
                            raise Exception
                    else:
                        raise Exception
                except IndexError:
                    return "Erro na gramática, tentando acessar indice inexistente"
                except:
                    return 'Esperado "::="'
            elif text[indice] == '"':
                try:
                    aux = indice
                    token = text[indice]
                    indice+=1
                    while(text[indice] != '"'):
                        token = token + text[indice]
                        indice += 1
                    if(text[indice] == '"'):

                        token = token + text[indice]
                        all_tokens.append(token)
                        indice += 1
                    else:
                        raise Exception
                except IndexError:
                    return 'Erro na gramática, termo sem (") '
                except:
                    print('Esperado "')
                    break
            elif text[indice] == "|":
                all_tokens.append(text[indice])
                indice += 1
            elif text[indice] == " ":
                indice += 1
            elif text[indice] == "\n":
                indice += 1
            else:
                all_tokens.append(text[indice])
                indice += 1
        except:
            return "Erro encontrado verifique a definição da gramática BNF"

    return all_tokens

def identificar_regras(text):
    all_tokens = criar_all_tokens(text)
    regras_gramatica = []
    indice = 1
    associacao = []
    while indice < len(all_tokens):
        if all_tokens[indice] == "::=":
            nao_terminal = all_tokens[indice-1]
            indice+=2
            try:
                while indice < len(all_tokens):
                    if all_tokens[indice] != "::=":
                        associacao.append(all_tokens[indice-1])
                        indice += 1
                    else:
                        regras_gramatica.append(dict({"nao_terminal":nao_terminal,"::=":associacao}))
                        nao_terminal = all_tokens[indice-1]
                        associacao = []
                        indice+=2
                associacao.append(all_tokens[indice-1])
                regras_gramatica.append(dict({"nao_terminal":nao_terminal,"::=":associacao}))
            except IndexError:
                return "ERROR1"
        else:
            return "ERROR2"
    return regras_gramatica

def first(gramatica):
    gramatica = identificar_regras(gramatica)
    conjunto_de_first = []
    ##PRIMEIRAMENTE DESCOBRIR OS TERMINAIS E OS QUE COMEÇAM COM TERMINAIS
    indice = len(gramatica)-1
    while indice >= 0: #PERCORRER TODOS NÃO TERMINAIS
        firsts = []
        indice_2 = len(gramatica)-1
        encontrei_terminal = True
        while indice_2 >= 0:
            if gramatica[indice]["::="][0] == gramatica[indice_2]["nao_terminal"]:
                encontrei_terminal = False
                break
            indice_2 -= 1
        if encontrei_terminal:
            firsts.append(gramatica[indice]["::="][0])
        ##TESTANDO PARA VER SE TEM "|"
        try:
            for x in range(len(gramatica[indice]["::="])):
                if gramatica[indice]["::="][x] == "|": #Tem "OU". Percorrer lista de não terminais para ver se após o ou vem um terminal
                    indice_3 = len(gramatica)-1
                    encontrei_terminal = True
                    while indice_3 >= 0:
                        if gramatica[indice]["::="][x+1] == gramatica[indice_3]["nao_terminal"]:
                            encontrei_terminal = False
                            break
                        indice_3 -= 1
                    if encontrei_terminal:
                        firsts.append(gramatica[indice]["::="][x+1])
        except:
            return "ERRO"
        if len(firsts) > 0:
            conjunto_de_first.append(dict({"nt":gramatica[indice]["nao_terminal"],"first":firsts}))
        indice -= 1
    ##DESCOBRIR OS NÃO TERMINAIS QUE NÃO COMEÇAM COM TERMINAIS
    indice = len(gramatica)-1
    while indice >= 0:
        firsts = []
        indice_2 = len(conjunto_de_first)-1
        nao_encontrei = True #Variável que diz se foi ou não encontrado um elemento que não está na array conjunto_de_first
        while indice_2 >= 0:#Percorre conjunto_de_first para ver se gramatica[indice] já está armazenado
            if gramatica[indice]["nao_terminal"] == conjunto_de_first[indice_2]["nt"]:
                nao_encontrei = False
            indice_2 -= 1
        if nao_encontrei:#Se não encontrou então vai percorrer o conjunto_de_first de novo, mas dessa vez para pegar o first do seu primeiro não terminal
            indice_2 = len(conjunto_de_first)-1
            encontrei = False
            while indice_2 >= 0:
                if gramatica[indice]["::="][0] == conjunto_de_first[indice_2]["nt"]:
                    encontrei = True
                    for p in conjunto_de_first[indice_2]["first"]:
                        firsts.append(p)
                    break
                indice_2 -= 1
            if encontrei == False:
                return "ERRO3"
        #TESTANDO PRA VER SE TEM "|"
        try:
            for x in range(len(gramatica[indice]["::="])):
                if gramatica[indice]["::="][x] == "|": #Tem "OU". Percorrer lista de não terminais para ver se após o ou vem um não terminal
                    indice_3 = len(gramatica)-1
                    encontrei = False
                    while indice_3 >= 0:
                        if gramatica[indice]["::="][x+1] == gramatica[indice_3]["nao_terminal"]:
                            nao_encontrei = True
                        indice_3 -= 1
                    if nao_encontrei:
                        for y in conjunto_de_first:
                            if y["nt"] == gramatica[indice]["::="][x+1]:
                                for p in y["first"]:
                                    firsts.append(p)
                                break;
        except:
            return "ERRO"
        if len(firsts) > 0:
            x = 0
            z = 0
            o = False
            while x < len(conjunto_de_first):
                if gramatica[indice]["nao_terminal"] == conjunto_de_first[x]["nt"]:
                    o = True
                    z = x
                x += 1
            if o:
                aux = conjunto_de_first[z]
                conjunto_de_first.pop(z)
                y = 0
                while y < len(aux["first"]):
                    firsts.append(aux["first"][y])
                    y += 1
                conjunto_de_first.append(dict({"nt":gramatica[indice]["nao_terminal"],"first":firsts}))
            else:
                o = False
                conjunto_de_first.append(dict({"nt":gramatica[indice]["nao_terminal"],"first":firsts}))
        indice -= 1
    #REORGANIZANDO CONJUNTO_DE_FIRST
    nt = []
    conjunto_first = []
    for linha in gramatica:
        nt.append(linha["nao_terminal"])
    for elemento in nt:
        for linha in conjunto_de_first:
            if linha["nt"] == elemento:
                conjunto_first.append(linha)

    return conjunto_first

def follow(gramatica,conjunto_de_first):
    conjunto_follow = []
    nt = []
    gramatica = identificar_regras(gramatica)
    for linha in gramatica:
        nt.append(linha["nao_terminal"])
    conjunto_follow.append(dict({"nt":nt[0],"follow":"$"}))#REGRA1
    for linha in gramatica:
        follows = []
        for indice in range(len(linha["::="])):
            try:
                a = nt.index(linha["::="][indice])#CHECANDO SE É UM NÃO-TERMINAL
                #APLICANDO REGRA 2
                try:
                    if linha["::="][indice+1] in nt:
                        nt.index(linha["::="][indice+1])
                        for y in conjunto_de_first[nt.index(linha["::="][indice+1])]["first"]:
                            if (y != '""'):
                                conjunto_follow.append(dict({"nt":linha["::="][indice],"follow":y}))
                    else:
                        if linha["::="][indice+1] != '|':
                            conjunto_follow.append(dict({"nt":linha["::="][indice],"follow":linha["::="][indice+1]}))
                except:
                    pass
                #APLICANDO REGRA 3
                try:
                    aplicar_regra_3 = False
                    a = 0
                    if linha["::="][indice+1] in nt:
                        a = nt.index(linha["::="][indice+1])
                        if '""' in conjunto_de_first[a]["first"]:
                            aplicar_regra_3 = True
                    elif linha["::="][indice+1] == "|":
                        aplicar_regra_3 = True
                except IndexError: #QUER DIZER QUE É O ULTIMO DA LINHA
                    if linha["::="][indice] in nt: #SE É O ULTIMO DA LINHA E É UM NAO TERMINAL, APLICA-SE REGRA3 POR SER (alfa)B
                        aplicar_regra_3 = True
                if aplicar_regra_3:
                    if linha["::="][indice] != linha["nao_terminal"]:
                        conjunto_follow.append(dict({"nt":linha["::="][indice],"follow":("FOLLOW("+linha["nao_terminal"]+")")}))
            except:
                pass
    #JUNTANDO OS CONJUNTOS FOLLOW
    aux = conjunto_follow
    conjunto_follow = []
    for x in nt:
        follows = []
        for y in aux:
            if y["nt"] == x:
                print(y["nt"]+x)
                follows.append(y["follow"])
        conjunto_follow.append(dict({"nt":x,"follow":follows}))

    return conjunto_follow
arquivo = open('arquivo.txt','r')
f = arquivo.read()
arquivo.close()
a = first(f)
b = follow(f,a)
print("--------------")
for x in a:
    print(x)
print("-----------")
for x in b:
    print(x)
