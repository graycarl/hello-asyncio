build:
	docker build .

serve: build
	docker run -p 8000:80 -it --rm $(shell docker images -q | head -n 1)

test: serve
	curl -X POST -H "Content-Type: application/json" -d '{"name": "John"}' http://localhost:8000/hello
