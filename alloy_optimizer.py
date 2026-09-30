import pandas as pd
import numpy as np
import sys
import os
#
=======================================================================
=======
# ÁREA DE CONFIGURAÇÃO DO USUÁRIO
#
=======================================================================
=======
# 1. ESCOLHA QUAIS ÍNDICES CALCULAR (Adicione ou remova IDs da lista
abaixo)
MEUS_INDICES_ESCOLHIDOS = [1, 3, 5, 6, 8 ]
# 2. DEFINA OS PESOS PARA CADA ÍNDICE (ID : PESO)
# Se um índice não estiver nesta lista, o sistema assumirá PESO = 1
automaticamente.
PESOS_INDICES = {
1: 2, # Rigidez Específica (Parede Fina)
2: 2, # Rigidez Específica (Geral)
3: 2, # Resistência Específica
4: 2, # Tenacidade à Fratura
5: 5, # Rigidez por Custo
6: 5, # Resistência por Custo
7: 1, # Tenacidade Total
8: 1, # Rigidez Flexão (Fina)
9: 1, # Rigidez Flexão (Geral)
10: 1 # Rigidez Material (Simples)
}
# 3. CAMINHOS DE ARQUIVOS
NOME_ARQUIVO_ENTRADA = "D:/backup pc lukas 2026/Mestrado LUKAS/calculo
python/20-03-2026/Tabela de material.xlsx - lista para pro.csv"
NOME_ARQUIVO_SAIDA = "D:/backup pc lukas 2026/Mestrado LUKAS/calculo
python/20-03-2026/Resultado_Final.xlsx"
NOME_ARQUIVO_RANK = "D:/backup pc lukas 2026/Mestrado LUKAS/calculo
python/20-03-2026/Resultado_Final_Rank.xlsx"
# 4. PARÂMETROS GEOMÉTRICOS
L_PADRAO = 1.0

R_PADRAO = 0.05
T_PADRAO = 0.005
C1_PADRAO = 3.0
#
=======================================================================
=======
# FUNÇÕES DE APOIO
#
=======================================================================
=======
def to_float(x):
if isinstance(x, str):
x = x.replace('.', '').replace(',', '.')
return pd.to_numeric(x, errors='coerce')
def find_column(df, keywords):
for c in df.columns:
if any(k in c.lower() for k in keywords):
return c
return None
#
=======================================================================
=======
# CÓDIGO PRINCIPAL
#
=======================================================================
=======

