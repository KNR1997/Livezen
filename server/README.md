### ⚡️ How to install

1. Create and activate virtual environment
```sh
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.\.venv\Scripts\activate  # Windows
```

2. Install requirements
```sh
pip install -r requirements.txt
```

3. copy .env.template and rename to .env

4. Start the backend service
```sh
uvicorn livezen.main:app --reload --host 0.0.0.0 --port 8080
```


### ⚡️ DB migration steps
1. Initialize Aerich
```sh
aerich init -t livezen.config.TORTOISE_ORM
aerich init-db
```

2. Generate migration script
```sh
aerich migrate
```

3. Apply migration
```sh
aerich upgrade
```

# docker mysql setup
