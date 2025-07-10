<!-- BADGES -->
[contributors_badge]: https://img.shields.io/github/contributors/guillaumepot/Train_Service_Alert.svg?style=for-the-badge
[contributors_url]: https://github.com/guillaumepot/Train_Service_Alert/graphs/contributors
[forks_badge]: https://img.shields.io/github/forks/guillaumepot/Train_Service_Alert.svg?style=for-the-badge
[forks_url]: https://github.com/guillaumepot/Train_Service_Alert/network/members
[stars_badge]: https://img.shields.io/github/stars/guillaumepot/Train_Service_Alert.svg?style=for-the-badge
[stars_url]: https://github.com/guillaumepot/Train_Service_Alert/stargazers
[issues_badge]: https://img.shields.io/github/issues/guillaumepot/Train_Service_Alert.svg?style=for-the-badge
[issues_url]: https://github.com/guillaumepot/Train_Service_Alert/issues
[license_badge]: https://img.shields.io/github/license/guillaumepot/Train_Service_Alert.svg?style=for-the-badge
[license_url]: https://github.com/guillaumepot/Train_Service_Alert/blob/master/LICENSE.txt
[linkedin_badge]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin_url]: https://linkedin.com/in/062guillaumepot

<!-- TECHNOLOGY BADGES -->
[python_badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python_url]: https://www.python.org/
[beautiful_soup_badge]: https://img.shields.io/badge/BeautifulSoup-59666C?style=for-the-badge&logo=python&logoColor=white
[beautiful_soup_url]: https://www.crummy.com/software/BeautifulSoup/
[elasticsearch_badge]: https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white
[elasticsearch_url]: https://www.elastic.co/
[fastapi_badge]: https://img.shields.io/badge/FastAPI-0056B3?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi_url]: https://fastapi.tiangolo.com/
[flask_badge]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[flask_url]: https://flask.palletsprojects.com/
[kafka_badge]: https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white
[kafka_url]: https://kafka.apache.org/
[redis_badge]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[redis_url]: https://redis.io/
[postgresql_badge]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql_url]: https://www.postgresql.org/
[docker_badge]: https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white
[docker_url]: https://www.docker.com/
[dbt_badge]: https://img.shields.io/badge/dbt-FF69B4?style=for-the-badge&logo=dbt&logoColor=white
[dbt_url]: https://www.getdbt.com/
[protobuf_badge]: https://img.shields.io/badge/protobuf-2F3134?style=for-the-badge&logo=protobuf&logoColor=white
[protobuf_url]: https://protobuf.dev/
[GCP_badge]: https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white
[GCP_url]: https://cloud.google.com/

<!-- README -->
<a id="readme-top"></a>

# Train Service Alert

