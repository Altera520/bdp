#!/bin/bash

{% set kafka_urls = [] %}
{% for hostname in groups.kafka %}
{{ kafka_urls.append(hostname + ':' + kafka_port) }}
{% endfor %}
BOOTSTRAP_SERVERS={{ kafka_urls | join(',') }}
KAFKA_BIN={{ stack_root }}/kafka/bin