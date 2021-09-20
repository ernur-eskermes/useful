#!/usr/bin/env bash

sleep 10;

# Run migrations
poetry run alembic upgrade head