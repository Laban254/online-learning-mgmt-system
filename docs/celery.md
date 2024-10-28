### Celery 

1.  **Run Redis**: Make sure your Redis server is running.
    
    ```bash
    redis-server` 
    ```
2.  **Run Celery Worker**: Open a new terminal and run the Celery worker.
    
    ```bash
    celery -A your_project_name worker --loglevel=info  # Replace with your project name`
    ```