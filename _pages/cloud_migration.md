---
permalink: /oracle/mig_upg/
title: "Oracle Cloud Migration"
author_profile: false
classes: wide
sidebar:
    nav: "docs"
---

{% for tag in site.tags %}
{% if tag[0] == "Cloud Migration" %}
  <!--<h3>{{ tag[0] }}</h3>-->
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endif %}
{% endfor %}

## Introduction

## Overview of Migration Toolkit

## Migration Approaches

There are several approaches that can be used to migrate a very large Oracle database to Oracle Cloud Infrastructure (OCI). Here are a few common ones:

* Full Export and Import: The most common and straightforward approach is to use Oracle's export and import utilities (EXPORT and IMPORT) to create a full backup of the on-premises database and then restore it to the OCI database. This approach is the simplest to implement, but it can take a long time to complete if the database is very large.

* Data Pump: Another approach is to use Oracle's Data Pump utility, which can export and import data more efficiently than the traditional export/import utilities. Data Pump supports parallel processing, which can greatly speed up the migration process. Data pump provides more options for data movement than the traditional export import.

* GoldenGate: Oracle GoldenGate is a real-time data integration and replication software that can be used to replicate data from an on-premises database to an OCI database. GoldenGate can replicate data in near real-time and can handle high volumes of data and high-availability requirements.

* Transportable Tablespaces: Another approach is to use Transportable Tablespaces (TTS) feature, in this case you move only the required subset of tablespaces instead of entire database, this way you can quickly move large amount of data, this method can be used in scenario where you need to move specific set of data instead of entire database.

* Cloud Data Guard: Finally, you can leverage Oracle's Cloud Data Guard, which allows you to create a physical or logical standby of an on-premises database in OCI. This approach allows you to keep the standby in sync with the primary database, so you can switch over to the standby in the event of a disaster.

## Use Cases

## Conclusion
- Practice, practice, practice
* Start on small database
* Prove it works on production-size database

- Automate
* To ensure consistency and avoid human error

- Save all logs and output
* Data Pump, RMAN

- Clean-up procedure
* In case of failure and rollback
* To repeat tests
* Offline source database afterwards

## Oracle Cloud Migration MOS References