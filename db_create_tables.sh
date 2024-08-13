#!/bin/bash
set -e

# Espera o banco de dados estar pronto
until PGPASSWORD=changethis psql -h localhost:5432 -U admin -d stock -c '\q'; do
  >&2 echo "Postgres está indisponível - aguardando..."
  sleep 1
done

# Executa o script SQL para criar as tabelas, se necessário
PGPASSWORD=changethis psql -h localhost:5432 -U admin -d stock -f ./init-db.sh
# Inicia a aplicação
exec "$@"
