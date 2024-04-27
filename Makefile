IMAGE_NAME=selenium-pothead
CONTAINER_NAME=selenium-pothead

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --name $(CONTAINER_NAME) -d --shm-size="2g" -p 4444:4444 -p 7900:7900 --rm -v .:/app $(IMAGE_NAME)

test:
	docker exec -it -u root --env "HOME=/root" selenium-pothead bash -l -c "python3 selenium_test.py" 

stop:
	docker stop $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash