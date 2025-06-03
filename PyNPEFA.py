import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyNPEFA import PyNPEFA

def run_inpefa_analysis():
    # Fazer upload do arquivo Excel pelo usuário (no Google Colab)
    from google.colab import files
    uploaded = files.upload()

    # Pega o nome do arquivo enviado
    filename = list(uploaded.keys())[0]

    # Ler os dados Excel (com decimal ',')
    data = pd.read_excel(filename, decimal=',')

    # Garantir que as colunas são séries do Pandas
    y = data['GR'].dropna()      # Proxy de análise (original GR)
    x = data['Depth'].dropna()   # Coluna de profundidade

    # Executar a análise INPEFA
    inpefa_log = PyNPEFA(y, x)

    # Adicionar a profundidade ao resultado para exportar
    inpefa_log['Depth'] = x

    # Criar DataFrame com os resultados
    df_inpefa = pd.DataFrame({
        'Depth': inpefa_log['Depth'],
        'OG': inpefa_log['OG'],  # Curva GR original
        'Long Term INPEFA': inpefa_log['1'],  # Longo prazo INPEFA
        'Mid Term INPEFA': inpefa_log['2'],   # Médio prazo INPEFA
        'Short Term INPEFA': inpefa_log['3'], # Curto prazo INPEFA
        'Shorter Term INPEFA': inpefa_log['4'] # Prazo mais curto INPEFA
    })

    # Exportar os resultados para CSV (na pasta atual do Colab)
    output_csv = 'inpefa_resultados.csv'
    df_inpefa.to_csv(output_csv, index=False, sep=';', decimal=',')
    print(f'Resultados salvos em: {output_csv}')

    # Plotar os gráficos
    fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(18, 16), dpi=300)

    axes[0].plot(inpefa_log['OG'], x)  # Curva GR original
    axes[0].grid(True)
    axes[0].set_xlabel('GR (API)')
    axes[0].set_ylabel('Depth (ft)')
    axes[0].set_xlim((0, 150))
    axes[0].set_title('Original GR Curve')

    axes[1].plot(inpefa_log['1'], x)  # Longo prazo INPEFA
    axes[1].grid(True)
    axes[1].set_xlim((-1, 1))
    axes[1].set_title('Long Term INPEFA')

    axes[2].plot(inpefa_log['2'], x)  # Médio prazo INPEFA
    axes[2].grid(True)
    axes[2].set_xlim((-1, 1))
    axes[2].set_title('Mid Term INPEFA')

    axes[3].plot(inpefa_log['3'], x)  # Curto prazo INPEFA
    axes[3].grid(True)
    axes[3].set_xlim((-1, 1))
    axes[3].set_title('Short Term INPEFA')

    axes[4].plot(inpefa_log['4'], x)  # Prazo mais curto INPEFA
    axes[4].grid(True)
    axes[4].set_xlim((-1, 1))
    axes[4].set_title('Shorter Term INPEFA')

    fig.tight_layout()

    # Salvar o gráfico como PNG (na pasta atual do Colab)
    output_png = 'Resultados-Imagens.png'
    fig.savefig(output_png, format='png', dpi=300, bbox_inches='tight')
    print(f'Gráfico salvo em: {output_png}')

    # Para facilitar o download no Colab
    files.download(output_csv)
    files.download(output_png)

# Só rodar a função
if __name__ == "__main__":
    run_inpefa_analysis()
