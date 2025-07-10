<!-- BADGES -->
[contributors_badge]: https://img.shields.io/github/contributors/{{github_username}}/{{repository_name}}.svg?style=for-the-badge
[contributors_url]: https://github.com/{{github_username}}/{{repository_name}}/graphs/contributors
[forks_badge]: https://img.shields.io/github/forks/{{github_username}}/{{repository_name}}.svg?style=for-the-badge
[forks_url]: https://github.com/{{github_username}}/{{repository_name}}/network/members
[stars_badge]: https://img.shields.io/github/stars/{{github_username}}/{{repository_name}}.svg?style=for-the-badge
[stars_url]: https://github.com/{{github_username}}/{{repository_name}}/stargazers
[issues_badge]: https://img.shields.io/github/issues/{{github_username}}/{{repository_name}}.svg?style=for-the-badge
[issues_url]: https://github.com/{{github_username}}/{{repository_name}}/issues
[license_badge]: https://img.shields.io/github/license/{{github_username}}/{{repository_name}}.svg?style=for-the-badge
[license_url]: https://github.com/{{github_username}}/{{repository_name}}/blob/master/LICENSE.txt
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

# {{project.name}}

[![Contributors][contributors_badge]][contributors_url]
[![Forks][forks_badge]][forks_url]
[![Stargazers][stars_badge]][stars_url]
[![Issues][issues_badge]][issues_url]
[![MIT License][license_badge]][license_url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/{{github_username}}/{{repository_name}}">
    <img src="{{project.logo}}" alt="Logo" width="150" height="150">
  </a>
</div>

<!-- PROJECT DESCRIPTION -->
<p align="center" style="font-size: 1.2rem; font-weight: 300; color: #666;">
  {{project.description}}
</p>

<!-- PROJECT INFO -->
<div>
  <p align="center">
    <br />
    <a href="https://github.com/{{github_username}}/{{repository_name}}/blob/main/docs/README.md"><strong>Explore the docs</strong></a>
    <br />
    <br />
    <a href="{{demo_url}}">View Demo</a>
    ·
    <a href="https://github.com/{{github_username}}/{{repository_name}}/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/{{github_username}}/{{repository_name}}/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


## Table of Contents

<details>
  <summary>Click to expand</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#what-is-gtfs">What is GTFS</a></li>
    <li><a href="#built-with">Built With</a></li>
  </ol>
</details>


## About The Project

[WIP]

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
* [![Python][python-icon-url]](https://www.python.org/) - Main programming language
* [![Docker][docker-icon-url]](https://www.docker.com/) - Containerization
* [![FastAPI][fastapi-icon-url]](https://fastapi.tiangolo.com/) - Web API framework

### Data Processing
* [![Kafka][kafka-icon-url]](https://kafka.apache.org/) - Message streaming
* [![Redis][redis-icon-url]](https://redis.io/) - Caching layer
* [![dbt][dbt-icon-url]](https://www.getdbt.com/) - Data transformation

### Data Storage
* [![PostgreSQL][postgresql-icon-url]](https://www.postgresql.org/) - GTFS schedule data
* [![GCP][GCP-icon-url]](https://cloud.google.com/) - Data storage


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 