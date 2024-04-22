build:
	docker build -t hello-asyncio --pull=false .

serve: build
	docker run -p 8000:80 -it --rm --cpus=2 --memory=512m hello-asyncio

test: serve
	curl -X POST -H "Content-Type: application/json" -d '{"name": "John"}' http://localhost:8000/hello
