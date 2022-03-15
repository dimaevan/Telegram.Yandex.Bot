# Telegram.Yandex.Bot

# Create role and database in Postgresql
> psql - U postgres  
> CREATE USER yandex with login password 'yandex';  
> ALTER ROLE yandex login createdb;  
> CREATE database yandex;  
> GRANT ALL PRIVILEGES ON database yandex TO yandex;

# Install as service:
> cp bot.service /lib/systemd/system/

