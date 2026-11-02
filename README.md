# Enterprise Open Data Platform

Modern Enterprise Data Engineering with AI. A comprehensive platform implementing end-to-end data ingestion pipelines, format benchmarks, operational OLTP storage, and high-performance OLAP analytical aggregation.

---

## 📚 Labs & Curriculum Overview

- **Lab 1: Environment Setup** — Configuring WSL2 (Ubuntu 26.04.1 LTS) and system clock sources for optimal container performance.
- **Lab 2: Git Workflow & Version Control** — Initializing the repository, managing CRLF/LF line endings, and establishing commit standards.
- **Lab 3: Containerization Infrastructure** — Setting up Docker Compose for multi-service enterprise architectures.
- **Lab 4: Python Virtual Environment** — Configuring isolated Python `.venv` environments and dependency management via `requirements.txt`.
- **Lab 5: Project Structure Design** — Establishing modular architecture (`src/ingestion`, `src/analytics`, `lectures`).
- **Lab 6: Configuration Management** — Managing environment configs, user settings, and secure credential handling.
- **Lab 7: Security & `.gitignore` Auditing** — Stripping environment secrets, Python caches (`__pycache__`), and build metadata.
- **Lab 8: Data Pipeline Architecture** — Designing the foundational architecture for ingestion, transformation, and storage.
- **Lab 9: Extraction Utilities** — Building robust data fetchers and source connectors.
- **Lab 10: XML Schema Validation** — Implementing `xml_validator.py` with XSD compliance for enterprise data integrity.
- **Lab 11: File Format Benchmarking** — Comparing performance, memory footprint, and compression efficiency across CSV, Parquet, and Avro (`compare_formats.py`).
- **Lab 12: Pandas Transformations** — Performing structured data manipulations and type casting (`test_pandas_transform.py`).
- **Lab 13: Excel Data Handling** — Implementing round-trip export logic and workbook processing (`test_excel_handler.py`).
- **Lab 14: Relational Databases (PostgreSQL)** — Setting up operational OLTP databases and connection parameters.
- **Lab 15: OLTP Schema Design** — Designing normalized tables for weather (`weather.forecasts`) and currency (`currency.rates`) datasets.
- **Lab 16: Operational Ingestion** — Populating PostgreSQL tables with real-time transactional metrics.
- **Lab 17: Distributed Processing (PySpark)** — Introducing PySpark session management and distributed data structures.
- **Lab 18: Spark Transformations** — Building distributed data processing pipelines and cleaning routines.
- **Lab 19: Columnar Storage Concepts** — Transitioning from OLTP row stores to OLAP columnar architectures.
- **Lab 20: ClickHouse Containerization** — Integrating ClickHouse into Docker Compose with custom user configurations (`users.d/default-user.xml`).
- **Lab 21: ClickHouse MergeTree Tables** — Defining high-performance analytical DDL tables with proper sorting keys (`ORDER BY`).
- **Lab 22: Postgres-to-ClickHouse ETL** — Implementing programmatic data pipelines (`run_clickhouse_etl.py`) to move records from operational storage to analytical tables.
- **Lab 23: ClickHouse Query Optimization & Data Skipping Indexes** — Building dynamic query handlers (`clickhouse_queries.py`) and configuring Data Skipping Indexes (`minmax`, `set`) via `skipping_indexes.sql`.

---

## 💻 Tech Stack
- **Languages & Frameworks:** Python 3.12, PySpark, Pandas, lxml, openpyxl, clickhouse-connect, psycopg2
- **Database & Storage:** PostgreSQL 16, ClickHouse (MergeTree Engine)
- **Infrastructure:** Docker Compose (Analytics Profile), Ubuntu 26.04 LTS (WSL2)
