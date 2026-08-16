# ============================================================
# PROJETO DE ANÁLISE DE DADOS - COVID-19 NO BRASIL
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------------
# 1. CAMINHO DOS ARQUIVOS
# ------------------------------------------------------------

arquivo = r"C:\Users\User\Documents\HIST_PAINEL_COVIDBR_\HIST_PAINEL_COVIDBR_.csv"

pasta_projeto = r"C:\Users\User\Documents\Projeto_Covid19"
pasta_graficos = os.path.join(pasta_projeto, "Graficos")

os.makedirs(pasta_graficos, exist_ok=True)


# ------------------------------------------------------------
# 2. LEITURA DOS DADOS
# ------------------------------------------------------------

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="utf-8-sig"
)

print("\n========== DADOS CARREGADOS ==========")
print(df.head())

print("\nQuantidade de linhas e colunas:")
print(df.shape)


# ------------------------------------------------------------
# 3. TRATAMENTO DA DATA
# ------------------------------------------------------------

df["data"] = pd.to_datetime(df["data"], errors="coerce")

df = df.dropna(subset=["data"])


# ------------------------------------------------------------
# 4. ANÁLISE POR ESTADO
# ------------------------------------------------------------

df_estados = df[df["estado"].notna()].copy()

# Último registro disponível de cada estado
ultimo_registro = (
    df_estados
    .sort_values("data")
    .groupby("estado")
    .tail(1)
)

ultimo_registro = ultimo_registro.sort_values(
    "casosAcumulado",
    ascending=False
)


# ------------------------------------------------------------
# 5. ESTADO COM MAIS CASOS
# ------------------------------------------------------------

estado_mais_casos = ultimo_registro.iloc[0]["estado"]
maior_numero_casos = ultimo_registro.iloc[0]["casosAcumulado"]

print("\n========== CASOS ACUMULADOS ==========")
print("Estado com mais casos:", estado_mais_casos)
print("Número de casos:", maior_numero_casos)


# ------------------------------------------------------------
# 6. ESTADO COM MAIS ÓBITOS
# ------------------------------------------------------------

ultimo_obitos = ultimo_registro.sort_values(
    "obitosAcumulado",
    ascending=False
)

estado_mais_obitos = ultimo_obitos.iloc[0]["estado"]
maior_numero_obitos = ultimo_obitos.iloc[0]["obitosAcumulado"]

print("\n========== ÓBITOS ACUMULADOS ==========")
print("Estado com mais óbitos:", estado_mais_obitos)
print("Número de óbitos:", maior_numero_obitos)


# ------------------------------------------------------------
# 7. GRÁFICO - CASOS POR ESTADO
# ------------------------------------------------------------

top10_casos = ultimo_registro.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top10_casos["estado"],
    top10_casos["casosAcumulado"]
)

plt.title("Top 10 Estados com Mais Casos de COVID-19")
plt.xlabel("Estado")
plt.ylabel("Casos acumulados")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "casos_por_estado.png"),
    dpi=300
)

plt.show()


# ------------------------------------------------------------
# 8. GRÁFICO - ÓBITOS POR ESTADO
# ------------------------------------------------------------

top10_obitos = ultimo_obitos.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top10_obitos["estado"],
    top10_obitos["obitosAcumulado"]
)

plt.title("Top 10 Estados com Mais Óbitos por COVID-19")
plt.xlabel("Estado")
plt.ylabel("Óbitos acumulados")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "obitos_por_estado.png"),
    dpi=300
)

plt.show()


# ------------------------------------------------------------
# 9. EVOLUÇÃO DOS CASOS AO LONGO DO TEMPO
# ------------------------------------------------------------

df_brasil = df[
    (df["regiao"] == "Brasil") &
    (df["estado"].isna())
].copy()

casos_tempo = (
    df_brasil
    .groupby("data")["casosNovos"]
    .sum()
)

plt.figure(figsize=(12, 6))

plt.plot(
    casos_tempo.index,
    casos_tempo.values
)

plt.title("Evolução dos Novos Casos de COVID-19 no Brasil")
plt.xlabel("Data")
plt.ylabel("Novos casos")

plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "evolucao_casos.png"),
    dpi=300
)

plt.show()


# ------------------------------------------------------------
# 10. EVOLUÇÃO DOS ÓBITOS
# ------------------------------------------------------------

obitos_tempo = (
    df_brasil
    .groupby("data")["obitosNovos"]
    .sum()
)

plt.figure(figsize=(12, 6))

plt.plot(
    obitos_tempo.index,
    obitos_tempo.values
)

plt.title("Evolução dos Novos Óbitos por COVID-19 no Brasil")
plt.xlabel("Data")
plt.ylabel("Novos óbitos")

plt.tight_layout()

plt.savefig(
    os.path.join(pasta_graficos, "evolucao_obitos.png"),
    dpi=300
)

plt.show()


# ------------------------------------------------------------
# 11. POPULAÇÃO X CASOS
# ------------------------------------------------------------

populacao_casos = ultimo_registro[
    ["estado", "populacaoTCU2019", "casosAcumulado"]
].copy()

populacao_casos = populacao_casos.dropna()

populacao_casos["percentual_casos"] = (
    populacao_casos["casosAcumulado"]
    / populacao_casos["populacaoTCU2019"]
) * 100

populacao_casos = populacao_casos.sort_values(
    "percentual_casos",
    ascending=False
)

print("\n========== POPULAÇÃO X CASOS ==========")
print(populacao_casos.head(10))


# ------------------------------------------------------------
# 12. RECUPERAÇÕES
# ------------------------------------------------------------

if "Recuperadosnovos" in df.columns:

    recuperados_tempo = (
        df_brasil
        .groupby("data")["Recuperadosnovos"]
        .max()
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        recuperados_tempo.index,
        recuperados_tempo.values
    )

    plt.title("Evolução dos Recuperados de COVID-19 no Brasil")
    plt.xlabel("Data")
    plt.ylabel("Recuperados")

    plt.tight_layout()

    plt.savefig(
        os.path.join(pasta_graficos, "evolucao_recuperados.png"),
        dpi=300
    )

    plt.show()


# ------------------------------------------------------------
# 13. SALVAR RESULTADO FINAL
# ------------------------------------------------------------

resultado_final = pd.DataFrame({
    "indicador": [
        "Estado com mais casos",
        "Maior número de casos acumulados",
        "Estado com mais óbitos",
        "Maior número de óbitos acumulados"
    ],
    
    "resultado": [
        estado_mais_casos,
        maior_numero_casos,
        estado_mais_obitos,
        maior_numero_obitos
    ]
})

resultado_final.to_csv(
    os.path.join(
        pasta_projeto,
        "resultado_final_covid.csv"
    ),
    index=False,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# 14. RESUMO FINAL
# ------------------------------------------------------------

print("\n")
print("==============================================")
print("       RESUMO DO PROJETO COVID-19")
print("==============================================")

print("Maior número de casos acumulados:", estado_mais_casos)
print("Quantidade de casos:", maior_numero_casos)

print("Maior número de óbitos acumulados:", estado_mais_obitos)
print("Quantidade de óbitos:", maior_numero_obitos)

print("\nArquivos salvos em:")
print(pasta_projeto)

print("\nGráficos salvos em:")
print(pasta_graficos)

print("\n========== PROJETO CONCLUÍDO ==========")
