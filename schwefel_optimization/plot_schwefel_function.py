# -*- coding: utf-8 -*-
"""
Script para visualizar a função Schwefel em 2D e 3D.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from datetime import datetime

# Define a função Schwefel para n dimensões
def schwefel_func(x):
    n = len(x)
    term1 = 418.9829 * n
    term2 = np.sum(x * np.sin(np.sqrt(np.abs(x))))
    return term1 - term2

# Cria diretório para salvar os plots se não existir
output_dir = "schwefel_plots"
os.makedirs(output_dir, exist_ok=True)

# --- Gráfico 2D (Contorno) ---
print("[Schwefel Plotting] Gerando gráfico 2D da função Schwefel...")

x = np.linspace(-500, 500, 400)
y = np.linspace(-500, 500, 400)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

# Calcula Z para cada ponto da grade
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = schwefel_func([X[i, j], Y[i, j]])

plt.figure(figsize=(10, 8))
# Corrigido: Removido escape desnecessário
contour = plt.contourf(X, Y, Z, levels=50, cmap="viridis") 
plt.colorbar(contour, label="Valor da Função Schwefel f(x, y)")
plt.title("Função Schwefel em 2D (Contorno)")
plt.xlabel("x1")
plt.ylabel("x2")
# Corrigido: Removido escape desnecessário
plt.plot(420.9687, 420.9687, "ro", markersize=8, label="Mínimo Global (aprox.)") 
plt.legend()
# Corrigido: Removido escape desnecessário
plt.grid(True, linestyle="--", alpha=0.6) 

# Salva o gráfico 2D
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Corrigido: Removido escape desnecessário
filename_2d = f"{output_dir}/schwefel_function_2d_{timestamp}.png" 
plt.savefig(filename_2d, bbox_inches="tight", dpi=300)
# Corrigido: Removido escape desnecessário
print(f"[Schwefel Plotting] Gráfico 2D salvo em: {filename_2d}") 
plt.close()

# --- Gráfico 3D (Superfície) ---
print("[Schwefel Plotting] Gerando gráfico 3D da função Schwefel...")

fig = plt.figure(figsize=(12, 9))
# Corrigido: Removido escape desnecessário
ax = fig.add_subplot(111, projection="3d") 

# Plota a superfície
# Corrigido: Removido escape desnecessário
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none", alpha=0.8) 

# Adiciona o ponto mínimo global
min_x, min_y = 420.9687, 420.9687
min_z = schwefel_func([min_x, min_y])
# Corrigido: Removido escape desnecessário
ax.scatter(min_x, min_y, min_z, color="red", s=100, label="Mínimo Global (aprox.)", depthshade=True) 

# Configurações do gráfico 3D
ax.set_title("Função Schwefel em 3D (Superfície)")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_zlabel("f(x1, x2)")
ax.view_init(elev=30, azim=120) # Ajusta o ângulo de visão
fig.colorbar(surf, shrink=0.5, aspect=5, label="Valor da Função Schwefel")
ax.legend()

# Salva o gráfico 3D
# Corrigido: Removido escape desnecessário
filename_3d = f"{output_dir}/schwefel_function_3d_{timestamp}.png" 
plt.savefig(filename_3d, bbox_inches="tight", dpi=300)
# Corrigido: Removido escape desnecessário
print(f"[Schwefel Plotting] Gráfico 3D salvo em: {filename_3d}") 
plt.close()

print("[Schwefel Plotting] Gráficos 2D e 3D da função Schwefel gerados com sucesso.")

