# 📊 Sender.py - Ferramenta de Análise e Envio de Relatórios de Vendas

## 📋 Visão Geral

O **Sender.py** é uma ferramenta automatizada de análise de dados que processa arquivos CSV de vendas, gera insights empresariais, cria visualizações gráficas e envia relatórios em PDF por e-mail. Ideal para analistas de dados, engenheiros de dados e profissionais de negócios que precisam automatizar a geração e distribuição de relatórios de vendas.

## 🚀 Funcionalidades Principais

- **📈 Análise Automatizada**: Processa dados de vendas e calcula métricas importantes
- **📊 Visualização Gráfica**: Gera gráficos profissionais usando matplotlib
- **📄 Relatórios em PDF**: Cria relatórios formatados com FPDF
- **📧 Envio Automatizado**: Envia relatórios por e-mail via SMTP do Gmail
- **🔒 Segurança**: Mascara senhas durante a entrada de dados
- **⚡ Tratamento de Erros**: Sistema robusto de tratamento de exceções

## 📦 Pré-requisitos

### Dependências Python

```bash
pip install pandas matplotlib fpdf2
```

### Bibliotecas Padrão (incluídas no Python)

- `smtplib` - Para envio de e-mails
- `email.mime.*` - Para formatação de e-mails
- `getpass` - Para entrada segura de senhas

### Configuração do Gmail

1. Ative a **verificação em duas etapas** na sua conta Google
2. Gere uma **senha de app** específica para este projeto
3. Use essa senha de app no script (não sua senha principal)

## 📁 Estrutura do Projeto

```
Sender/
├── Sender.py                 # Script principal
├── planilhas/
│   ├── sales.csv            # Arquivo de dados de exemplo
│   └── sales2.csv           # Arquivo de dados alternativo
├── grafico_vendas.png       # Gráfico gerado automaticamente
└── README.md               # Esta documentação
```

## 📊 Formato dos Dados de Entrada

O script espera um arquivo CSV com as seguintes colunas:

| Coluna               | Tipo    | Descrição        | Exemplo     |
| -------------------- | ------- | ---------------- | ----------- |
| `Data`               | Date    | Data da venda    | 2024-01-15  |
| `Produto`            | String  | Nome do produto  | "Produto A" |
| `Valor`              | Float   | Valor da venda   | 150.50      |
| `Custo_Produto`      | Float   | Custo do produto | 100.00      |
| `Canal_Venda`        | String  | Canal de venda   | "Online"    |
| `Satisfacao_Cliente` | Integer | Avaliação (1-5)  | 4           |

### Exemplo de CSV:

```csv
Data,Produto,Valor,Custo_Produto,Canal_Venda,Satisfacao_Cliente
2024-01-15,Produto A,150.50,100.00,Online,4
2024-01-16,Produto B,200.00,120.00,Loja Física,5
```

## 🛠️ Como Usar

### 1. Preparação dos Dados

1. Coloque seu arquivo CSV na pasta `planilhas/`
2. Certifique-se de que o arquivo segue o formato esperado
3. Verifique se todas as colunas obrigatórias estão presentes

### 2. Execução do Script

```bash
python Sender.py
```

### 3. Entrada de Dados

O script solicitará:

- **E-mail do Gmail**: Seu e-mail para envio
- **Senha de App**: Senha de aplicativo do Google (não será exibida)
- **E-mail Destinatário**: Para quem enviar o relatório
- **Nome do PDF**: Nome do arquivo de saída (ex: `relatorio.pdf`)

### 4. Processo Automatizado

1. ✅ Carregamento dos dados
2. ✅ Análise e cálculo de insights
3. ✅ Geração de gráficos
4. ✅ Criação do PDF
5. ✅ Envio por e-mail

## 📈 Insights Gerados

O script calcula automaticamente:

### Métricas Principais

- **Lucro Total**: Soma de todos os lucros (Valor - Custo_Produto)
- **Produto Mais Vendido**: Produto com maior frequência
- **Satisfação Média**: Média das avaliações dos clientes
- **Total de Vendas**: Número total de registros