[![Contributors][contributors_badge]][contributors_url]
[![Forks][forks_badge]][forks_url]
[![Stargazers][stars_badge]][stars_url]
[![Issues][issues_badge]][issues_url]
[![MIT License][license_badge]][license_url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/guillaumepot/Train_Service_Alert">
    <img src="images/logo.jpeg" alt="Logo" width="150" height="150">
  </a>
</div>

<!-- PROJECT DESCRIPTION -->
<p align="center" style="font-size: 1.2rem; font-weight: 300; color: #666;">
  A Data streaming tool to monitor French train service alerts.
</p>

<!-- PROJECT INFO -->
<div>
  <p align="center">
    <br />
    <a href="https://github.com/guillaumepot/Train_Service_Alert/blob/main/docs/README.md"><strong>Explore the docs</strong></a>
    <br />
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/guillaumepot/Train_Service_Alert/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/guillaumepot/Train_Service_Alert/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


## Table of Contents

<details>
  <summary>Click to expand</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#what-is-gtfs">What is GTFS</a></li>
      </ul>
    </li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#key-features">Key Features</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#configuration">Configuration</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#known-issues">Known Issues</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#development">Development</a></li>
    <li><a href="#security--privacy">Security & Privacy</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#sources">Sources</a></li>
  </ol>
</details>


## About The Project

Based on a project I made for a client, I decided to make a more generic version of it.
This project is a data streaming tool to monitor French train service alerts.
- It uses the GTFS schedule data to monitor the train service and alert through a BI dashboard.
- Statistics are computed on the fly and stored in a PostgreSQL database and displayed in a BI dashboard.
- The project is containerized and can be deployed on any platform.


### What is GTFS
```text
The General Transit Feed Specification (GTFS) is an Open Standard used to distribute relevant information about transit systems to riders. It allows public transit agencies to publish their transit data in a format that can be consumed by a wide variety of software applications.

GTFS consists of two main parts:
• GTFS Schedule: Contains information about routes, schedules, fares, and geographic transit details
• GTFS Realtime: Contains trip updates, vehicle positions, and service alerts

This project focuses on French TGV (high-speed train) data provided by SNCF.
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

### Core Technologies
* [![Python][python_badge]][python_url] - Main programming language
* [![Docker][docker_badge]][docker_url] - Containerization
* [![FastAPI][fastapi_badge]][fastapi_url] - Web API framework

### Data Processing
* [![Kafka][kafka_badge]][kafka_url] - Message streaming
* [![Redis][redis_badge]][redis_url] - Caching layer
* [![dbt][dbt_badge]][dbt_url] - Data transformation

### Data Storage
* [![PostgreSQL][postgresql_badge]][postgresql_url] - GTFS data storage


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Key Features

### 🚄 Real-Time Train Monitoring
- **GTFS-RT Data Processing**: Fetches and processes real-time train data from SNCF API
- **Trip Updates**: Live tracking of train schedules, delays, and arrival/departure times  
- **Service Alerts**: Real-time alerts about service disruptions and incidents
- **Multi-language Support**: Alert messages in both French and English

### 📊 Advanced Analytics & KPIs
- **Punctuality Analysis**: Track on-time performance for both trains and stations
- **Delay Metrics**: Calculate mean delays by trains, stations, and dates
- **Current Delays**: Real-time view of active delays across the network
- **Train Volume**: Daily train frequency analysis
- **Most Delayed Trains**: Identify consistently delayed routes
- **Active Alerts**: Monitor current service alerts and their impact

### 🏗️ Stream Processing Architecture
- **Apache Kafka**: High-throughput message streaming for real-time data
- **Redis Caching**: Intelligent duplicate detection and data deduplication
- **Producer-Consumer Pattern**: Scalable data processing pipeline
- **Parallel Processing**: Simultaneous handling of multiple data feeds

### 💾 Robust Data Management
- **TimescaleDB**: Time-series optimized PostgreSQL for historical data
- **Data Compression**: Automatic compression of historical data
- **Retention Policies**: Configurable data lifecycle management (3 years default)
- **GTFS Schedule Updates**: Periodic updates of static schedule data

### 🔧 Enterprise-Ready Infrastructure
- **Containerized Architecture**: Full Docker Compose deployment
- **Multi-Profile Setup**: Separate environments for different components
- **Automatic Scaling**: Kafka cluster with multiple brokers
- **Health Monitoring**: Built-in health checks and logging
- **Secret Management**: Secure handling of database credentials

### 📈 Business Intelligence Ready
- **dbt Transformations**: Clean, modeled data ready for BI tools
- **KPI Dashboards**: Pre-built metrics for operational insights
- **Data Quality**: Automated data validation and error handling
- **Historical Analysis**: 3-year data retention for trend analysis

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Architecture

1. **Data Ingestion**: Containerized Kafka cluster to ingest data from SNCF APIs with a producer service.
2. **Data Processing**: Containerized Kafka consumer to process data and store it in a PostgreSQL database.
3. **Data Storage**: PostgreSQL database to store the data.
4. **Data analysis**: dbt to transform the data and get KPIs.
[WIP] 5. **Data Visualization**: dbt to transform the data and create a BI dashboard with a dashboard service.
[WIP] 6. **Data Notification**: Containerized Kafka consumer to process alerts and send them to the user.

### Data Pipeline

#### GTFS Real Time (Trip Updates & Service Alerts)
**Source**: SNCF Open Data Platform
- **Frequency**: every 5 minutes (can be changed in producer.py and consumer.py)
- **Process**: - `producer.py` Get data and send it to Kafka
               - `consumer.py` Get data from Kafka and store it in a PostgreSQL database
 - **Storage**: Kafka topic with structured tables (routes, trips, stops, etc.)

#### GTFS Schedule
**Source**: SNCF Open Data Platform
- **Frequency**: 1 time/week (Must be configured as cronjob)
- **Process**: - `gtfs_updater.py` Get data and store it in a PostgreSQL database
 - **Storage**: PostgreSQL database with structured tables (routes, trips, stops, etc.)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites
- **Python 3.12+** with [uv](https://github.com/astral-sh/uv) package manager
- **Docker & Docker Compose** for infrastructure services

### Configuration

1. Set postgres credentials as secrets in the following files:
  - ./secrets/postgres_user.secret
  - ./secrets/postgres_password.secret

2. Set the cronjob to update the GTFS schedule data.
  - `crontab -e`
  - Add the following line:
    ```bash
    # GTFS update (every day at 00:00)
    0 0 * * * cd /path/to/your/project && docker compose --profile gtfs-update up
    # DBT models update (every 5 minutes)
    */5 * * * * cd /path/to/your/project/src/dbt/train_service_alert && uv run dbt run
    ```
3. Set your data sources configuration accoridng your compose configuration here:
  - ./config/data_sources.json



### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/guillaumepot/Train_Service_Alert.git
   cd Train_Service_Alert
   ```
2. **Install dependencies**
   ```bash
   uv sync
   ```
3. **Run the project**
   ```bash
   docker compose --profile database up -d
   docker compose --profile pipeline up -d
   # Optional (pgadmin)
   docker compose --profile administration up -d
   ```

### Usage
- You can directly Postgres or use pgadmin to access the database.
- You can create a Dashboard and connect postgres to it go get real-time data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Known Issues

- [ ] 


## Roadmap

### Upcoming Features



- [ ] **Add a dashboard feature** to display the data in a dashboard including:
    - Global punctuality analysis for trains and stations
    - Mean delay calculations by trains, stations, and dates
    - Current delays monitoring (last 60 minutes)
    - Train volume analysis per day
    - Most delayed trains identification and ranking
    - Active service alerts tracking with cause and effect classification

### Long-term Goals

- [ ] **Add a notification feature** to send alerts to users.
      - This will include kafka topic to send alerts to users.
      - This will include an API to register users and manage their preferences.



<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Development

### Project structure

```text
Train_Service_Alert/
├── config/
│   └── data_sources.json              # Configuration for data sources and connections
├── data/
│   ├── kafka/                         # Kafka persistent data
│   ├── pgadmin/                       # pgAdmin configuration data
│   └── postgres/                      # PostgreSQL persistent data
├── documents/
│   └── changelogs/
│       └── 1.0.0.md                   # Version changelog
├── images/
│   └── logo.jpeg                      # Project logo
├── logs/                              # Application logs directory
├── notebooks/
│   └── explore.ipynb                  # Data exploration notebook
├── scripts/
│   ├── config.json                    # README generation configuration
│   ├── generate_readme.py             # README template processor
│   ├── postgres_backup.sh             # Database backup utility
│   └── postgres_to_csv.sh             # Data export utility
├── secrets/                           # Docker secrets directory
├── src/
│   ├── consumer/
│   │   ├── consumer.py                # Kafka consumer service
│   │   ├── Dockerfile                 # Consumer container definition
│   │   ├── PostgreEngine.py           # PostgreSQL connection engine
│   │   └── requirements.txt           # Consumer dependencies
│   ├── dbt/
│   │   └── train_service_alert/
│   │       ├── analyses/              # dbt analyses
│   │       ├── dbt_project.yml        # dbt project configuration
│   │       ├── macros/
│   │       │   └── delay_helper.sql   # dbt macros for delay calculations
│   │       ├── models/
│   │       │   ├── marts/
│   │       │   │   └── kpis/          # Business KPI models
│   │       │   │       ├── active_alerts.sql
│   │       │   │       ├── current_delays.sql
│   │       │   │       ├── global_ponctuality_*.sql
│   │       │   │       ├── mean_delay_*.sql
│   │       │   │       ├── most_delayed_trains.sql
│   │       │   │       └── train_volume_per_day.sql
│   │       │   ├── sources.yml        # dbt source definitions
│   │       │   └── staging/
│   │       │       └── stg_stop_time_updates.sql
│   │       ├── seeds/                 # dbt seed data
│   │       ├── snapshots/             # dbt snapshots
│   │       └── tests/                 # dbt tests
│   ├── gtfs_update/
│   │   ├── Dockerfile                 # GTFS updater container
│   │   ├── gtfs_update.py             # GTFS schedule data updater
│   │   ├── PostgreEngine.py           # Database engine
│   │   └── requirements.txt           # Updater dependencies
│   ├── postgres/
│   │   └── init.sql                   # Database initialization script
│   ├── producer/
│   │   ├── Dockerfile                 # Producer container definition
│   │   ├── producer.py                # Kafka producer service
│   │   ├── RedisEngine.py             # Redis connection engine
│   │   └── requirements.txt           # Producer dependencies
│   └── redis/
│       └── redis_7.2.conf             # Redis configuration
├── tests/
│   ├── conftest.py                    # pytest configuration
│   ├── test_consumer.py               # Consumer service tests
│   ├── test_extract.py                # Data extraction tests
│   ├── test_gtfs_update.py            # GTFS update tests
│   ├── test_hello.py                  # Basic tests
│   ├── test_postgre_engine.py         # PostgreSQL engine tests
│   └── test_redis_engine.py           # Redis engine tests
├── docker-compose.yaml                # Multi-service orchestration
├── LICENSE                            # MIT License
├── pyproject.toml                     # Python project configuration
├── README.template.md                 # README template
├── todo.md                            # Project todos
└── uv.lock                            # Dependency lock file
```



### Changelogs

- [V1.0.0](documents/changelogs/1.0.0.md) - Initial release


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Security & Privacy

- **🔐 No Personal Data Storage**: The whole data pipeline use public data from SNCF Open Data Platform.
- **⏱️ Respectful Scraping**: Implements delays to avoid rate limiting
- **🏠 Local Storage**: All data is stored locally by default
- **📝 Minimal Logging**: Only essential information is logged

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the **MIT License**. See `LICENSE.txt` for more information.


## Sources

- **[SNCF Open Data](https://ressources.data.sncf.com/)** - French railway data provider


<p align="right">(<a href="#readme-top">back to top</a>)</p>
