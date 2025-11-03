import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def gerar_relatorio(caminho_excel):
    # Lê planilha
    df = pd.read_csv(caminho_excel, sep=',', encoding='utf-8', on_bad_lines='skip')

    # Trata dados
    tratar_dados(df)
    
    # Cálculos
    total = df['QUANTITYORDERED'].sum()
    media = df['QUANTITYORDERED'].mean()
    media = round(media, 2)
    mais_vendido = df.groupby('PRODUCTCODE')['QUANTITYORDERED'].sum().idxmax()

    # Gráfico
    grafico_path = "output/grafico.png"
    df.groupby('PRODUCTLINE')['QUANTITYORDERED'].sum().plot(kind='bar')
    plt.title('Produto mais vendido')
    plt.tight_layout()
    plt.savefig(grafico_path)
    plt.close()

    # PDF
    nome_pdf = f"relatorio_vendas_{datetime.now().strftime('%d%m%Y')}.pdf"
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    c.drawString(50, 800, f"Relatório de Vendas - {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(50, 770, f"Total de produtos vendidos: {total}")
    c.drawString(50, 750, f"Ticket Médio: R$ {media}")
    c.drawString(50, 730, f"Codigo do produto mais vendido: {mais_vendido}")
    c.drawImage(grafico_path, 50, 450, width=500, height=250, preserveAspectRatio=True)
    c.save()

    print(f"Relatório gerado: {nome_pdf}")
    
def tratar_dados(df):
    df['SALES'] = pd.to_numeric(df['SALES'], errors='coerce').fillna(0)
    df['QUANTITYORDERED'] = pd.to_numeric(df['QUANTITYORDERED'], errors='coerce').fillna(0)
    
    

if __name__ == "__main__":
    gerar_relatorio("data/sales_data_sample.csv")