### Análise por Canal

- **Vendas por Canal**: Contagem de vendas por canal de venda
- **Distribuição**: Percentual de cada canal no total

## 🎨 Personalização do Código

### 1. Modificando Colunas de Dados

Se sua planilha tem colunas diferentes, edite a função `carregar_dados()`:

```python
def carregar_dados(caminho_arquivo: str) -> pd.DataFrame:
    try:
        # Modifique as colunas conforme sua planilha
        df = pd.read_csv(caminho_arquivo, parse_dates=['Sua_Coluna_Data'])
        print(f"Arquivo '{caminho_arquivo}' carregado com sucesso.")

        # Ajuste os nomes das colunas
        df['Sua_Coluna_Valor'] = pd.to_numeric(df['Sua_Coluna_Valor'], errors='coerce')
        df['Sua_Coluna_Custo'] = pd.to_numeric(df['Sua_Coluna_Custo'], errors='coerce')
        df.dropna(subset=['Sua_Coluna_Valor', 'Sua_Coluna_Custo'], inplace=True)
        return df
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar os dados: {e}")
        return None
```

### 2. Adicionando Novos Insights

Para incluir novas métricas, modifique a função `analisar_dados()`:

```python
def analisar_dados(df: pd.DataFrame) -> dict:
    # ... código existente ...

    # Adicione suas novas métricas
    insights = {
        "lucro_total": df['Lucro'].sum(),
        "produto_mais_vendido": df['Produto'].mode()[0],
        "vendas_por_canal": df['Canal_Venda'].value_counts().to_dict(),
        "satisfacao_media": df['Satisfacao_Cliente'].mean(),
        "total_vendas": len(df),

        # NOVAS MÉTRICAS
        "valor_medio_venda": df['Valor'].mean(),
        "produto_mais_lucrativo": df.groupby('Produto')['Lucro'].sum().idxmax(),
        "melhor_canal": df.groupby('Canal_Venda')['Lucro'].sum().idxmax(),
        "tendencia_mensal": df.groupby(df['Data'].dt.month)['Valor'].sum().to_dict()
    }
    return insights
```

### 3. Personalizando Gráficos

Para modificar a aparência dos gráficos, edite a função `gerar_grafico()`:

```python
def gerar_grafico(df: pd.DataFrame, caminho_saida: str):
    # ... código existente ...

    # Personalize cores, estilo e layout
    plt.style.use('seaborn-v0_8-whitegrid')  # Mude o estilo
    fig, ax = plt.subplots(figsize=(12, 8))   # Ajuste tamanho

    # Cores personalizadas
    cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    vendas_por_canal.plot(kind='bar', ax=ax, color=cores)

    # Títulos e labels personalizados
    ax.set_title('Análise de Vendas por Canal - Sua Empresa', fontsize=18, pad=25)
    ax.set_xlabel('Canais de Venda', fontsize=14)
    ax.set_ylabel('Volume de Vendas', fontsize=14)
```

### 4. Modificando o Relatório PDF

Para personalizar o layout do PDF, edite `criar_pdf_relatorio()`:

```python
def criar_pdf_relatorio(nome_pdf: str, insights: dict, caminho_grafico: str):
    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho personalizado
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 20, "Relatório de Vendas - Sua Empresa", 0, 1, "C")

    # Adicione logo da empresa (se disponível)
    # pdf.image('logo.png', x=10, y=10, w=30)

    # Seções personalizadas
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resumo Executivo", 0, 1, 'L')

    # ... resto do código ...
```

### 5. Configurando Outros Servidores de E-mail

Para usar outros provedores de e-mail, modifique `enviar_email()`:

```python
def enviar_email(remetente_email: str, remetente_senha: str, destinatario_email: str, nome_pdf: str):
    # Para Outlook/Hotmail
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)

    # Para Yahoo
    # server = smtplib.SMTP('smtp.mail.yahoo.com', 587)

    # Para servidor próprio
    # server = smtplib.SMTP('seu-servidor.com', 587)

    server.starttls()
    server.login(remetente_email, remetente_senha)
    # ... resto do código ...
```

