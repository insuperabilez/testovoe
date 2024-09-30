# Используем официальный образ PostgreSQL
FROM postgres:latest

# Копируем скрипт инициализации в контейнер
COPY init.sql /docker-entrypoint-initdb.d/
#COPY pg_hba.conf /etc/postgresql/pg_hba.conf
#COPY run_init.sh /docker-entrypoint-initdb.d/


# Устанавливаем права на выполнение скрипта
RUN chmod +x /docker-entrypoint-initdb.d/init.sql
#RUN chmod +x /docker-entrypoint-initdb.d/run_init.sh

#CMD ["postgres", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]