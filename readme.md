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
├── data/
│   └── raw/                 # Armazenamento local dos JSONs brutos extraídos da API
├── src/
│   ├── 1_extract_raw.py     # Script de extração da API
│   ├── 2_load_to_bronze.py  # Script de ingestão no PostgreSQL
│   ├── 3_transform_silver.py# Limpeza e padronização (ELT)
│   └── 4_model_gold.py      # Criação e carga do Star Schema
├── requirements.txt         # Dependências do projeto
└── README.md