def main():
print("="*60)
print(" INICIANDO CÁLCULO COMPLETO (10 ÍNDICES) + RANKING
PONDERADO")
print("="*60)
try:
df = pd.read_csv(NOME_ARQUIVO_ENTRADA, sep=None,
engine='python', encoding='utf-8')
except UnicodeDecodeError:
df = pd.read_csv(NOME_ARQUIVO_ENTRADA, sep=None,
engine='python', encoding='cp1252')

except Exception as e:
print(f"ERRO ao ler arquivo: {e}"); return
dff = df.copy()
dff.columns = dff.columns.str.strip()
col_material = dff.columns[0]
# --- MAPEAMENTO DINÂMICO ---
col_rho = find_column(dff, ["density", "densidade", "rho"])
col_young = find_column(dff, ["modulus", "elasticidade", "young",
"e_gpa", "módulo", "modulo"])
col_yield = find_column(dff, ["ys", "escoamento", "yield",
"sigma_y"])
col_k1c = find_column(dff, ["k1c", "tenacity", "tenacidade"])
col_energy = find_column(dff, ["energy", "energia",
"energia_total"])
col_cost = find_column(dff, ["cost", "custo", "preco", "preço"])
col_ref = find_column(dff, ["referencia", "reference", "ref"])
or dff.columns[-1]
# --- CONVERSÕES SI ---
if col_rho: dff["rho_SI"] = dff[col_rho].apply(to_float) *
1000.0
if col_young: dff["E_SI"] = dff[col_young].apply(to_float) * 1e9
if col_yield: dff["SigY_SI"] = dff[col_yield].apply(to_float) * 1e6
if col_k1c: dff["K1C_SI"] = dff[col_k1c].apply(to_float) * 1e6
if col_energy:dff["Ener_SI"] = dff[col_energy].apply(to_float)
if col_cost: dff["Cost_val"]= dff[col_cost].apply(to_float)
# Parâmetros Geométricos Auxiliares
Area_SI = 2 * np.pi * R_PADRAO * T_PADRAO
Inertia_SI = np.pi * (R_PADRAO**3) * T_PADRAO
indices_gerados = []
# --- CÁLCULO DOS 10 ÍNDICES ---
if 1 in MEUS_INDICES_ESCOLHIDOS:
dff["IM1_Rigidez_ParedeFina"] = (C1_PADRAO * (R_PADRAO**2) / (2
* L_PADRAO**4)) * (dff["E_SI"] / dff["rho_SI"])
indices_gerados.append("IM1_Rigidez_ParedeFina")
if 2 in MEUS_INDICES_ESCOLHIDOS:
dff["IM2_Rigidez_GeralSimp"] = np.sqrt(dff["E_SI"]) /
dff["rho_SI"]

indices_gerados.append("IM2_Rigidez_GeralSimp")
if 3 in MEUS_INDICES_ESCOLHIDOS:
dff["IM3_Resistencia_Esp"] = dff["SigY_SI"] / dff["rho_SI"]
indices_gerados.append("IM3_Resistencia_Esp")
if 4 in MEUS_INDICES_ESCOLHIDOS and col_k1c:
dff["IM4_Tenacidade_Fratura"] = (dff["K1C_SI"]**2) /
(dff["E_SI"] * dff["rho_SI"])
indices_gerados.append("IM4_Tenacidade_Fratura")
if 5 in MEUS_INDICES_ESCOLHIDOS and col_cost:
dff["IM5_Rigidez_Custo"] = dff["E_SI"] / dff["Cost_val"]
indices_gerados.append("IM5_Rigidez_Custo")
if 6 in MEUS_INDICES_ESCOLHIDOS and col_cost:
dff["IM6_Resistencia_Custo"] = dff["SigY_SI"] / dff["Cost_val"]
indices_gerados.append("IM6_Resistencia_Custo")
if 7 in MEUS_INDICES_ESCOLHIDOS and col_energy:
dff["IM7_Tenacidade_Total"] = dff["Ener_SI"] / dff["rho_SI"]
indices_gerados.append("IM7_Tenacidade_Total")
if 8 in MEUS_INDICES_ESCOLHIDOS:
dff["IM8_Rigidez_Flexao_Fina"] = (dff["E_SI"] * (R_PADRAO**2))
/ (dff["rho_SI"] * (L_PADRAO**4))
indices_gerados.append("IM8_Rigidez_Flexao_Fina")
if 9 in MEUS_INDICES_ESCOLHIDOS:
dff["IM9_Rigidez_Flexao_Geral"] = (C1_PADRAO * dff["E_SI"] *
Inertia_SI) / (dff["rho_SI"] * Area_SI * (L_PADRAO**4))
indices_gerados.append("IM9_Rigidez_Flexao_Geral")
if 10 in MEUS_INDICES_ESCOLHIDOS:
dff["IM10_Rigidez_Material_Simp"] = dff["E_SI"] / dff["rho_SI"]
indices_gerados.append("IM10_Rigidez_Material_Simp")
# --- LÓGICA DE RANKING PONDERADO ---
dff["PONTUACAO_TOTAL_PESO"] = 0.0
for im_col in indices_gerados:
try:
im_id = int(im_col.split('_')[0].replace('IM', ''))

peso = PESOS_INDICES.get(im_id, 1)
except: peso = 1
# Tratar NaNs para não quebrar o ranking
if dff[im_col].isnull().all(): continue
rank_temp = dff[im_col].rank(ascending=False, method='min')
dff[f"Rank_{im_col}"] = rank_temp
dff[f"Pontos_{im_col}"] = rank_temp * peso
dff["PONTUACAO_TOTAL_PESO"] +=
dff[f"Pontos_{im_col}"].fillna(0)
dff["RANK_GERAL_CAMPEAO"] =
dff["PONTUACAO_TOTAL_PESO"].rank(ascending=True, method='min')
# Limpeza de colunas SI
cols_si = ["rho_SI", "E_SI", "SigY_SI", "K1C_SI", "Ener_SI",
"Cost_val"]
dff.drop(columns=[c for c in cols_si if c in dff.columns],
inplace=True)
# --- SALVAMENTO ---
try:
dff.to_excel(NOME_ARQUIVO_SAIDA, index=False)
with pd.ExcelWriter(NOME_ARQUIVO_RANK) as writer:
df_campeao = dff.sort_values("RANK_GERAL_CAMPEAO").copy()
cols_c = [col_material, "RANK_GERAL_CAMPEAO",
"PONTUACAO_TOTAL_PESO", col_ref]
df_campeao[cols_c].head(50).to_excel(writer,
sheet_name="CAMPEAO GERAL", index=False)
for im_col in indices_gerados:
top_ind = dff.nsmallest(51,
f"Rank_{im_col}")[[col_material, im_col, f"Rank_{im_col}", col_ref]]
top_ind.to_excel(writer, sheet_name=im_col[:31],
index=False)
print(f"\n> SUCESSO!\n Arquivo Geral: {NOME_ARQUIVO_SAIDA}\n
Arquivo Campeão: {NOME_ARQUIVO_RANK}")
except Exception as e:
print(f"\nERRO ao salvar: {e}. Feche o Excel e tente
novamente.")

if __name__ == "__main__":
main()