## 🔧 Configurações Avançadas

### Variáveis de Configuração

Adicione no início do script para facilitar personalização:

```python
# CONFIGURAÇÕES DO PROJETO
CONFIG = {
    'arquivo_csv': 'planilhas/sales2.csv',
    'arquivo_grafico': 'grafico_vendas.png',
    'servidor_smtp': 'smtp.gmail.com',
    'porta_smtp': 587,
    'assunto_email': 'Relatório de Análise de Vendas',
    'estilo_grafico': 'seaborn-v0_8-whitegrid',
    'tamanho_grafico': (10, 6),
    'cores_grafico': ['#4a90e2', '#e27c4a']
}
```

### Logging Avançado

Para melhor monitoramento, adicione logging:

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sender.log'),
        logging.StreamHandler()
    ]
)

# Usar nos logs
logging.info("Iniciando processamento dos dados")
logging.error(f"Erro ao carregar arquivo: {e}")
```

## 🚨 Troubleshooting

### Problemas Comuns e Soluções

#### 1. Erro: "Arquivo não encontrado"

**Sintoma**: `ERRO CRÍTICO: O arquivo 'planilhas/sales2.csv' não foi encontrado.`

**Solução**:

- Verifique se o arquivo existe na pasta `planilhas/`
- Confirme o nome exato do arquivo (case sensitive)
- Use caminho absoluto se necessário: `C:/caminho/completo/arquivo.csv`

#### 2. Erro de Autenticação Gmail

**Sintoma**: `ERRO DE AUTENTICAÇÃO: E-mail ou senha de app incorretos.`

**Solução**:

- Verifique se a verificação em duas etapas está ativa
- Gere uma nova senha de app no Google
- Certifique-se de usar a senha de app, não a senha principal

#### 3. Erro de Dependências

**Sintoma**: `ModuleNotFoundError: No module named 'pandas'`

**Solução**:

```bash
pip install pandas matplotlib fpdf2
```

#### 4. Erro de Formato de Data

**Sintoma**: `ParserError: Unknown string format`

**Solução**:

- Verifique o formato das datas no CSV
- Ajuste o parâmetro `parse_dates` na função `carregar_dados()`
- Exemplo: `parse_dates=['Data'], date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y')`

#### 5. Erro de Memória

**Sintoma**: Processo lento ou travamento com arquivos grandes

**Solução**:

- Use `chunksize` no `pd.read_csv()` para arquivos grandes
- Implemente processamento em lotes
- Considere usar `dask` para datasets muito grandes

### Debug Mode

Para ativar modo debug, adicione no início do script:

```python
DEBUG = True

def debug_print(message):
    if DEBUG:
        print(f"[DEBUG] {message}")
```

## 📊 Exemplos de Uso

### Exemplo 1: Análise Mensal

```python
# Modificar para análise mensal
df['Mes'] = df['Data'].dt.month
vendas_mensais = df.groupby('Mes')['Valor'].sum()
```

### Exemplo 2: Análise por Produto

```python
# Adicionar análise detalhada por produto
produto_analise = df.groupby('Produto').agg({
    'Valor': ['sum', 'mean', 'count'],
    'Lucro': 'sum',
    'Satisfacao_Cliente': 'mean'
}).round(2)
```

### Exemplo 3: Relatório Comparativo

```python
# Comparar períodos
df['Trimestre'] = df['Data'].dt.quarter
comparativo = df.groupby('Trimestre')['Valor'].sum()
```

## 🤝 Contribuição

Para contribuir com melhorias:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:

- Abra uma issue no repositório
- Consulte a seção de troubleshooting
- Verifique os logs gerados pelo script

---

**Desenvolvido com ❤️ para a comunidade de análise de dados**

_Última atualização: Janeiro 2024_

