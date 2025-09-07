import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import getpass # Para mascarar a senha

def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados de um arquivo CSV, realiza a limpeza inicial e trata erros.
    """
    try:
        df = pd.read_csv(caminho_arquivo, parse_dates=['Data'])
        print(f"Arquivo '{caminho_arquivo}' carregado com sucesso.")
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df['Custo_Produto'] = pd.to_numeric(df['Custo_Produto'], errors='coerce')
        df.dropna(subset=['Valor', 'Custo_Produto'], inplace=True)
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar os dados: {e}")
        return None

def analisar_dados(df: pd.DataFrame) -> dict:
    """
    Recebe um DataFrame e retorna um dicionário com os principais insights.
    """
    if df is None or df.empty:
        print("Análise não pode ser realizada: dados de entrada inválidos.")
        return None
    print("Iniciando a análise dos dados...")
    df['Lucro'] = df['Valor'] - df['Custo_Produto']
    insights = {
        "lucro_total": df['Lucro'].sum(),
        "produto_mais_vendido": df['Produto'].mode()[0],
        "vendas_por_canal": df['Canal_Venda'].value_counts().to_dict(),
        "satisfacao_media": df['Satisfacao_Cliente'].mean(),
        "total_vendas": len(df)
    }
    print("Análise concluída.")
    return insights

def gerar_grafico(df: pd.DataFrame, caminho_saida: str):
    """
    Gera um gráfico de barras das vendas por canal e o salva como um arquivo PNG.
    """
    if df is None or df.empty:
        print("Não foi possível gerar o gráfico: DataFrame vazio.")
        return False
    print("Gerando gráfico de vendas por canal...")
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        vendas_por_canal = df['Canal_Venda'].value_counts()
        vendas_por_canal.plot(kind='bar', ax=ax, color=['#4a90e2', '#e27c4a'])
        ax.set_title('Total de Vendas por Canal', fontsize=16, pad=20)
        ax.set_xlabel('Canal de Venda', fontsize=12)
        ax.set_ylabel('Número de Vendas', fontsize=12)
        ax.tick_params(axis='x', rotation=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.savefig(caminho_saida)
        plt.close(fig)
        print(f"Gráfico salvo com sucesso em: {caminho_saida}")
        return True
    except Exception as e:
        print(f"ERRO ao gerar o gráfico: {e}")
        return False

def criar_pdf_relatorio(nome_pdf: str, insights: dict, caminho_grafico: str):
    """
    Cria um relatório em PDF bem formatado com os insights e o gráfico gerado.
    """
    if not insights:
        print("Não foi possível criar o PDF: insights vazios.")
        return False
    print(f"Criando relatório PDF: {nome_pdf}...")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 15, "Relatório de Análise de Vendas", 0, 1, "C")
        pdf.ln(10)

        # Seção de Insights
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Principais Insights:", 0, 1, 'L')
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, f"- Lucro Total: R$ {insights['lucro_total']:,.2f}".replace(",", "."))
        pdf.multi_cell(0, 8, f"- Produto Mais Vendido: {insights['produto_mais_vendido']}")
        pdf.multi_cell(0, 8, f"- Satisfação Média do Cliente: {insights['satisfacao_media']:.2f} / 5.0")
        pdf.multi_cell(0, 8, "- Vendas por Canal:")
        for canal, quantidade in insights['vendas_por_canal'].items():
            pdf.multi_cell(0, 8, f"    - {canal}: {quantidade} vendas")
        pdf.ln(15)

        # Seção do Gráfico
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Visualização Gráfica:", 0, 1, 'L')
        pdf.image(caminho_grafico, x=pdf.get_x(), y=pdf.get_y(), w=pdf.w - 20)

        pdf.output(nome_pdf)
        print(f"PDF '{nome_pdf}' criado com sucesso.")
        return True
    except Exception as e:
        print(f"ERRO ao criar o PDF: {e}")
        return False

def enviar_email(remetente_email: str, remetente_senha: str, destinatario_email: str, nome_pdf: str):
    """
    Configura e envia o relatório PDF por e-mail usando o servidor SMTP do Gmail.
    """
    print(f"Preparando para enviar e-mail para {destinatario_email}...")
    msg = MIMEMultipart()
    msg['From'] = remetente_email
    msg['To'] = destinatario_email
    msg['Subject'] = "Seu Relatório de Análise de Vendas está Pronto!"

    corpo_email = "Olá,\n\nAnexamos a este e-mail o relatório de análise de vendas solicitado.\n\nEle contém os principais insights extraídos dos dados e uma visualização gráfica para facilitar a compreensão.\n\nAtenciosamente,\nSender.py - Seu Assistente de Análise"
    msg.attach(MIMEText(corpo_email, 'plain'))

    try:
        with open(nome_pdf, "rb") as attachment:
            part = MIMEApplication(attachment.read(), _subtype="pdf")
            part.add_header('Content-Disposition', 'attachment', filename=nome_pdf)
            msg.attach(part)
        print(f"Anexo '{nome_pdf}' adicionado ao e-mail.")
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo PDF '{nome_pdf}' não foi encontrado para ser anexado.")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente_email, remetente_senha)
        server.send_message(msg)
        server.quit()
        print("\nE-mail enviado com sucesso!")
    except smtplib.SMTPAuthenticationError:
        print("\nERRO DE AUTENTICAÇÃO: E-mail ou senha de app incorretos.")
        print("Verifique suas credenciais e certifique-se de que a senha de app é válida.")
    except Exception as e:
        print(f"\nERRO ao enviar e-mail: {e}")

if __name__ == "__main__":
    print("\n--- Ferramenta de Análise e Envio de Relatórios ---")
    print("Este script analisa um arquivo 'sales.csv', gera um relatório em PDF e o envia por e-mail.")

    # --- Coleta de Informações do Usuário ---
    print("\nPor favor, forneça as seguintes informações:")
    email_remetente = input("Seu e-mail do Gmail (remetente): ")
    # Usando getpass para não exibir a senha na tela enquanto o usuário digita
    senha_app = getpass.getpass("Sua senha de app do Google: ")
    email_destinatario = input("E-mail do destinatário: ")
    nome_pdf_output = input("Nome do arquivo PDF a ser gerado (ex: relatorio.pdf): ")

    # --- Definição de Nomes de Arquivos ---
    ARQUIVO_CSV = 'planilhas/sales2.csv'
    ARQUIVO_GRAFICO = 'grafico_vendas.png'

    # --- Orquestração do Processo ---
    print("\nIniciando processo...")
    dados = carregar_dados(ARQUIVO_CSV)
    if dados is not None:
        insights = analisar_dados(dados)
        if insights is not None:
            if gerar_grafico(dados, ARQUIVO_GRAFICO):
                if criar_pdf_relatorio(nome_pdf_output, insights, ARQUIVO_GRAFICO):
                    enviar_email(email_remetente, senha_app, email_destinatario, nome_pdf_output)

    print("\n--- Processo Concluído ---")