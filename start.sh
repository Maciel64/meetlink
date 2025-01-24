#!/bin/bash

if [ "$ENV" = "production" ]; then
  echo "Iniciando Daphne em produção com SSL..."
  daphne -e ssl:443:privateKey=/app/certbot/conf/live/totemvirtual.com.br/privkey.pem:certKey=/app/certbot/conf/live/totemvirtual.com.br/fullchain.pem core.asgi:application
else
  echo "Iniciando Daphne em desenvolvimento sem SSL..."
  daphne -b 0.0.0.0 -p 8001 core.asgi:application
fi