start:
	set -a && source .env && docker-compose up

stop:
	set -a && source .env && docker-compose down -v

restart: stop start

.PHONY: start stop restart