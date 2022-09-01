# Introduction

## What is Explainit?
Explainit is a modern, enterprise-ready business intelligence web application that re-uses existing frameworks to manage and serve dashboard features to machine learning project lifecycle.

Explainit allows ML platform teams to:
* Analyze Drift in the existing data stack (Features & Targets).
* Prepare very short summary of productionized data.
* Perform Quality Checks on the data.
* Analyze relationship between features & target.
* Understand more about intricasies of features and target.

## Who is Explainit for?
Explainit helps ML platform teams with DevOps experience monitor productionized batch data. Explainit can also help these teams build towards a explainability/monitoring platform that improves collaboration between engineers and data scientists.

Explainit is likely not the right tool if you
* are in an organization that’s just getting started with ML and is not yet sure what the business impact of ML is
* rely primarily on unstructured data

## What Explainit is not?

### Explainit is not

* **an** **BI** / [**ETL**](https://en.wikipedia.org/wiki/Extract,\_transform,\_load) / [**ELT**](https://en.wikipedia.org/wiki/Extract,\_load,\_transform) **system:** Explainit is not (and does not plan to become) a general purpose data transformation or pipelining system. Users often leverage tools like [dbt](https://www.getdbt.com) to manage upstream data transformations.
* **a data orchestration tool:** Explainit does not manage or orchestrate complex workflow DAGs. It relies on upstream data pipelines to produce feature values and integrations with tools like [Airflow](https://airflow.apache.org) to make features consistently available.
* **a dashboard engine:** Explainit is not a replacement for your data dashboard engine or the source of truth for all dashboarding system in your organization. Rather, Explainit is a light-weight downstream layer that can monitor data from an existing batch data warehouse (or other data sources) in production.
* **a real-time dashboard:** Explainit is not a real-time dashboard, but helps monitor data stored in batch systems (e.g. local) to make features & target consistently checks at production.

### Explainit does not _fully_ solve
* **data quality / drift detection**: Explainit is not complete solution built to solve data drift / data quality issues. This requires more sophisticated monitoring across data pipelines, served feature values, labels, and model versions.
* **statistical tests**: Explainit does not cover all statistical tests available yet, but cover few of them.
* reproducible model explainability / data quality testing / model backtesting / experiment management.
* **batch + real-time support**: Explainit primarily processes already transformed feature values. Users usually integrate Explainit with batch systems (e.g. existing ETL/ELT pipelines).
* native real-time feature integration.

## How can I get started?

The best way to learn Explainit is to use it. Head over to our [Getting-start](getting-started.md) and try it out!
{% endhint %}

Explore the following resources to get started with Explainit:

* [Getting-started](getting-started.md) is the fastest way to get started with Explainit
* [Architecture](codebase-structure.md) describes Explainit's overall architecture.
