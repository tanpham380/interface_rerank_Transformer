#!/bin/bash
# Automatically answer "yes" to prompts
yes | uvicorn app:app --host 0.0.0.0 --port 8080
