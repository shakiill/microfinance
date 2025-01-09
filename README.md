Micro Finance 
---
1. Clone Project from github
2. Create virtualenv
      ```sh
    $ virtualenv venv
    ```
3. Activate Virtualenv
   ```sh
    $ source venv/Scripts/activate
    ```
4. Install Requirements
   ```sh
    $ pip install -r requirements.txt
    ```

5. Add project specific information in .env
6. Make migration
    ```sh
    $ python manage.py makemigrations
    ```
7. Migrate
    ```sh
    $ python manage.py migrate
    ```
8. Create Superuser
    ```sh
    $ python manage.py createsuperuser
    ```
9. Start Server
    ```sh
    $ python manage.py runserver
    ```
