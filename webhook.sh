#!/bin/bash
curl -dH -X POST "$(terraform output -raw webhook_url)"
