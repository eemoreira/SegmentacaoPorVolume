import numpy as np
import pickle
import sys
import matplotlib.pyplot as plt

directions = [
    (1, 0, 0), (-1, 0, 0),  # faces no eixo x
    (0, 1, 0), (0, -1, 0),  # faces no eixo y
    (0, 0, 1), (0, 0, -1),  # faces no eixo z
    (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),  # arestas xy
    (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),  # arestas xz
    (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)   # arestas yz
]

sys.setrecursionlimit(1000000)

with open('volume_TAC', 'rb') as f:
    volume = pickle.load(f)


def valid(i, j, k):
    return i >= 0 and i < len(volume) and j >= 0 and j < len(volume[i]) and k >= 0 and k < len(volume[i][j])



def GetGroups(lookfor):
    vis = np.zeros_like(volume, dtype=bool)

    component = []
    def dfs(i, j, k, looking):
        if (not valid(i, j, k)) or vis[i][j][k] or volume[i][j][k] != looking:
            return 0
        cnt = 1
        vis[i][j][k] = True
        component.append((i, j, k))
        for ii, jj, kk in directions:
                    nxt_i = i + ii
                    nxt_j = j + jj
                    nxt_k = k + kk
                    cnt += dfs(nxt_i, nxt_j, nxt_k, looking)
        return cnt

    groups = []
    max_group = []
    for i in range(0, len(volume)):
        for j in range(0, len(volume[i])):
            for k in range(0, len(volume[i][j])):
                if (not vis[i][j][k]) and volume[i][j][k] == lookfor:
                    component = []
                    group = dfs(i, j, k, lookfor)
                    groups.append(group)
                    if len(max_group) < len(component):
                        max_group = component
    return groups, max_group


def show(group, name):
    mask = np.zeros_like(volume, dtype=bool)
    for vx, vy, vz in group:
        mask[vx, vy, vz] = True

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plotar os voxels do maior agrupamento
    ax.voxels(mask, facecolors='red', edgecolor='k')

    ax.set_title(f'Visualização 3D do Maior Agrupamento de Células {name}')
    plt.savefig(f'maior_agrupamento_{name}_18conectividade.png', format='png', dpi=300)


PROLIFERATIVA = 255
QUIESCENTE = 200
NECROTICA = 140

total_proliferativas = np.sum(volume == PROLIFERATIVA)
total_quiescentes = np.sum(volume == QUIESCENTE)
total_necroticas = np.sum(volume == NECROTICA)

print(f'Total de células proliferativas: {total_proliferativas}')
print(f'Total de células quiescentes: {total_quiescentes}')
print(f'Total de células necróticas: {total_necroticas}')

proliferativas_grupos, proliferativas_max_grupo = GetGroups(PROLIFERATIVA)
quiescentes_grupos, quiescentes_max_grupo = GetGroups(QUIESCENTE)
necroticas_grupos, necroticas_max_grupo = GetGroups(NECROTICA)

print(f'Grupos de células proliferativas: {proliferativas_grupos}')
print(f'Grupos de células quiescente: {quiescentes_grupos}')
print(f'Grupos de células necróticas: {necroticas_grupos}')

print(f'Maior grupo de células proliferativas: {len(proliferativas_max_grupo)}')
print(f'Maior grupo de células quiescente: {len(quiescentes_max_grupo)}')
print(f'Maior grupo de células necróticas: {len(necroticas_max_grupo)}')

show(proliferativas_max_grupo, "proliferativas")
show(quiescentes_max_grupo, "quiscentes")
show(necroticas_max_grupo, "necroticas")
