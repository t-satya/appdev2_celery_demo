## Requriements
1. pip install -r requirements.txt
2. sudo apt-get install redis
3. installation guide for mailhog - https://gist.github.com/dipenparmar12/4e6cd50d8d1303d5e914742f62659116
4. installation guide for redis - https://redis.io/docs/getting-started/installation/install-redis-on-linux/
## How to start the application
1. Start your redis server in a linux env using the command : redis-server
2. Start the Mailhog using the command - mailhog
3. You can access mailhog at http://localhost:8025
4. cd to backend folder and run the main.py file - python main.py or python3 main.py
5. cd to backend folder and start your celery worker - celery -A main.cel worker --loglevel=info

6. cd to backend folder and start your celery beat - celery -A main.cel beat --loglevel=info
7. cd to frontend folder and run the app.py file - python app.py or python3 app.py