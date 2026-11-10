<div align="center">

# 🎓 GovEdu Data Flow

### Pipeline ETL automatizado para os gastos federais com Ensino Superior no Brasil

*Extrai, limpa, agrega e carrega dados do Portal da Transparência em um banco MySQL.*

<br>

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![ETL](https://img.shields.io/badge/Pipeline-ETL-success?style=for-the-badge)

<br>

[📌 Sobre](#-sobre-o-projeto) •
[🔄 Fluxo](#-fluxo-do-pipeline) •
[⚙️ Processos](#️-o-que-cada-etapa-faz) •
[📂 Estrutura](#-estrutura-do-repositório) •
[🚀 Como usar](#-como-executar) •
[👤 Autor](#-autor)

</div>

---

## 📌 Sobre o projeto

O **GovEdu Data Flow** transforma os arquivos CSV de despesas públicas do [Portal da Transparência](https://portaldatransparencia.gov.br/) em uma base estruturada e consultável, focada em **gastos federais com Ensino Superior**.

Os arquivos brutos são grandes, usam codificação `latin-1`, separador `;` e valores monetários com vírgula decimal. O pipeline resolve tudo isso de forma automática:

- ✅ Lê somente as colunas relevantes
- ✅ Filtra apenas a subfunção **Ensino superior**
- ✅ Converte valores monetários para numérico
- ✅ Calcula indicadores de execução orçamentária
- ✅ Agrega os registros e carrega no **MySQL**
- ✅ Organiza os arquivos já processados para preservar o histórico

---

## 🔄 Fluxo do pipeline

```mermaid
flowchart LR
    A[("📁 raw_data/<br>CSVs do Portal<br>da Transparência")] --> M["🐍 main.py<br>Orquestrador"]
    M --> I["⚙️ initializing_db.py<br>Setup do BD"]
    M --> B["🔎 extraction.py<br>Extract"]
    M --> C["🧹 transforming.py<br>Transform"]
    M --> D["💾 loading.py<br>Load"]
    D --> E[("🐬 MySQL<br>gastos_ensino_superior")]
    M --> F[("📦 processed_data/<br>arquivos concluídos")]

    style A fill:#fff3cd,stroke:#f0ad4e,color:#000
    style E fill:#d1ecf1,stroke:#17a2b8,color:#000
    style F fill:#d4edda,stroke:#28a745,color:#000
```

O orquestrador é o `main.py`: ele percorre todos os CSVs de `raw_data/`, executa as três etapas em sequência e move cada arquivo concluído para `processed_data/`.


---

## ⚙️ O que cada etapa faz

### 0️⃣ Setup — `initializing_db.py`

| Ação | Detalhe | 
| ----- | ----- | 
| Leitura SQL | Lê o script estrutural `sql/creation_db.sql` | 
| Conexão | Cria a *engine* de comunicação com o banco MySQL via SQLAlchemy | 
| Inicialização | Automatiza a criação do banco de dados e da tabela alvo antes do processamento dos dados | 

### 1️⃣ Extract — `extraction.py`

| Ação | Detalhe | 
| ----- | ----- | 
| Leitura | `pd.read_csv` com `sep=';'` e `encoding='latin-1'` | 
| Seleção | Carrega apenas as colunas necessárias (`usecols`) | 
| Padronização | Padroniza a nomenclatura das colunas originais adotando o formato `snake_case` | 
| Filtro | Mantém somente `nome_subfuncao == 'Ensino superior'` | 
| Limpeza | Remove linhas com valores nulos (`dropna`) | 

### 2️⃣ Transform — `transforming.py`

| Ação | Detalhe | 
| ----- | ----- | 
| Conversão de tipos | Valores monetários de texto com vírgula para `float` | 
| Novo campo `valor_abatido` | `valor_pago + valor_liquidado + valor_restos_a_pagar_cancelado` | 
| Novo campo `restos_a_pagar` | `valor_empenhado - valor_abatido` | 
| Enxugamento | Descarta as colunas intermediárias que não serão mais usadas | 
| Agregação | `groupby` por período, órgão, unidade, programa, ação, localizador, categoria e grupo de despesa, somando `valor_empenhado`, `valor_abatido` e `restos_a_pagar` | 
| Ordenação | Resultado ordenado por `nome_orgao_subordinado` | 

### 3️⃣ Load — `loading.py`

| Ação | Detalhe | 
| ----- | ----- | 
| Destino | Tabela `gastos_ensino_superior` | 
| Modo | `if_exists='append'`, preservando o histórico já carregado | 
| Performance | Inserção em lotes (`chunksize=1000`) | 
| Retorno | Quantidade de linhas enviadas ao banco | 

### 🎛️ Orquestração — `main.py`

1. **Inicializa o banco de dados**: Aciona o módulo `initializing_db.py` para ler o arquivo SQL, automatizar a criação do banco e gerar a *engine* de conexão necessária para a carga.
2. **Busca de arquivos**: Percorre todos os arquivos `.csv` localizados no diretório `raw_data/`.
3. **Execução do ETL**: Aplica o ciclo completo de **extração → transformação → carga** individualmente para cada arquivo encontrado.
4. **Organização**: Move automaticamente o arquivo processado com sucesso para a pasta `processed_data/`.
5. **Tratamento de falhas**: Se ocorrer falha em um arquivo específico, ele **permanece em `raw_data/`** e o erro é reportado no terminal, sem interromper o processamento dos demais arquivos.
6. **Resumo**: Exibe ao término da execução o total de linhas que foram enviadas com sucesso para o banco de dados.
---

## 📂 Estrutura do repositório

```
GovEdu_Data_Flow/
├── 📁 raw_data/            # CSVs brutos aguardando processamento
├── 📁 processed_data/      # CSVs já carregados no banco
├── 📁 sql/                 # Armazena todas as queries SQL do projeto
│   └── creation_db.sql     # Script de criação do banco/tabela
│   └── ufabc_queries.sql   # Queries de consulta voltadas a UFABC
│   └── queries.sql         # Queries de consulta do cenário geral
├── 🐍 main.py              # Orquestrador do pipeline
├── 🐍 extraction.py        # Etapa de extração
├── 🐍 transforming.py      # Etapa de transformação
├── 🐍 loading.py           # Etapa de carga
├── 🐍 initializing_db.py   # Leitura do SQL e criação da engine
├── 🔐 .env.example         # Modelo de variáveis de ambiente
├── 🚫 .gitignore
└── 📄 requirements.txt
```

---

## 🚀 Como executar

### Pré-requisitos
- Python 3.9+
- MySQL em execução

### Passo a passo

```bash
git clone https://github.com/joaoalexds/GovEdu_Data_Flow.git
cd GovEdu_Data_Flow

python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

cp .env.example .env      # Preencha as credenciais no .env

# Adicione os CSVs na pasta raw_data/ e inicie:
python main.py
```

### Saída esperada

```text
--------------------------------------------------
O processo foi concluído!
Foram passadas um total de N linhas a DB
```

---

## 🛠️ Tecnologias e Bibliotecas

| Tecnologia/Biblioteca | Uso no projeto | 
| ----- | ----- | 
| **Python** | Linguagem principal do pipeline de dados | 
| **Pandas** | Leitura dos CSVs, seleção, limpeza, conversão de tipos, cálculo e agregação estruturada dos dados | 
| **SQLAlchemy** | Toolkit SQL e ORM utilizado para criar a camada de conexão (*engine*) e facilitar a inserção de DataFrames no banco | 
| **PyMySQL** | Driver de conexão em Python que permite a comunicação direta e a execução de comandos no servidor MySQL | 
| **python-dotenv** | Leitura e carregamento seguro das variáveis de ambiente e credenciais de banco a partir do arquivo `.env` | 
| **os / shutil** | Bibliotecas nativas do Python utilizadas na orquestração para mapear os diretórios e mover os arquivos processados | 
| **SQL** | Linguagem utilizada no arquivo `creation_db.sql`, `queries.sql` e `ufabc_queries.sql` para definir a estrutura (DDL) de criação do banco e da tabela, além de realizar consultas nos dados | 
| **MySQL** | Banco de dados relacional (SGBD) de destino final, garantindo armazenamento estruturado e manutenção do histórico | 

---

## 👤 Autor

<div align="center">

**João Alexandre V. Bernardo**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaoalexandrevb-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaoalexandrevb/)
[![GitHub](https://img.shields.io/badge/GitHub-joaoalexds-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/joaoalexds)

*Gostou do projeto? Deixe uma ⭐ e vamos nos conectar no LinkedIn!*

</div>