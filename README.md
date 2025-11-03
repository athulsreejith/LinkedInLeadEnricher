# GenAI Real-time Lead Enrichment Pipeline

A cutting-edge, real-time lead enrichment system that automates sales development representative (SDR) workflows by enriching sales leads with LinkedIn-based profile intelligence and AI-generated conversation starters using GenAI. Built with Apache Kafka, Apache Flink, LangChain, OpenAI, SerpAPI, and deployed via Docker containers, this project demonstrates a microservices-based event-driven pipeline for near real-time lead augmentation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Pipeline](#running-the-pipeline)
- [Usage](#usage)
- [Pipeline Components](#pipeline-components)
- [Sample Output](#sample-output)
- [Troubleshooting](#troubleshooting)
- [References](#references)
- [Contributors](#contributors)

---

## Overview

This project creates a real-time lead enrichment pipeline that consumes raw lead data (names, companies, emails) from a Kafka topic, enriches it with profile data scraped via LinkedIn using SerpAPI, and augments it with AI-generated summaries, interesting facts, and icebreaker conversation starters using OpenAI's GPT models via LangChain.

The enriched lead data is produced back to a Kafka topic for downstream consumption by SDR tools or other customer engagement systems.

---

## Features

- Near real-time event-driven pipeline using Kafka for scalable data streaming
- Profile enrichment via LinkedIn web scraping using SerpAPI
- AI augmentation with OpenAI GPT models through LangChain for:
  - Concise lead summaries
  - Interesting lead-specific facts
  - Custom conversation topics and icebreaker questions
- Resilient design with fallback templates for missing data or API failures
- Dockerized microservices for easy deployment and scalability
- Optional Flink integration for live ETL and streaming transformations

---

## Architecture

The system architecture consists of:

- **Kafka Topics**
  - `salesforcemyleads`: Input topic with raw lead data
  - `salesforceicebreakers`: Output topic with enriched AI-augmented lead details
- **Microservices**
  - Kafka Consumer and Producer wrappers abstracting Kafka integration
  - Enrichment module that fetches LinkedIn profile URLs and summaries
  - AI chain module using LangChain and OpenAI API to run LLM prompts
  - Orchestrator managing the whole pipeline lifecycle
- **Dockerized Environment**
  - Services for Zookeeper, Kafka, Flink JobManager and TaskManager, and the enrichment app

---

## Getting Started

### Prerequisites

- Docker and Docker Compose (latest version)
- Python 3.10+ (optional, for local development/debugging)
- Git
- API Keys:
  - OpenAI (for GPT-based summaries & icebreakers)
  - SerpAPI (for LinkedIn and Google Custom Search scraping)
- Recommended system specs: 4GB+ RAM for smooth container operation

---

### Installation

Clone the repository:
```bash
git clone https://github.com/athulsreejith/LinkedInLeadEnricher.git
cd <project directory>
```

Running the Pipeline
Build and start all Docker containers:
```
docker compose up -d --build
```

Create Kafka topics (skip if auto-create is enabled):
```
docker run --rm -it --network genai-realtimedefault \
  confluentinc/cp-kafka:7.5.0 \
  kafka-topics --bootstrap-server kafka:9092 \
  --create --topic salesforcemyleads --partitions 1 --replication-factor 1

docker run --rm -it --network genai-realtimedefault \
  confluentinc/cp-kafka:7.5.0 \
  kafka-topics --bootstrap-server kafka:9092 \
  --create --topic salesforceicebreakers --partitions 1 --replication-factor 1
```

Start the lead enrichment application:
```
docker compose exec app python -u -m app.run
```

Send test leads using the dummy producer:
```
docker compose exec app python -u tools/dummy_producer.py
```

Consume and print enriched results:
```
docker compose exec app python -u tools/print_results.py
```
## Usage

- Send raw lead data to the Kafka `salesforcemyleads` topic. The system automatically:  
  - Fetches LinkedIn profile information via SerpAPI  
  - Runs AI augmentations using OpenAI GPT models  
  - Produces enriched lead data to `salesforceicebreakers`  

- Consumers subscribing to `salesforceicebreakers` will receive:  
  - Summaries of leads’ professional background  
  - Two interesting facts  
  - One suggested interest topic  
  - Two creative icebreaker questions  

---

## Pipeline Components

- **Configuration (`config.py`)**  
  - Loads environment variables including Kafka, OpenAI, and SerpAPI credentials  

- **Kafka Integration (`kafka_io.py`, `dummy_producer.py`, `print_results.py`)**  
  - Producers and consumers for lead ingestion and enriched output  

- **LinkedIn Enrichment (`enrichers.py`)**  
  - Searches LinkedIn URLs and extracts profile snippets using SerpAPI  

- **AI Augmentation (`llm_chain.py`)**  
  - Generates summaries, facts, interests, and icebreakers using LangChain + OpenAI  

- **Pipeline Orchestration (`pipeline.py`, `run.py`)**  
  - Main consumer-producer loop handling enrichment and output  

- **Streaming ETL (Optional)**  
  - Flink SQL files for streaming transformations

## Sample Output
```
{
  "full_name": "Edwin Francis",
  "company": "SureFlow",
  "summary": "Edwin Francis is making waves at SureFlow with notable achievements.",
  "facts": [
    "Edwin has demonstrated strong expertise in process automation.",
    "He contributes to impactful projects in workflow optimization."
  ],
  "interest_topic": "Emerging tech trends",
  "icebreakers": [
    "Hi Edwin, what's the most exciting part of your role at SureFlow?",
    "Hey Edwin, I'm curious what innovation at SureFlow inspires you most?"
  ]
}
```
## Troubleshooting

- **Ensure Docker daemon is running** and all containers are healthy.
- **Check logs for the app container**:

```bash
docker compose logs app
```
- **Verify .env contains valid API keys and Kafka settings.**
- **For SASL/SSL Kafka connections**, update the .env accordingly.
- **Confirm Kafka topics exist** and messages flow correctly.
