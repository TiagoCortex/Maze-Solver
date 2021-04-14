def nums_validos(tuplo):
    if len(tuplo) != 0:
        if str(tuplo[0]) == '0' or str(tuplo[0]) == '1':
            return True and nums_validos(tuplo[1:])
        else:
            return False
    else:
        return True



def eh_coluna(tuplo):
    if isinstance(tuplo, tuple):
        if len(tuplo) >= 3:
            return nums_validos(tuplo)
        else:
            return False
    else:
        return False



def eh_labirinto(labirinto):
    if not isinstance(labirinto, tuple):
        return False
    if len(labirinto) < 3:
        return False
    dim_coluna = len(labirinto[0])
    for coluna in labirinto:
        if dim_coluna != len(coluna) or not eh_coluna(coluna):
            return False
    for i in range(len(labirinto)):
        if i == 0 or i == len(labirinto) - 1:
            if labirinto[i] != (1, )*dim_coluna: #dimensao da coluna
                return False
        else:
            if labirinto[i][0] != 1 or labirinto[i][-1] != 1:
                return False
    return True


def eh_posicao(tuplo):
    if not isinstance(tuplo, tuple) or len(tuplo) !=2 :
        return False
    for dig in tuplo:
        if type(dig) is not int or dig<0 :
            return False
    return True


def eh_conj_posicoes(tuplo):
    if not isinstance(tuplo, tuple) :
        return False
    comparacao = ()
    for coordenadas in tuplo:
        if not eh_posicao(coordenadas):
            return False
        if coordenadas not in comparacao:
            comparacao = comparacao + (coordenadas, )
        else:
            return False
    return True



def tamanho_labirinto(labirinto):
    if not eh_labirinto(labirinto):
        raise ValueError("tamanho labirinto: argumento invalido")
    else:
        return (len(labirinto), len(labirinto[0]))


def eh_mapa_valido(labirinto, conj_posicoes):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes):
        raise ValueError("eh mapa valido: algum dos argumentos e invalido")
    for coordenadas in conj_posicoes:
        if labirinto[coordenadas[0]][coordenadas[1]] == 1:
            return False
        if coordenadas[0] > tamanho_labirinto(labirinto)[0] or \
                coordenadas[1] > tamanho_labirinto(labirinto)[1]:
            return False
    return True


def eh_posicao_livre(labirinto, conj_posicoes, posicao):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes) or not eh_posicao(posicao):
        raise ValueError("eh posicao livre: algum dos argumentos e invalido")
    if posicao in conj_posicoes:
        return False
    if not eh_mapa_valido(labirinto, conj_posicoes + (posicao, )):
        return False
    return True



def posicoes_adjacentes(posicao):
    if not eh_posicao(posicao):
        raise ValueError("posicoes adjacentes: argumento invalido")
    if posicao[0] == 0 and posicao[1] != 0:
        return ((posicao[0],posicao[1] - 1), (posicao[0] + 1,posicao[1]), (posicao[0],posicao[1] + 1))
    elif posicao[0] != 0 and posicao[1] == 0:
        return ((posicao[0] - 1,posicao[1]), (posicao[0] + 1,posicao[1]), (posicao[0],posicao[1] + 1))
    elif posicao[0] == 0 and posicao[1] == 0:
        return ((posicao[0] + 1,posicao[1]), (posicao[0],posicao[1] + 1))
    else:
        return ((posicao[0] - 1,posicao[1]), (posicao[0],posicao[1] - 1),
                (posicao[0] + 1,posicao[1]), (posicao[0],posicao[1] + 1))


def mapa_str(labirinto, conj_posicoes):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes) or not eh_mapa_valido(labirinto, conj_posicoes):
        raise ValueError("mapa str: algum dos argumentos e invalido")

    lab = []
    for coluna in labirinto:
        col = list(coluna)
        lab = lab + [col, ]  #Transformacao dos tuplos em listas para poder alterar o seu conteudo

    for coordenada in conj_posicoes:
        lab[coordenada[0]][coordenada[1]] = 2  #Alterar os valores no labirinto onde existem unidades


    texto = ''
    i = 0
    while i < len(lab[0]):
        for col in lab:
            if str(col[i]) == '1':
                texto += '#'
            elif str(col[i]) == '0':
                texto += '.'
            elif str(col[i]) == '2':
                texto += 'O'

        texto += '\n'
        i += 1

    return texto



#Funcoes de movimento

