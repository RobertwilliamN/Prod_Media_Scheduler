#!/bin/sh

# Aguarde o banco de dados PostgreSQL ficar disponível
until pg_isready -h db -p 5432 -U root; do
  echo "Aguardando o banco de dados PostgreSQL estar disponível..."
  sleep 2
done

# Execute as migrações, mas apenas se houver novas migrações para aplicar
echo "Executando migrações..."
python /app/social_media_scheduler/manage.py migrate --check || python /app/social_media_scheduler/manage.py migrate

# Criar superusuário se não existir
echo "Verificando se o superusuário padrão já existe..."
python /app/social_media_scheduler/manage.py shell -c "
from django.contrib.auth.models import User;
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superusuário criado: $SUPERUSER_USERNAME')
else:
    print('Superusuário $SUPERUSER_USERNAME já existe.')
"

# Iniciando o scheduler em segundo plano
echo "Iniciando o Scheduler..."
python /app/social_media_scheduler/scheduler/scheduler.py &

# Inicie o servidor Django
echo "Iniciando o servidor Django..."
python /app/social_media_scheduler/manage.py runserver 0.0.0.0:8000
