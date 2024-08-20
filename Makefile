# Command to run app.py
server:
	@echo "Running app.py..."
	@python3 app.py

# Command to stop RabbitMQ
stop:
	@echo "Stopping RabbitMQ..."
	@brew services stop rabbitmq
