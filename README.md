### ⚡️ How to install

## requirements
python 3.11.0 or higher
node v20.19.4 or higher

1. Setup backend/server
# navigate to server folder
```sh
cd\server
```

# create virtual environment
```sh
python -m venv .venv
```

# activate virtial environment
```sh
source .venv/bin/activate  # Linux/Mac
# or
.\.venv\Scripts\activate  # Windows
```

# install requirements
```sh
pip install -r requirements.txt
```

# copy .env.template and rename to .env

# start backend server
```sh
uvicorn livezen.main:app --reload --host 0.0.0.0 --port 8080
```
The backend service is now running, and you can visit http://localhost:8080/docs to view the API documentation.

# db setup
- for simpliciy we use the sqlite.
- if you accidently delete the db.sqlite file follow these to generate a sqlite
- or if you prefer connect to a mysql database, add db credentials in the .env and change config.py TORTOISE_ORM connections.

# Initialize Aerich
```sh
aerich init -t livezen.config.TORTOISE_ORM
aerich init-db
```

# Generate migration script
```sh
aerich migrate
```

# Apply migration
```sh
aerich upgrade
```



2. Setup admin
# install dependencies
```sh
yarn or npm install
```
# copy .env.template and rename to .env

# start admin
```sh
yarn dev
```
The admin service is now running, and you can visit http://localhost:3002 to view the admin panel.


2. Setup shop
# install dependencies
```sh
yarn or npm install
```
# copy .env.template and rename to .env

# start shop
```sh
yarn dev:rest
```
The admin service is now running, and you can visit http://localhost:3003 to view the admin panel.



### Choice of Technology
- Backend: FastAPI (Python) – Chosen for its high performance, easy async support, and automatic Swagger docs generation.
- Frontend: Next.js (React) – Enables fast server-side rendering, API integration, and component-based UI for a modern UX.
- Database: SQLite/MySQL (whichever you used) – Simple to set up, ideal for small projects.
- Other Libraries:
    - Tortoise ORM – For ORM-based data modeling.
    - Pydantic – For request/response validation.
    - Axios – For API calls in the frontend.
    - Tailwind CSS – For rapid UI styling.

### Design Decisions
# Backend Architecture – Domain-Driven Design (DDD)
I structured the backend following Domain-Driven Design principles to promote modularity, scalability, and separation of concerns.

- Each domain/module (e.g., product, auth, wishlist) contains its own:
    - models.py – Defines domain entities and ORM mappings.
    - repository.py – Handles all database operations for that domain (CRUD, queries, etc.).
    - service.py – Contains business logic and domain rules, independent of framework or persistence.
    - views.py – Exposes REST endpoints using FastAPI routers and calls service layer functions.

- This ensures:
    - The business logic is independent from API routes or ORM details.
    - Each module can be tested and maintained separately.
    - Easier scalability and refactoring in future.

- structure
    server/
    ├── livezen/
    │   ├── auth/                  # Shared configs, database setup, utils
    │   ├── product/
    │   │   ├── models.py
    │   │   ├── repository.py
    │   │   ├── service.py
    │   │   └── views.py
    │   ├── tag/
    │   │   ├── service.py
    │   │   └── views.py
    │   └── main.py

# Repository Pattern
- The Repository Pattern is used between the Service and Database layers to decouple persistence logic from business rules.
- This means the service layer interacts only with abstract data operations, not raw database queries — improving testability and maintainability.

## Implementation Details
- Modules(server)
    - main.py – FastAPI entry point defining routes.
    - api.py - api endpoints setup
    - repository.py - base repository class
    - models.py - base models
    - config.py - project configuration(db, logging, JWT secret)

## Additional Novel Feature
- Wishlist System:
    - Users can click “Add to Wishlist” on any product.
    - Wishlist stored in backend table wishlist.
    - My Wishlist” page displays saved products.
    - This improves user engagement and personalization.

## Concerns & Challenges Faced
- Limited time to build extra features(rate-limit).
- Improvements (with more time):
    - Docker setup
    - Test deployment(mvp)

## References
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/docs)
- [PickBazar](https://redq.io/pickbazar)
- [Dispatch Blog Post](https://medium.com/@NetflixTechBlog/introducing-dispatch-da4b8a2a8072)
- [Source Code](https://github.com/netflix/dispatch)
- [Issue tracker](https://github.com/netflix/dispatch/issues)