def obter_objetivos(labirinto, conj_posicoes, posicao):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes) or not eh_posicao(posicao) \
            or not eh_mapa_valido(labirinto, conj_posicoes) or not eh_mapa_valido(labirinto, (posicao, )) :
        raise ValueError("obter objetivos: algum dos argumentos e invalido")

    lista_conj_posicoes = list(conj_posicoes)
    if posicao in lista_conj_posicoes:
        lista_conj_posicoes.remove(posicao)

    posic_adjacentes = posicoes_adjacentes(lista_conj_posicoes[0])
    print(posic_adjacentes)

                                                                            #provavelmente terei que alterar para os limites do mapa
    for unidade in range(1, len(lista_conj_posicoes)):
        posic_adjacentes = posic_adjacentes + (posicoes_adjacentes(unidade), )
    print(posic_adjacentes)

    res = ()
    for coordenada in posic_adjacentes:
        if eh_posicao_livre(labirinto, conj_posicoes, coordenada):
            res = res + (coordenada, )
    return res



def obter_caminho(labirinto, conj_posicoes, posicao):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes) or not eh_posicao(posicao) or not eh_mapa_valido(labirinto, conj_posicoes) or not eh_mapa_valido(labirinto, (posicao, )) or posicao not in conj_posicoes:
        raise ValueError("obter caminho: algum dos argumentos e invalido")

    if conj_posicoes == (posicao,):
        return ()


    else:
        lista_conj_posicoes = list(conj_posicoes)
        lista_conj_posicoes.remove(posicao)

    possiveis_objetivos = posicoes_adjacentes(lista_conj_posicoes[0])
    for i in range(len(lista_conj_posicoes)):
        for elemento in posicoes_adjacentes(lista_conj_posicoes[i]):
            if elemento not in possiveis_objetivos:
                possiveis_objetivos = possiveis_objetivos + (posicoes_adjacentes(lista_conj_posicoes[i]), )


    caminho_atual = []
    posicoes_visitadas = []
    ele_fila_exploracao = [posicao, []]
    fila_exploracao = [ele_fila_exploracao]
    posicao_atual = posicao
    while fila_exploracao != []:
        posicao_atual = fila_exploracao[0][0]
        caminho_atual = fila_exploracao[0][1]
        if posicao_atual not in posicoes_visitadas:
            posicoes_visitadas = posicoes_visitadas + [posicao_atual, ]
            caminho_atual = caminho_atual + [posicao_atual, ]
            if posicao_atual in possiveis_objetivos:
                return caminho_atual
            else:
                for pos in posicoes_adjacentes(posicao_atual):
                    if eh_posicao_livre(labirinto, conj_posicoes, pos):
                        fila_exploracao = fila_exploracao + [[pos, caminho_atual]]
        fila_exploracao.remove(fila_exploracao[0])
    return ()



def index_pos_lista(lista, pos):
    if len(lista) != 0:
        if lista[0] != pos:
            return 1 + index_pos_lista(lista[1:], pos)
        else:
            return 0
    return 0

print(index_pos_lista([1,2,3,4,5], 4))
print(len([1,2,3,4,5]))





def mover_unidade(labirinto, conj_posicoes, posicao):
    if not eh_labirinto(labirinto) or not eh_conj_posicoes(conj_posicoes) or not eh_posicao(posicao) or not obter_caminho(labirinto, conj_posicoes, posicao):
        raise ValueError("mover unidade: algum dos argumentos e invalido")

    caminho = obter_caminho(labirinto, conj_posicoes, posicao)
    lista_conj_posicoes = list(conj_posicoes)
    for i in range(len(lista_conj_posicoes)):
        if lista_conj_posicoes[i] == posicao:
            index = index_pos_lista(caminho, lista_conj_posicoes[i])
            if index < len(caminho) -1:
                lista_conj_posicoes[i] = caminho[index + 1]
                return tuple(lista_conj_posicoes)
            return tuple(lista_conj_posicoes)

maze = ((1,1,1,1,1),(1,0,0,0,1),(1,0,0,0,1),(1,0,0,0,1),
(1,0,0,0,1),(1,0,0,0,1),(1,1,1,1,1))
unidades = ((2,1),(4,3))
print(mapa_str(maze, unidades))

unidades = mover_unidade(maze, unidades, unidades[0])
print(mapa_str(maze, unidades))

unidades = mover_unidade(maze, unidades, unidades[1])
print(mapa_str(maze, unidades))

unidades = mover_unidade(maze, unidades, unidades[0])
print(mapa_str(maze, unidades))

unidades = mover_unidade(maze, unidades, unidades[1])
print(mapa_str(maze, unidades))











