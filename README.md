# 🏅 Medallion Retail Pipeline

## 📖 Sobre o Projeto
End-to-end Data Engineering pipeline usando Python, PostgreSQL, Airflow e AWS, totalmente baseado na **Arquitetura Medallion** (Raw, Bronze, Silver e Gold). 

Este projeto extrai dados de um catálogo de produtos de uma API externa e processa essas informações através de camadas progressivas de qualidade de dados, culminando em um modelo dimensional otimizado para consumo por ferramentas de Business Intelligence (BI).

---

## 🏗️ Arquitetura de Dados (Medallion)

O pipeline foi estruturado seguindo o padrão da indústria de camadas lógicas:

* **Ingestion (Extract):** Consumo da API via Python, com tratamento de resiliência e salvamento do JSON particionado localmente para evitar *Data Swamp*.
* **🥉 Bronze Layer:** Carga (Load) dos dados brutos no PostgreSQL, garantindo um espelho exato da origem e proteção contra duplicatas (`ON CONFLICT DO NOTHING`).
* **🥈 Silver Layer:** Transformação (ELT) usando o motor do banco de dados para limpeza, padronização de categorias, tratamento de campos JSONB e remoção de nulos.
* **🥇 Gold Layer:** Modelagem Dimensional (*Star Schema*). Criação de tabelas Dimensão (ex: `dim_category`, `dim_product`) e uma Tabela Fato de agregação (`fact_category_metrics`) contendo métricas de negócio pré-calculadas (ticket médio, nota média, total de produtos).

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3
* **Banco de Dados:** PostgreSQL
* **Bibliotecas Principais:** `psycopg2`, `requests`, `logging`
* **Orquestração e Cloud:** Apache Airflow & AWS *(Em desenvolvimento/Roadmap)*
* **Práticas Adotadas:** Idempotência, Tratamento de Exceções, Logs de Execução, SQL DDL/DML, Modelagem Relacional.

---

## 🚀 Estrutura do Repositório

```text
medallion-retail-pipeline/
├── data/
│   └── raw/                      # JSONs brutos extraidos da API (versionamento ignorado)
├── infra/
│   └── aws/
│       └── lambda_handler.py     # Handler AWS Lambda (roadmap)
├── logs/
│   └── app.log                   # Log unico de execucao do pipeline
├── src/
│   ├── database/
│   │   └── create_schemas.py     # DDL: schemas bronze/silver/gold e tabelas
│   ├── extract/
│   │   └── extract_products.py   # Extracao da API -> data/raw
│   ├── load/
│   │   └── load_bronze.py        # Ingestao do JSON bruto no PostgreSQL
│   └── transform/
│       ├── transform_silver.py   # Limpeza e padronizacao (ELT)
│       └── build_gold.py         # Star Schema (dimensoes + fato)
├── tests/                        # Testes automatizados
├── requirements.txt              # Dependencias do projeto
├── .gitignore
└── README.md
```

---

## ▶️ Ordem de Execucao

```bash
python -m src.database.create_schemas   # 1. cria schemas e tabelas
python -m src.extract.extract_products  # 2. extrai da API para data/raw
python -m src.load.load_bronze          # 3. carrega o bruto na camada bronze
python -m src.transform.transform_silver # 4. limpa e padroniza -> silver
python -m src.transform.build_gold       # 5. monta o star schema -> gold
```
