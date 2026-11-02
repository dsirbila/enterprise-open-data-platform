# Enterprise Open Data Platform

Modern Enterprise Data Engineering with AI. A comprehensive platform implementing end-to-end data pipelines based on Georgian open data (Open-Meteo weather, NBG currency, USGS earthquakes).

---

## 📚 Labs & Curriculum Overview

### Module I — Foundations
1. **Lab 1: Environment & WSL2 Setup** — Installing VS Code, Git, Docker Desktop, repository structure setup.
2. **Lab 2: Dev Environment & Git** — Docker Compose with Postgres+Redis containers, feature-branch → PR → merge workflow.
3. **Lab 3: Database Foundations** — DBeaver + PostgreSQL connection, 3 schemas: weather / currency / seismic.
4. **Lab 4: PostgreSQL & SQL Basics** — DDL/DML, table creation, and initial data loading from sample JSON.
5. **Lab 5: Advanced SQL** — Window functions, CTE, JOIN, trend analysis, and EXPLAIN.
6. **Lab 6: Data Modeling** — Star Schema design (fact/dim tables) using dbdiagram.io or draw.io.

### Module II — Python & Data Ingestion
7. **Lab 7: Python for Data Engineering** — First REST client using requests and logging for Open-Meteo.
8. **Lab 8: Parallel Processing** — Fetching weather for 4 Georgian cities concurrently using `concurrent.futures`.
9. **Lab 9: REST API Integration** — Production-grade client with retry/backoff for Open-Meteo + NBG[cite: 1].
10. **Lab 10: File Processing & XML Validation** — CSV, JSON, XML, GeoJSON file handling and USGS earthquake data integration.
11. **Lab 11: Modern Data Formats** — PyArrow (Parquet/Avro) conversion, size and performance benchmarking across 3 sources.
12. **Lab 12: FastAPI** — Building a custom wrapper API ("Georgia Open Data Gateway").

### Module III — Data Pipelines
13. **Lab 13: ETL Fundamentals** — Python + psycopg2 REST-to-PostgreSQL incremental loading (NBG).
14. **Lab 14: ELT & Data Quality** — Validation framework, freshness/duplicate checks, and error reporting.
15. **Lab 15: Enterprise Data Integration** — Docker SFTP image simulation, partner feeds, XML/CSV, ACK/NACK handling.
16. **Lab 16: Redis Caching** — API response caching with TTL and Pub/Sub invalidation.

### Module IV — Orchestration & Streaming
17. **Lab 17: Apache Airflow — Basics** — First Airflow DAG for daily data ingestion.
18. **Lab 18: Airflow — Advanced** — Dynamic DAGs, sensors, and retry policies.
19. **Lab 19: Apache Kafka — Basics** — Producer/Consumer stream setup for USGS earthquake events.
20. **Lab 20: Kafka — Advanced** — Dead Letter Queue (DLQ), partitioning, and stream monitoring.
21. **Lab 21: Apache Spark — Basics** — PySpark DataFrame API for NBG batch transformations.
22. **Lab 22: Spark — Advanced** — Joining 3 sources and Spark query optimization.

### Module V — Modern Data Platform Engineering
23. **Lab 23: ClickHouse OLAP Integration** — Columnar database setup for fast analytical aggregations on weather and currency data.

---

## 💻 Tech Stack
- **Languages & Frameworks:** Python 3.12, PySpark, Pandas, FastAPI, psycopg2
- **Databases & Storage:** PostgreSQL, Redis, ClickHouse, Parquet/Avro
- **Orchestration & Streaming:** Apache Airflow, Apache Kafka
- **Infrastructure:** Docker Compose, Ubuntu / WSL2
