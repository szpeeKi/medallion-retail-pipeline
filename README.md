# 🏅 Medallion Retail Pipeline

## 📖 Sobre o Projeto
End-to-end Data Engineering pipeline usando Python, PostgreSQL, Airflow e AWS, totalmente baseado na **Arquitetura Medallion** (Raw, Bronze, Silver e Gold).

Este projeto extrai dados de produtos da API pública [dummyjson.com](https://dummyjson.com) e processa essas informações através de camadas progressivas de qualidade de dados, culminando em um modelo dimensional (Star Schema) otimizado para consumo por ferramentas de Business Intelligence (BI).

---

## 🏗️ Arquitetura de Dados (Medallion)

O pipeline foi estruturado seguindo o padrão da indústria de camadas lógicas:

* **Ingestion (Raw):** Extração via AWS Lambda, que salva o JSON bruto da API particionado por data no S3 (bucket `medallion-retail-raw-rafa`), evitando *Data Swamp*. A partição usa o fuso `America/Sao_Paulo`, para refletir o dia do negócio no Brasil. O script `extract_products.py` cobre a mesma extração para uso local em desenvolvimento.
* **🥉 Bronze Layer:** Carga (Load) dos dados brutos do S3 no PostgreSQL, garantindo um espelho exato da origem e proteção contra duplicatas (`ON CONFLICT DO NOTHING`).
* **🥈 Silver Layer:** Transformação (ELT) usando o motor do banco de dados para limpeza, padronização de categorias, tratamento de campos JSONB e remoção de nulos.
* **🥇 Gold Layer:** Modelagem Dimensional (*Star Schema*). `dim_category` e `dim_product` (SCD Tipo 1, sempre com o atributo mais recente do produto) e a tabela fato `fact_product_snapshot`, granular por produto e por dia de snapshot, com métricas de preço, desconto, avaliação e status de disponibilidade.

---

## 🧠 Decisões de Modelagem (Gold)

* **Chave composta em `fact_product_snapshot` (`snapshot_date`, `product_id`):** o mesmo produto aparece uma vez por dia de snapshot, então a granularidade exige as duas colunas na PK.
* **`NUMERIC` em vez de `FLOAT` para valores monetários:** evita erro de arredondamento em `price` e `discount_percentage`.
* **`availability_status` na fato, não na dimensão:** é um dado que pode mudar de um dia para o outro, diferente de atributos fixos do produto.
* **`DO NOTHING` na carga da fato, `DO UPDATE` nas dimensões:** um snapshot já gravado é histórico e não deve ser reescrito; a dimensão (SCD Tipo 1) sempre reflete o estado mais recente do produto.
* **`rating` como coluna única em `silver.products`:** a API de origem retorna a nota como número direto, sem separar nota e contagem de avaliações.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3
* **Banco de Dados:** PostgreSQL
* **Bibliotecas Principais:** `psycopg2`, `requests`, `boto3`, `logging`
* **Cloud:** AWS Lambda + S3 (camada Raw, implementado)
* **Orquestração:** Apache Airflow *(roadmap)*
* **Práticas Adotadas:** Idempotência, Tratamento de Exceções, Logs de Execução, SQL DDL/DML, Modelagem Relacional.

---

## 🚀 Estrutura do Repositório

```text
medallion-retail-pipeline/
├── data/
│ └── raw/ # JSONs brutos extraidos da API (versionamento ignorado)
├── infra/
│ └── aws/
│ └── lambda_handler.py # Handler AWS Lambda
├── logs/
│ └── app.log # Log unico de execucao do pipeline
├── src/
│ ├── database/
│ │ └── create_schemas.py # DDL: schemas bronze/silver/gold e tabelas
│ ├── extract/
│ │ └── extract_products.py # Extracao da API -> data/raw
│ ├── load/
│ │ └── load_bronze.py # Ingestao do JSON bruto no PostgreSQL
│ └── transform/
│ ├── transform_silver.py # Limpeza e padronizacao (ELT)
│ └── build_gold.py # Star Schema (dimensoes + fato)
├── tests/ # Testes automatizados
├── requirements.txt # Dependencias do projeto
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
python -m src.transform.build_gold      # 5. monta o star schema -> gold
```

---

## 🔁 Recuperação de Carga Perdida

O pipeline roda uma vez por dia e é incremental. Se um dia não gerar arquivo no S3 (falha na Lambda, API fora do ar), a carga daquele dia não existe em nenhuma camada. A recuperação hoje é manual: rodar a extração apontando para a data específica, garantir que o arquivo caia na partição correta do S3, e então rodar bronze → silver → gold normalmente a partir dele.
