#!/usr/bin/env bash
airflow users create \
          -u admin \
          -f jj \
          -l elg \
          -r Admin \
          -p 123 \
          -e elguetaj@ufm.edu
airflow webserver
