# Code Collection Report

## Directory Structure:
```
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   ├── b712aa6d45af_update_user_model.py
│   │   │   └── fe07219460da_initial_migration.py
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── app/
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── image.py
│   │   │   └── user.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── image.py
│   │   │   └── user.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── extraction.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── image.py
│   │   │   ├── token.py
│   │   │   └── user.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── dependencies.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── utils.py
│   ├── uploads/
│   │   ├── 1056c2a3-ae07-4466-b298-b044e8d16172/
│   │   │   └── 20231225_065026.jpg
│   │   ├── 360a7238-9c87-4727-9f29-c19ea08ccc03/
│   │   │   └── 20231225_065026.jpg
│   │   ├── 48353928-4fec-4dc9-b6db-54434800b241/
│   │   │   └── 20231225_065026.jpg
│   │   ├── 61c5ec05-6d49-4b32-977b-ea08c363d219/
│   │   │   └── 20231225_065026.jpg
│   │   ├── 7a2040d7-8270-40c0-a00a-ebc1ab5e44bc/
│   │   │   └── 20231225_065026.jpg
│   │   ├── cb9f1156-8be5-45b1-bc7b-4c920dcd0219/
│   │   │   └── 20231225_065026.jpg
│   │   ├── ed4f7ea2-96af-4654-b10c-3ff1aa0f0bc0/
│   │   │   └── 20231225_065026.jpg
│   │   ├── images/
│   │   │   ├── 7f2318da-ec74-48ae-be49-a14883cae6d9/
│   │   │   │   ├── 005c2b26-cea4-47ea-8602-a5213bb5de96.jpg
│   │   │   │   ├── 252e3da3-feef-4b6f-9ecd-7a4a7f22d85a.jpg
│   │   │   │   ├── 2c173398-9a07-4ccf-9793-ba0fa23ebff6.jpg
│   │   │   │   ├── 3926ca7e-3da4-4037-a923-64e6b9a8f3d8.jpg
│   │   │   │   ├── 51505c76-923f-4950-908c-4f1c679b8e29.jpg
│   │   │   │   ├── 845b59bb-4248-4a50-a6d7-dc1df200d245.jpg
│   │   │   │   ├── c003066f-d85b-43ef-b4a9-38d51b454285.jpg
│   │   │   │   ├── c22ff6d2-4dbb-4921-b74b-6fd73c764119.jpg
│   │   │   │   └── fe2dbe00-d7fa-4992-a259-9e2dafb65db6.jpg
│   │   │   ├── edcdec56-71c3-4842-a182-88d85b47bd46/
│   │   │   ├── 016b8926-b666-4e3b-bc45-c198defd0967.png
│   │   │   ├── 2133bcdc-777d-4291-b188-69f5e0d3f5f2.png
│   │   │   ├── 2d0ba8dc-e108-4d07-ad8a-f0a6b7a1cf1e.png
│   │   │   ├── 56883ac7-d71f-4431-b155-8f2718a8c11e.png
│   │   │   ├── 73c0008c-8344-45ea-ba4b-98494197283c.png
│   │   │   ├── 75450e70-c7d8-4551-ad8e-0d2fe4b662f7.png
│   │   │   ├── 85b0ae0d-d750-48ee-b377-256c533e2e71.png
│   │   │   ├── 881d83dd-823b-4470-9cfd-793734bbd786.png
│   │   │   ├── c36bde3e-7b67-4680-ae16-6361eff91a39.png
│   │   │   └── c7fd9e23-c715-40c9-9dbe-943c2eb21848.png
│   │   └── original_images/
│   │       ├── <app.models.user.User object at 0x10d19c910>/
│   │       │   └── ce2e404a-aad7-434e-b2af-5c836889f31d.jpg
│   │       ├── <app.models.user.User object at 0x11732a4d0>/
│   │       │   └── 2b8dc014-2ce5-4d8c-b6f6-741851b75bae.jpg
│   │       ├── <app.models.user.User object at 0x11733e490>/
│   │       │   └── bb6fd7b0-4906-4feb-847b-c9f58eff3eae.jpg
│   │       ├── <app.models.user.User object at 0x118a30810>/
│   │       │   └── 3454ddce-71e8-4b15-aa02-568f1aba14f2.jpg
│   │       ├── <app.models.user.User object at 0x12379be10>/
│   │       │   └── 2eb0bbfc-1c54-4bea-b9aa-19ccef5d8271.jpg
│   │       ├── <app.models.user.User object at 0x1237b0350>/
│   │       │   └── 341b5792-9b38-4370-b0f7-0a4808c6d3c2.jpg
│   │       ├── edcdec56-71c3-4842-a182-88d85b47bd46/
│   │       │   ├── 7cc733c8-d8a9-4d81-bbe1-0959dc034eec.jpg
│   │       │   └── c87c9d86-4119-40ed-b1d8-36027d83d3f5.jpg
│   │       ├── 51001bb2-4b1a-45a6-85da-b5436063493e.jpg
│   │       ├── 528479a0-4672-41c9-9c02-079b7b36c855.jpg
│   │       └── 8706fa40-0c24-4bf4-94a1-a514028eca57.jpg
│   ├── .env
│   ├── alembic.ini
│   ├── app.log
│   ├── generate_secret.py
│   ├── setup_db.py
│   ├── test_auth.py
│   ├── test_upload.py
│   ├── verify_db.py
│   └── verify_setup.py
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── Common/
│   │   │   ├── Button.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── Extraction/
│   │   │   ├── ColorPicker.jsx
│   │   │   ├── ExtractionResult.jsx
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── SignatureCropper.jsx
│   │   │   └── ThresholdSlider.jsx
│   │   ├── Layout/
│   │   │   └── Navbar.jsx
│   │   └── Payments/
│   │       └── PaymentButton.jsx
│   ├── hooks/
│   │   └── redux.js
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── NotFound.jsx
│   │   └── Register.jsx
│   ├── store/
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── extractionSlice.js
│   │   │   └── paymentSlice.js
│   │   └── index.js
│   ├── utils/
│   │   ├── api.js
│   │   ├── axiosInstance.js
│   │   ├── errorHandling.js
│   │   └── file.js
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   ├── main.jsx
│   └── routes.jsx
├── .gitignore
├── .prettierrc
├── index.html
├── op.txt.md
├── package-lock.json
├── package.json
├── postcss.config.js
├── README.md
├── tailwind.config.js
└── vite.config.js

```

### File: `index.html`

**Language:** html

**File Size:** 361 bytes
**Created:** 2024-11-11T11:24:57.584473
**Modified:** 2024-11-11T11:24:57.584473

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### File: `tailwind.config.js`

**Language:** js

**File Size:** 1354 bytes
**Created:** 2024-11-11T12:45:07.248895
**Modified:** 2024-11-11T12:45:07.248895

```js
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
export default {
  content: [
    "./index.html",
    "./src*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1E3A8A',    
        secondary: '#F59E0B',  
        link: '#646cff',       
        linkHover: '#535bf2',  
        bodyBg: '#242424',     
        bodyText: 'rgba(255, 255, 255, 0.87)', 
        lightBodyBg: '#ffffff', 
        lightBodyText: '#213547', 
        lightLinkHover: '#747bff', 
        lightButtonBg: '#f9f9f9', 
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      },
      fontSize: {
        '3xl': '3.2em', 
      },
      borderRadius: {
        'xl': '8px', 
      },
      spacing: {
        '0.6em': '0.6em',
        '1.2em': '1.2em',
      },
    },
  },
  plugins: [
    forms,      
    typography, 
  ],
};
```

### File: `vite.config.js`

**Language:** js

**File Size:** 161 bytes
**Created:** 2024-11-11T11:24:57.587726
**Modified:** 2024-11-11T11:24:57.587726

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
})
```

### File: `postcss.config.js`

**Language:** js

**File Size:** 80 bytes
**Created:** 2024-11-11T11:55:58.771183
**Modified:** 2024-11-11T11:55:58.771183

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### File: `backend/verify_setup.py`

**Language:** py

**File Size:** 1161 bytes
**Created:** 2024-11-14T14:35:44.312909
**Modified:** 2024-11-14T14:35:44.312909

```py
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.image import Image
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def verify_setup():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        logger.info(f"Found {len(users)} users")
        for user in users:
            logger.info(f"User: {user.email}, Plan: {user.subscription_plan}")
        logger.info("\nVerifying images table structure...")
        image_columns = Image.__table__.columns
        for column in image_columns:
            logger.info(f"Column: {column.name}, Type: {column.type}")
        logger.info("\nVerifying foreign key constraints...")
        for fk in Image.__table__.foreign_keys:
            logger.info(f"Foreign Key: {fk}")
        return True
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return False
    finally:
        db.close()
if __name__ == "__main__":
    verify_setup()
```

### File: `backend/verify_db.py`

**Language:** py

**File Size:** 1057 bytes
**Created:** 2024-11-14T13:36:49.694046
**Modified:** 2024-11-14T13:36:49.694046

**Security Misconfigurations:**

- Potential security risk: Use of exec detected

```py
from sqlalchemy import create_engine, text
from app.config import settings
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def verify_connection():
    try:
        database_url = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
        safe_url = database_url.replace(settings.DATABASE_PASSWORD, "****")
        logger.info(f"Attempting to connect to: {safe_url}")
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
if __name__ == "__main__":
    verify_connection()
```

### File: `backend/test_auth.py`

**Language:** py

**File Size:** 3252 bytes
**Created:** 2024-11-14T14:43:21.545578
**Modified:** 2024-11-14T14:43:21.545578

**Security Misconfigurations:**

- Potential security risk: Use of exec detected

```py
import requests
import logging
import json
from app.utils.auth import get_password_hash
from app.config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "test@example.com",
    "password": "test123456"
}
def update_test_user_password():
    """Update test user's password in database."""
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASE_NAME,
            user=settings.DATABASE_USERNAME,
            password=settings.DATABASE_PASSWORD,
            host=settings.DATABASE_HOSTNAME,
            port=settings.DATABASE_PORT,
            cursor_factory=RealDictCursor
        )
        with conn.cursor() as cur:
            hashed_password = get_password_hash(TEST_USER["password"])
            cur.execute(
                """
                UPDATE users 
                SET hashed_password = %s 
                WHERE email = %s 
                RETURNING id, email
                """,
                (hashed_password, TEST_USER["email"])
            )
            updated_user = cur.fetchone()
            if updated_user:
                logger.info(f"Updated password for user: {updated_user['email']}")
            else:
                logger.warning("No user found to update")
            conn.commit()
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
def get_test_token():
    """Get authentication token for test user."""
    try:
        update_test_user_password()
        login_data = {
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        logger.info(f"Attempting login for user: {TEST_USER['email']}")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data
        )
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            if token:
                logger.info("Login successful!")
                logger.info(f"Access token: {token[:20]}...")
                with open("test_token.txt", "w") as f:
                    json.dump({"access_token": token}, f)
                logger.info("Token saved to test_token.txt")
                return token
            else:
                logger.error("No token in response")
                return None
        else:
            logger.error(f"Login failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error getting test token: {str(e)}")
        return None
if __name__ == "__main__":
    get_test_token()
```

### File: `backend/alembic.ini`

**Language:** ini

**File Size:** 3761 bytes
**Created:** 2024-11-11T14:25:37.160086
**Modified:** 2024-11-11T14:25:37.160086

```ini
# A generic, single database configuration.
[alembic]
# path to migration scripts
# Use forward slashes (/) also on windows to provide an os agnostic path
script_location = alembic
# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .
# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =
# max length of characters to apply to the "slug" field
# truncate_slug_length = 40
# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false
# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false
# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions
# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
# version_path_separator = newline
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.
# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false
# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8
# backend/alembic.ini
sqlalchemy.url = postgresql://pranay:pranay@localhost:5432/signature_extractor
[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples
# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME
# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME
# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARNING
handlers = console
qualname =
[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### File: `backend/test_upload.py`

**Language:** py

**File Size:** 2537 bytes
**Created:** 2024-11-14T14:40:04.469770
**Modified:** 2024-11-14T14:40:04.469770

```py
import requests
import logging
import json
import os
from PIL import Image
import io
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
BASE_URL = "http://localhost:8000"
def create_test_image():
    """Create a test image if none exists."""
    if not os.path.exists("test_image.jpg"):
        img = Image.new('RGB', (100, 100), color='red')
        img.save("test_image.jpg")
        logger.info("Created test image: test_image.jpg")
def test_upload(image_path="test_image.jpg"):
    try:
        create_test_image()
        try:
            with open("test_token.txt", "r") as f:
                token_data = json.load(f)
                token = token_data.get("access_token")
        except FileNotFoundError:
            logger.error("No token found. Please run test_auth.py first")
            return False
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False
        headers = {
            "Authorization": f"Bearer {token}"
        }
        files = {
            'file': (
                'test_image.jpg',
                open(image_path, 'rb'),
                'image/jpeg'
            )
        }
        logger.info("Sending upload request...")
        logger.info(f"URL: {BASE_URL}/extraction/upload")
        logger.info(f"File: {image_path}")
        logger.info("Headers:")
        logger.info(json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, indent=2))
        response = requests.post(
            f"{BASE_URL}/extraction/upload",
            headers=headers,
            files=files
        )
        logger.info(f"\nStatus Code: {response.status_code}")
        logger.info("Response Headers:")
        logger.info(json.dumps(dict(response.headers), indent=2))
        logger.info("\nResponse Body:")
        try:
            logger.info(json.dumps(response.json(), indent=2))
        except:
            logger.info(response.text)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error during upload test: {str(e)}")
        return False
    finally:
        if 'files' in locals():
            files['file'][1].close()
if __name__ == "__main__":
    test_upload()
```

### File: `backend/generate_secret.py`

**Language:** py

**File Size:** 338 bytes
**Created:** 2024-11-13T21:30:35.818851
**Modified:** 2024-11-13T21:30:35.818851

```py
from secrets import token_hex
def generate_secret_key():
    """Generate a secure secret key."""
    return token_hex(32)
if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("\nGenerated secure secret key:")
    print(secret_key)
    print("\nUpdate your .env file with:")
    print(f"JWT_SECRET={secret_key}\n")
```

### File: `backend/setup_db.py`

**Language:** py

**File Size:** 834 bytes
**Created:** 2024-11-14T13:37:11.162350
**Modified:** 2024-11-14T13:37:11.162350

```py
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.models.user import User
from app.models.image import Image
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def setup_database():
    try:
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database setup completed successfully!")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error during setup: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during setup: {str(e)}")
        return False
if __name__ == "__main__":
    setup_database()
```

### File: `backend/app/config.py`

**Language:** py

**File Size:** 5995 bytes
**Created:** 2024-11-13T21:32:13.124520
**Modified:** 2024-11-13T21:32:13.124520

```py
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError
import logging
logger = logging.getLogger(__name__)
class Settings(BaseSettings):
    DATABASE_HOSTNAME: str = 'localhost'
    DATABASE_PORT: str = '5432'
    DATABASE_PASSWORD: str = 'pranay'
    DATABASE_NAME: str = 'signature_extractor'
    DATABASE_USERNAME: str = 'pranay'
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    class Config:
        env_file = ".env"
        case_sensitive = True
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Settings initialized successfully")
        logger.debug(f"Database URL: {self.DATABASE_URL}")
        logger.debug(f"JWT Algorithm: {self.JWT_ALGORITHM}")
        logger.debug(f"JWT Expiry: {self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
try:
    settings = Settings()
except ValidationError as e:
    logger.error(f"Settings validation error: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error loading settings: {e}")
    raise
```

### File: `backend/app/database.py`

**Language:** py

**File Size:** 3135 bytes
**Created:** 2024-11-14T14:40:54.008493
**Modified:** 2024-11-14T14:40:54.008493

**Security Misconfigurations:**

- Potential security risk: Use of exec detected

```py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging
logger = logging.getLogger(__name__)
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  
    pool_pre_ping=True,  
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def safe_commit(db):
    """Safely commit database changes with error handling."""
    try:
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database commit failed: {str(e)}")
        logger.error("Rolling back transaction")
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during commit: {str(e)}")
        logger.error("Rolling back transaction")
        return False
def verify_db_connection():
    """Verify database connection is working."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logger.info("Database connection verified successfully")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False
    finally:
        db.close()
```

### File: `backend/app/utils.py`

**Language:** py

**File Size:** 27038 bytes
**Created:** 2024-11-13T21:33:11.357960
**Modified:** 2024-11-13T21:33:11.357960

```py
import cv2
import numpy as np
from PIL import Image
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from passlib.context import CryptContext
from app.config import settings
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        logger.debug(f"Created token for user ID: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        exp = payload.get("exp")
        if exp is None or exp < datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User not found for ID: {user_id}")
        raise credentials_exception
    return user
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False
def get_password_hash(password: str) -> str:
    """Generate password hash."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password"
        )
def save_image(file, temp_dir) -> str:
    """Save an uploaded image and convert transparent areas to white if RGBA."""
    try:
        file_path = temp_dir / file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        img = Image.open(file_path)
        if img.mode == 'RGBA':
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  
            background.save(file_path)
        logger.info(f"Image saved successfully at {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving image"
        )
def process_signature(sig, color: str, threshold: int) -> np.ndarray:
    """Process a signature image with color and threshold."""
    try:
        sig_gray = cv2.cvtColor(sig, cv2.COLOR_BGR2GRAY)
        ret, alpha_mask = cv2.threshold(sig_gray, threshold, 255, cv2.THRESH_BINARY_INV)
        color_bgr = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
        color_mask = np.zeros_like(sig, dtype=np.uint8)
        for i in range(3):
            color_mask[:, :, i] = color_bgr[i]
        sig_color = cv2.addWeighted(sig, 1, color_mask, 0.5, 0)
        b, g, r = cv2.split(sig_color[..., :3])
        png = cv2.merge([b, g, r, alpha_mask])
        logger.info("Signature processed successfully")
        return png
    except Exception as e:
        logger.error(f"Error processing signature: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing signature"
        )
```

### File: `backend/app/main.py`

**Language:** py

**File Size:** 24093 bytes
**Created:** 2024-11-14T15:38:44.306141
**Modified:** 2024-11-14T15:38:44.306141

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, extraction
from app.database import Base, engine
import os
import logging
import sys
Base.metadata.create_all(bind=engine)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Signature Extraction App",
    description="API for user authentication and signature extraction from images.",
    version="1.0.0"
)
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "images"))
os.makedirs(UPLOADS_DIR, exist_ok=True)
logger.info(f"Uploads directory configured at: {UPLOADS_DIR}")
try:
    app.mount("/uploads/images", StaticFiles(directory=UPLOADS_DIR), name="uploads")
    logger.info("Successfully mounted uploads directory")
except Exception as e:
    logger.error(f"Failed to mount uploads directory: {str(e)}")
    raise
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "uploads_dir": UPLOADS_DIR,
        "uploads_dir_exists": os.path.exists(UPLOADS_DIR)
    }
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(extraction.router, prefix="/extraction", tags=["Extraction"])
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Signature Extraction App API"}
```

### File: `backend/app/routers/auth.py`

**Language:** py

**File Size:** 31541 bytes
**Created:** 2024-11-14T11:32:09.644041
**Modified:** 2024-11-14T11:32:09.644041

```py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.crud.user import authenticate_user, create_user
from app.database import get_db
from app.utils import create_access_token
from datetime import timedelta
from app.config import settings
import logging
logger = logging.getLogger(__name__)
router = APIRouter(
    tags=["Authentication"]
)
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        if not db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return db_user
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        logger.info(f"User {user.email} successfully logged in")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )
```

### File: `backend/app/routers/__init__.py`

**Language:** py

**File Size:** 174 bytes
**Created:** 2024-11-11T15:29:46.817985
**Modified:** 2024-11-11T15:29:46.817985

```py
from .auth import router as auth_router
from .extraction import router as extraction_router
__all__ = ["auth_router", "extraction_router"]
```

### File: `backend/app/routers/extraction.py`

**Language:** py

**File Size:** 25274 bytes
**Created:** 2024-11-14T15:40:02.878015
**Modified:** 2024-11-14T15:40:02.878015

```py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import logging
import uuid
import os
import traceback
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
router = APIRouter(tags=["Extraction"])
UPLOADS_DIR = "uploads/images"  
@router.post("/upload")
async def upload_image_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.png"
        file_path = os.path.join(UPLOADS_DIR, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        logger.info(f"Successfully uploaded image: {filename}")
        return {
            "id": file_id,
            "filename": filename,
            "file_path": f"/uploads/images/{filename}"
        }
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image")
@router.post("/process_image")
async def process_image_endpoint(
    session_id: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: str,
    threshold: int,
    db: Session = Depends(get_db)
):
    try:
        file_path = os.path.join(UPLOADS_DIR, f"{session_id}.png")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Image file not found.")
        image = cv2.imread(file_path)
        cropped_image = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
        color_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        color_image = np.zeros_like(cropped_image, dtype=np.uint8)
        color_image[:, :] = color_rgb
        result_image = cv2.bitwise_and(color_image, color_image, mask=mask)
        b, g, r = cv2.split(result_image)
        alpha = mask
        final_image = cv2.merge([b, g, r, alpha])
        final_image_pil = Image.fromarray(final_image)
        final_image_io = BytesIO()
        final_image_pil.save(final_image_io, format="PNG")
        final_image_io.seek(0)
        return StreamingResponse(final_image_io, media_type="image/png")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process image")
```

### File: `backend/app/utils/auth.py`

**Language:** py

**File Size:** 1287 bytes
**Created:** 2024-11-14T14:42:50.020682
**Modified:** 2024-11-14T14:42:50.020682

```py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from app.config import settings
import logging
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation failed: {str(e)}")
        raise
```

### File: `backend/app/utils/__init__.py`

**Language:** py

**File Size:** 294 bytes
**Created:** 2024-11-14T14:47:17.229912
**Modified:** 2024-11-14T14:47:17.229912

```py
from .auth import (
    verify_password,
    get_password_hash,
    create_access_token
)
from .dependencies import (
    get_current_user,
    oauth2_scheme
)
__all__ = [
    'verify_password',
    'get_password_hash',
    'create_access_token',
    'get_current_user',
    'oauth2_scheme'
]
```

### File: `backend/app/utils/dependencies.py`

**Language:** py

**File Size:** 1774 bytes
**Created:** 2024-11-14T14:47:09.749555
**Modified:** 2024-11-14T14:47:09.749555

```py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.config import settings
import logging
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User {user_id} not found in database")
        raise credentials_exception
    return user
```

### File: `backend/app/models/user.py`

**Language:** py

**File Size:** 1477 bytes
**Created:** 2024-11-13T20:52:49.932569
**Modified:** 2024-11-13T20:52:49.932569

```py
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base
import enum
class SubscriptionPlan(enum.Enum):
    Free = "Free"
    Pro = "Pro"
    Enterprise = "Enterprise"
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.Free)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### File: `backend/app/models/__init__.py`

**Language:** py

**File Size:** 154 bytes
**Created:** 2024-11-14T13:31:34.726234
**Modified:** 2024-11-14T13:31:34.726234

```py
from app.database import Base
from app.models.user import User
from app.models.image import Image
__all__ = ['Base', 'User', 'Image']
```

### File: `backend/app/models/image.py`

**Language:** py

**File Size:** 2015 bytes
**Created:** 2024-11-14T13:19:29.387931
**Modified:** 2024-11-14T13:19:29.387931

```py
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base
class Image(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    original_image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    user = relationship("User", backref="images")
    original_image = relationship("Image", remote_side=[id], backref="derived_images")
    def __repr__(self):
        return f"<Image(id={self.id}, filename={self.filename})>"
```

### File: `backend/app/schemas/auth.py`

**Language:** py

**File Size:** 425 bytes
**Created:** 2024-11-13T21:25:42.617810
**Modified:** 2024-11-13T21:25:42.617810

```py
from pydantic import BaseModel, EmailStr
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True
```

### File: `backend/app/schemas/user.py`

**Language:** py

**File Size:** 1813 bytes
**Created:** 2024-11-14T14:46:27.305762
**Modified:** 2024-11-14T14:46:27.305762

```py
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum
class SubscriptionPlan(str, Enum):
    Free = "Free"
    Pro = "Pro"
    Enterprise = "Enterprise"
class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    password: str
class UserResponse(UserBase):
    id: UUID4
    subscription_plan: SubscriptionPlan
    created_at: datetime
    class Config:
        from_attributes = True
class UserInDB(UserResponse):
    hashed_password: str
```

### File: `backend/app/schemas/token.py`

**Language:** py

**File Size:** 747 bytes
**Created:** 2024-11-13T21:25:26.723026
**Modified:** 2024-11-13T21:25:26.723026

```py
from pydantic import BaseModel
from typing import Optional
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True
class TokenData(BaseModel):
    username: Optional[str] = None
    sub: Optional[str] = None  
    class Config:
        from_attributes = True
```

### File: `backend/app/schemas/__init__.py`

**Language:** py

**File Size:** 210 bytes
**Created:** 2024-11-11T15:30:31.320230
**Modified:** 2024-11-11T15:30:31.320230

```py
from .user import *
from .image import *
from .token import *
__all__ = ["UserCreate", "UserResponse", "ImageCreate", "ImageResponse", "ExtractionData", "Token", "TokenData"]
```

### File: `backend/app/schemas/image.py`

**Language:** py

**File Size:** 7547 bytes
**Created:** 2024-11-14T13:20:06.655344
**Modified:** 2024-11-14T13:20:06.655344

```py
from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Optional
from datetime import datetime
import re
class ExtractionData(BaseModel):
    x: int = Field(..., ge=0, description="X coordinate of the extraction area")
    y: int = Field(..., ge=0, description="Y coordinate of the extraction area")
    width: int = Field(..., gt=0, description="Width of the extraction area")
    height: int = Field(..., gt=0, description="Height of the extraction area")
    threshold: int = Field(
        default=128,
        ge=0,
        le=255,
        description="Threshold value for binarization"
    )
    color: Optional[str] = Field(
        None,
        description="Hex color code for the signature (e.g., '
    )
    @field_validator('color')
    def validate_color(cls, v):
        if v is not None:
            if not re.match(r'^
                raise ValueError('Invalid hex color code')
        return v
class ImageBase(BaseModel):
    filename: str
    file_path: str
    content_type: str
class ImageCreate(ImageBase):
    pass
class Image(ImageBase):
    id: UUID4
    user_id: UUID4
    original_image_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
class ImageResponse(BaseModel):
    id: UUID4
    filename: str
    file_path: str
    content_type: str
    original_image_id: Optional[UUID4] = None
    created_at: datetime
```

### File: `backend/app/crud/user.py`

**Language:** py

**File Size:** 14779 bytes
**Created:** 2024-11-14T14:46:14.111462
**Modified:** 2024-11-14T14:46:14.111462

```py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import verify_password, get_password_hash
import logging
logger = logging.getLogger(__name__)
def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()
def create_user(db: Session, user: UserCreate) -> User:
    """Create new user."""
    try:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"User with email {user.email} already exists")
            return None
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            subscription_plan='Free'  
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Created new user with email: {user.email}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise
def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user."""
    try:
        user = get_user_by_email(db, email)
        if not user:
            logger.warning(f"No user found with email: {email}")
            return None
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password for user: {email}")
            return None
        logger.info(f"User authenticated successfully: {email}")
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise
```

### File: `backend/app/crud/__init__.py`

**Language:** py

**File Size:** 157 bytes
**Created:** 2024-11-11T15:30:02.621713
**Modified:** 2024-11-11T15:30:02.621713

```py
from .user import *
from .image import *
__all__ = ["create_user", "authenticate_user", "upload_image", "extract_signature"]
```

### File: `backend/app/crud/image.py`

**Language:** py

**File Size:** 11846 bytes
**Created:** 2024-11-14T13:18:39.936327
**Modified:** 2024-11-14T13:18:39.936327

```py
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from app.models.image import Image
from app.schemas.image import ExtractionData
from app.database import safe_commit
import uuid
import os
import cv2
import numpy as np
import logging
from pathlib import Path
import traceback
from typing import Optional
from app.models.user import User
import aiofiles
logger = logging.getLogger(__name__)
async def upload_image(db: Session, file: UploadFile, current_user: User) -> Optional[Image]:
    """Upload and save an image file."""
    file_path = None
    try:
        logger.info(f"Starting file upload process for user {current_user.id}")
        logger.info(f"File details - Name: {file.filename}, Content-Type: {file.content_type}")
        if not file.content_type.startswith('image/'):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}"
            )
        upload_dir = Path("uploads/images") / str(current_user.id)
        try:
            os.makedirs(str(upload_dir), exist_ok=True)
            logger.info(f"Created/verified upload directory: {upload_dir}")
        except Exception as e:
            logger.error(f"Failed to create upload directory: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create upload directory"
            )
        file_ext = os.path.splitext(file.filename)[1].lower()
        if not file_ext:
            file_ext = '.jpg'  
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename
        logger.info(f"Generated file path: {file_path}")
        try:
            contents = await file.read()
            async with aiofiles.open(str(file_path), 'wb') as f:
                await f.write(contents)
            logger.info("File saved successfully")
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file"
            )
        try:
            db_image = Image(
                id=uuid.uuid4(),
                user_id=current_user.id,
                filename=unique_filename,
                file_path=str(file_path),
                content_type=file.content_type
            )
            db.add(db_image)
            if not safe_commit(db):
                raise Exception("Failed to commit to database")
            logger.info(f"Database record created for image: {db_image.id}")
            return db_image
        except Exception as e:
            logger.error(f"Failed to create database record: {e}")
            logger.error(traceback.format_exc())
            if os.path.exists(file_path):
                os.unlink(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create database record: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {e}")
        logger.error(traceback.format_exc())
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file upload: {str(e)}"
        )
def extract_signature(
    db: Session, 
    image_id: uuid.UUID, 
    extraction_data: ExtractionData, 
    current_user: User
) -> Optional[Image]:
    """Extract signature from an uploaded image."""
    try:
        original_image = db.query(Image).filter(
            Image.id == image_id,
            Image.user_id == current_user.id
        ).first()
        if not original_image:
            logger.error(f"Image {image_id} not found for user {current_user.id}")
            return None
        try:
            img = cv2.imread(str(original_image.file_path))
            if img is None:
                logger.error(f"Failed to load image from {original_image.file_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading image: {e}")
            return None
        try:
            x1, y1 = extraction_data.x1, extraction_data.y1
            x2, y2 = extraction_data.x2, extraction_data.y2
            height, width = img.shape[:2]
            x1, x2 = max(0, min(x1, width-1)), max(0, min(x2, width-1))
            y1, y2 = max(0, min(y1, height-1)), max(0, min(y2, height-1))
            signature = img[y1:y2, x1:x2]
            output_dir = Path("uploads/signatures") / str(current_user.id)
            os.makedirs(str(output_dir), exist_ok=True)
            output_filename = f"sig_{uuid.uuid4()}.png"
            output_path = output_dir / output_filename
            cv2.imwrite(str(output_path), signature)
            signature_image = Image(
                id=uuid.uuid4(),
                user_id=current_user.id,
                filename=output_filename,
                file_path=str(output_path),
                content_type="image/png",
                original_image_id=original_image.id
            )
            db.add(signature_image)
            if not safe_commit(db):
                logger.error("Failed to save signature record to database")
                if os.path.exists(output_path):
                    os.unlink(output_path)
                return None
            return signature_image
        except Exception as e:
            logger.error(f"Error extracting signature: {e}")
            logger.error(traceback.format_exc())
            return None
    except Exception as e:
        logger.error(f"Error in extract_signature: {e}")
        logger.error(traceback.format_exc())
        return None
def extract_signature_async(
    db: Session, 
    image_id: uuid.UUID, 
    extraction_data: ExtractionData, 
    current_user: User
) -> Image:
    """Extract signature from an uploaded image."""
    try:
        logger.info(f"Starting signature extraction for image {image_id}")
        image = db.query(Image).filter(
            Image.id == image_id,
            Image.user_id == current_user.id
        ).first()
        if not image:
            logger.error(f"Image {image_id} not found for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        original_path = Path(image.original_image_path)
        if not original_path.exists():
            logger.error(f"Original image file not found: {original_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original image file not found"
            )
        try:
            img = cv2.imread(str(original_path))
            if img is None:
                raise ValueError("Failed to read image file")
            logger.info("Successfully read original image")
        except Exception as e:
            logger.error(f"Error reading image: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image file"
            )
        height, width, _ = img.shape
        if not (0 <= extraction_data.x < width and 
                0 <= extraction_data.y < height and
                0 < extraction_data.width <= width - extraction_data.x and
                0 < extraction_data.height <= height - extraction_data.y):
            logger.error("Invalid extraction coordinates")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid extraction coordinates"
            )
        try:
            roi = img[
                extraction_data.y:extraction_data.y + extraction_data.height,
                extraction_data.x:extraction_data.x + extraction_data.width
            ]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(
                gray,
                extraction_data.threshold,
                255,
                cv2.THRESH_BINARY
            )
            if extraction_data.color:
                color = extraction_data.color.lstrip('
                if len(color) == 3:
                    color = ''.join(c * 2 for c in color)
                bgr_color = tuple(int(color[i:i+2], 16) for i in (4, 2, 0))
                colored_signature = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                colored_signature[thresh == 255] = bgr_color
            else:
                colored_signature = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            logger.info("Successfully processed signature")
        except Exception as e:
            logger.error(f"Error processing signature: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process signature"
            )
        try:
            signature_dir = Path("uploads/signatures") / str(current_user.id)
            signature_dir.mkdir(parents=True, exist_ok=True)
            signature_id = uuid.uuid4()
            signature_path = signature_dir / f"{signature_id}.png"
            cv2.imwrite(str(signature_path), colored_signature)
            logger.info(f"Saved extracted signature to: {signature_path}")
            image.extracted_signature_path = str(signature_path)
            db.commit()
            db.refresh(image)
            logger.info("Updated database record with signature path")
            return image
        except Exception as e:
            logger.error(f"Error saving signature: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save signature"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in extract_signature: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract signature"
        )
```

### File: `backend/alembic/env.py`

**Language:** py

**File Size:** 5477 bytes
**Created:** 2024-11-14T13:31:53.304952
**Modified:** 2024-11-14T13:31:53.304952

```py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.database import Base
from app.models.user import User  
from app.models.image import Image  
from app.config import settings
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### File: `backend/alembic/versions/fe07219460da_initial_migration.py`

**Language:** py

**File Size:** 676 bytes
**Created:** 2024-11-14T13:38:24.761799
**Modified:** 2024-11-14T13:38:24.761799

```py
"""initial_migration
Revision ID: fe07219460da
Revises: 
Create Date: 2024-11-14 13:38:24.758450
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = 'fe07219460da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    pass
def downgrade() -> None:
    pass
```

### File: `backend/alembic/versions/b712aa6d45af_update_user_model.py`

**Language:** py

**File Size:** 698 bytes
**Created:** 2024-11-14T14:47:38.009746
**Modified:** 2024-11-14T14:47:38.009746

```py
"""update_user_model
Revision ID: b712aa6d45af
Revises: fe07219460da
Create Date: 2024-11-14 14:47:38.006662
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = 'b712aa6d45af'
down_revision: Union[str, None] = 'fe07219460da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    pass
def downgrade() -> None:
    pass
```

### File: `src/routes.jsx`

**Language:** jsx

**File Size:** 2114 bytes
**Created:** 2024-11-13T16:11:19.717973
**Modified:** 2024-11-13T16:11:19.717973

```jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProtectedRoute from './components/Common/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};
export default AppRoutes;
```

### File: `src/App.css`

**Language:** css

**File Size:** 606 bytes
**Created:** 2024-11-11T11:24:57.585959
**Modified:** 2024-11-11T11:24:57.585959

```css
#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.react:hover {
  filter: drop-shadow(0 0 2em #61dafbaa);
}
@keyframes logo-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
@media (prefers-reduced-motion: no-preference) {
  a:nth-of-type(2) .logo {
    animation: logo-spin infinite 20s linear;
  }
}
.card {
  padding: 2em;
}
.read-the-docs {
  color: #888;
}
```

### File: `src/index.css`

**Language:** css

**File Size:** 2131 bytes
**Created:** 2024-11-11T22:11:16.521051
**Modified:** 2024-11-11T22:11:16.521051

```css
/* src/index.css */
/* Tailwind Directives */
@tailwind base;
@tailwind components;
@tailwind utilities;
/* Custom Styles */
@layer base {
  :root {
    --font-family-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    /* Dark Mode Variables */
    --body-text-dark: rgba(255, 255, 255, 0.87);
    --body-bg-dark: #242424;
    --link-hover-dark: #90cdf4;
    /* Light Mode Variables */
    --body-text-light: #213547;
    --body-bg-light: #ffffff;
    --link-hover-light: #1d4ed8;
    /* Initial (Dark Mode) Variables */
    --body-text: var(--body-text-dark);
    --body-bg: var(--body-bg-dark);
    --link-hover: var(--link-hover-dark);
    font-family: var(--font-family-sans);
    line-height: 1.5;
    font-weight: 400;
    color-scheme: light dark;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  body {
    margin: 0;
    color: var(--body-text);
    background-color: var(--body-bg);
    min-width: 320px;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  h1 {
    @apply text-3xl font-bold leading-tight;
  }
  a {
    @apply font-medium no-underline;
    color: var(--body-text);
    transition: color 0.2s ease-in-out;
  }
  a:hover {
    color: var(--link-hover);
  }
  button {
    @apply rounded-xl border px-[0.6em] py-[0.6em] text-base font-medium transition-colors duration-200 cursor-pointer;
    background-color: var(--body-bg);
    color: var(--body-text);
    border: 1px solid transparent;
  }
  button:hover {
    border-color: var(--link-hover);
  }
  button:focus,
  button:focus-visible {
    @apply outline-none ring-4 ring-blue-500;
  }
  /* Light Mode Overrides */
  @media (prefers-color-scheme: light) {
    :root {
      --body-text: var(--body-text-light);
      --body-bg: var(--body-bg-light);
      --link-hover: var(--link-hover-light);
    }
    button {
      background-color: var(--body-bg-light);
      color: var(--body-text-light);
    }
  }
}
```

### File: `src/main.jsx`

**Language:** jsx

**File Size:** 862 bytes
**Created:** 2024-11-13T21:43:12.740945
**Modified:** 2024-11-13T21:43:12.740945

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';
import { store } from './store';
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
```

### File: `src/App.jsx`

**Language:** jsx

**File Size:** 3619 bytes
**Created:** 2024-11-13T21:39:04.245758
**Modified:** 2024-11-13T21:39:04.245758

```jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Layout/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import ProtectedRoute from './components/Common/ProtectedRoute';
import './index.css';
function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
}
export default App;
```

### File: `src/utils/errorHandling.js`

**Language:** js

**File Size:** 3066 bytes
**Created:** 2024-11-14T13:12:33.887592
**Modified:** 2024-11-14T13:12:33.887592

```js
export const formatErrorMessage = (error) => {
    if (!error) {
        return 'An unknown error occurred';
    }
    if (error.response?.data) {
        const { data } = error.response;
        if (data.detail) {
            return typeof data.detail === 'string'
                ? data.detail
                : JSON.stringify(data.detail);
        }
        if (typeof data === 'object') {
            const messages = Object.entries(data)
                .map(([key, value]) => {
                    if (Array.isArray(value)) {
                        return `${key}: ${value.join(', ')}`;
                    }
                    return `${key}: ${value}`;
                });
            if (messages.length > 0) {
                return messages.join('\n');
            }
        }
        return JSON.stringify(data);
    }
    if (error.request) {
        return 'Unable to connect to the server. Please check your internet connection.';
    }
    return error.message || 'An unexpected error occurred';
};
export const logError = (error, context = '') => {
    const errorInfo = {
        timestamp: new Date().toISOString(),
        context,
        message: error.message,
        stack: error.stack,
    };
    if (error.response) {
        errorInfo.response = {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
        };
    }
    if (error.config) {
        errorInfo.request = {
            url: error.config.url,
            method: error.config.method,
        };
    }
    console.error('Error:', errorInfo);
};
export const isAuthError = (error) => {
    return error.response?.status === 401;
};
export const isPermissionError = (error) => {
    return error.response?.status === 403;
};
export const getErrorMessage = (error) => {
    if (isAuthError(error)) {
        return 'Please log in to continue';
    }
    if (isPermissionError(error)) {
        return 'You do not have permission to perform this action';
    }
    return formatErrorMessage(error);
};
export const handleUploadError = (error) => {
    if (error.response?.status === 413) {
        return 'File is too large. Please try a smaller file.';
    }
    if (error.response?.status === 415) {
        return 'File type not supported. Please use JPG or PNG files.';
    }
    return getErrorMessage(error);
};
```

### File: `src/utils/file.js`

**Language:** js

**File Size:** 1348 bytes
**Created:** 2024-11-11T22:49:18.332322
**Modified:** 2024-11-11T22:49:18.332322

```js
export const ACCEPTED_IMAGE_TYPES = {
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png']
};
export const MAX_FILE_SIZE = 10 * 1024 * 1024; 
export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
export const validateImageFile = (file) => {
    if (!file) {
        return 'No file selected';
    }
    if (file.size > MAX_FILE_SIZE) {
        return `File size (${formatFileSize(file.size)}) exceeds the limit of ${formatFileSize(MAX_FILE_SIZE)}.`;
    }
    if (!Object.keys(ACCEPTED_IMAGE_TYPES).includes(file.type)) {
        return `File type "${file.type}" is not supported. Accepted types are: JPG, PNG`;
    }
    return null;
};
export const createFilePreview = (file) => {
    return URL.createObjectURL(file);
};
export const revokeFilePreview = (previewUrl) => {
    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
    }
};
export const getFileExtension = (filename) => {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2).toLowerCase();
};
export const isImageFile = (file) => {
    return Object.keys(ACCEPTED_IMAGE_TYPES).includes(file.type);
};
```

### File: `src/utils/api.js`

**Language:** js

**File Size:** 5535 bytes
**Created:** 2024-11-13T14:51:17.141896
**Modified:** 2024-11-13T14:51:17.141896

```js
import axiosInstance from './axiosInstance';
const uploadImage = async (formData) => {
    try {
        const response = await axiosInstance.post('/extraction/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};
const selectRegion = async ({ session_id, x1, y1, x2, y2 }) => {
    try {
        const response = await axiosInstance.post('/extraction/select_region/', {
            session_id,
            x1,
            y1,
            x2,
            y2
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};
const processImage = async ({ session_id, color, threshold }) => {
    try {
        const response = await axiosInstance.post('/extraction/process_image/', {
            session_id,
            color,
            threshold
        }, {
            responseType: 'blob'
        });
        return URL.createObjectURL(response.data);
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};
const resetSession = async (session_id) => {
    try {
        const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};
export default {
    uploadImage,
    selectRegion,
    processImage,
    resetSession
};
```

### File: `src/utils/axiosInstance.js`

**Language:** js

**File Size:** 22937 bytes
**Created:** 2024-11-14T13:11:45.646294
**Modified:** 2024-11-14T13:11:45.646294

```js
import axios from 'axios';
const axiosInstance = axios.create({
    baseURL: 'http:
    timeout: 30000, 
    maxContentLength: 50 * 1024 * 1024, 
    maxBodyLength: 50 * 1024 * 1024, 
});
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        console.debug('Making request:', {
            url: config.url,
            method: config.method,
            headers: {
                ...config.headers,
                Authorization: token ? 'Bearer <token>' : undefined 
            },
            contentType: config.headers['Content-Type']
        });
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        if (!config.headers['Content-Type']) {
            config.headers['Content-Type'] = 'application/json';
        }
        return config;
    },
    (error) => {
        console.error('Request configuration error:', error);
        return Promise.reject(error);
    }
);
axiosInstance.interceptors.response.use(
    (response) => {
        console.debug('Response received:', {
            url: response.config.url,
            status: response.status,
            statusText: response.statusText,
            data: response.data
        });
        return response;
    },
    (error) => {
        if (error.response) {
            console.error('Response error:', {
                url: error.config?.url,
                status: error.response.status,
                statusText: error.response.statusText,
                data: error.response.data
            });
            switch (error.response.status) {
                case 401:
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                    break;
                case 403:
                    console.error('Permission denied:', error.response.data);
                    error.message = 'You do not have permission to perform this action';
                    break;
                case 413:
                    error.message = 'File is too large. Please try a smaller file.';
                    break;
                case 415:
                    error.message = 'File type not supported. Please use JPG or PNG files.';
                    break;
                case 422:
                    error.message = Object.values(error.response.data).join('. ');
                    break;
                case 500:
                    error.message = error.response.data?.detail || 'An unexpected error occurred. Please try again.';
                    console.error('Server error details:', error.response.data);
                    break;
                default:
                    error.message = error.response.data?.detail || 'Request failed. Please try again.';
            }
        } else if (error.request) {
            console.error('No response received:', {
                url: error.config?.url,
                method: error.config?.method,
                request: error.request
            });
            error.message = 'No response from server. Please check your connection.';
        } else {
            console.error('Request setup error:', error.message);
            error.message = 'Failed to send request. Please try again.';
        }
        error.timestamp = new Date().toISOString();
        return Promise.reject(error);
    }
);
axiosInstance.isAuthenticated = () => {
    return !!localStorage.getItem('token');
};
axiosInstance.clearAuth = () => {
    localStorage.removeItem('token');
};
export default axiosInstance;
```

### File: `src/components/Payments/PaymentButton.jsx`

**Language:** jsx

**File Size:** 2935 bytes
**Created:** 2024-11-11T13:01:51.489626
**Modified:** 2024-11-11T13:01:51.489626

```jsx
import React from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
const PaymentButton = () => {
  const token = useSelector((state) => state.auth.token);
  const loadRazorpayScript = (src) => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };
  const handlePayment = async () => {
    const res = await loadRazorpayScript(
      'https:
    );
    if (!res) {
      alert('Razorpay SDK failed to load. Are you online?');
      return;
    }
    const order = await axios.post(
      'http:
      {
        amount: 500, 
        currency: 'INR',
        receipt: 'receipt#1',
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    const options = {
      key: 'YOUR_RAZORPAY_KEY_ID', 
      amount: order.data.amount.toString(),
      currency: order.data.currency,
      name: 'Signature Extractor App',
      description: 'Subscription Payment',
      order_id: order.data.id,
      handler: async (response) => {
        try {
          const verification = await axios.post(
            'http:
            {
              payment_id: response.razorpay_payment_id,
              order_id: response.razorpay_order_id,
              signature: response.razorpay_signature,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (verification.data.status === 'captured') {
            alert('Payment Successful!');
          } else {
            alert('Payment Verification Failed!');
          }
        } catch (error) {
          alert('Payment Verification Failed!');
        }
      },
      prefill: {
        name: 'User Name', 
        email: 'user@example.com', 
        contact: '9999999999', 
      },
      notes: {
        address: 'Signature Extractor App Office',
      },
      theme: {
        color: '#1E3A8A',
      },
    };
    const paymentObject = new window.Razorpay(options);
    paymentObject.open();
  };
  return (
    <button
      onClick={handlePayment}
      className="bg-secondary text-white px-4 py-2 rounded hover:bg-primary"
    >
      Subscribe Now
    </button>
  );
};
export default PaymentButton;
```

### File: `src/components/Auth/RegisterForm.jsx`

**Language:** jsx

**File Size:** 13321 bytes
**Created:** 2024-11-13T21:18:06.719323
**Modified:** 2024-11-13T21:18:06.719323

```jsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { registerUser, clearError } from '../../store/slices/authSlice';
const RegisterForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!email || !password) {
      setFormError('Please fill in all fields');
      return;
    }
    try {
      dispatch(clearError());
      await dispatch(registerUser({ email, password })).unwrap();
      navigate('/login');
    } catch (err) {
      console.error('Registration failed:', err);
    }
  };
  const formatError = (error) => {
    if (!error) return null;
    if (typeof error === 'string') return error;
    if (error.detail) {
      if (Array.isArray(error.detail)) {
        return error.detail.map((err) => err.msg || err).join(', ');
      }
      return error.detail;
    }
    return 'Registration failed. Please try again.';
  };
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-2xl font-bold mb-6">Register</h2>
      {(error || formError) && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 text-red-500 dark:text-red-400 mt-0.5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div>
              <h4 className="text-sm font-medium text-red-800 dark:text-red-400">
                Registration failed
              </h4>
              <p className="mt-1 text-sm text-red-700 dark:text-red-300 whitespace-pre-line">
                {formatError(error) || formError}
              </p>
            </div>
          </div>
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Email:
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            disabled={loading}
            required
          />
        </div>
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Password:
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            disabled={loading}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http:
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Registering...
            </span>
          ) : (
            'Register'
          )}
        </button>
      </form>
    </div>
  );
};
export default RegisterForm;
```

### File: `src/components/Auth/LoginForm.jsx`

**Language:** jsx

**File Size:** 31006 bytes
**Created:** 2024-11-13T21:44:20.862251
**Modified:** 2024-11-13T21:44:20.862251

```jsx
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { loginUser, clearError } from '../../store/slices/authSlice';
const LoginForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState('');
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!email || !password) {
      setFormError('Please fill in all fields');
      return;
    }
    try {
      dispatch(clearError());
      console.log('Attempting login with:', { email, password: '***' });
      const result = await dispatch(loginUser({ email, password })).unwrap();
      console.log('Login successful:', result);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
      if (err.detail) {
        setFormError(
          Array.isArray(err.detail)
            ? err.detail.map((e) => e.msg).join(', ')
            : err.detail
        );
      } else {
        setFormError('An error occurred during login');
      }
    }
  };
  const formatError = (error) => {
    if (!error) return null;
    if (typeof error === 'string') return error;
    if (Array.isArray(error)) return error.join(', ');
    if (error.detail) {
      if (Array.isArray(error.detail)) {
        return error.detail.map((err) => err.msg || err).join(', ');
      }
      return error.detail;
    }
    return 'An error occurred';
  };
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-2xl font-bold mb-6">Login</h2>
      {(error || formError) && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 text-red-500 dark:text-red-400 mt-0.5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div>
              <h4 className="text-sm font-medium text-red-800 dark:text-red-400">
                Login failed
              </h4>
              <p className="mt-1 text-sm text-red-700 dark:text-red-300 whitespace-pre-line">
                {formatError(error) || formError}
              </p>
            </div>
          </div>
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Email:
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            disabled={loading}
            required
          />
        </div>
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Password:
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            disabled={loading}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http:
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Logging in...
            </span>
          ) : (
            'Login'
          )}
        </button>
      </form>
    </div>
  );
};
export default LoginForm;
```

### File: `src/components/Layout/Navbar.jsx`

**Language:** jsx

**File Size:** 1952 bytes
**Created:** 2024-11-11T13:11:10.787328
**Modified:** 2024-11-11T13:11:10.787328

```jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../store/slices/authSlice';
import Button from '../Common/Button'; 
const Navbar = () => {
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(false);
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);
  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };
  return (
    <nav className="bg-primary text-white p-4 flex justify-between items-center">
      <div>
        <Link to="/" className="text-xl font-bold">
          Signature Extractor
        </Link>
      </div>
      <div className="flex items-center space-x-4">
        {}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="focus:outline-none"
          aria-label="Toggle Dark Mode"
        >
          {darkMode ? '🌞' : '🌙'}
        </button>
        {isAuthenticated && user ? (
          <>
            <span className="text-sm">Plan: {user.subscriptionPlan}</span>
            <Link to="/dashboard" className="hover:text-secondary">
              Dashboard
            </Link>
            <Button onClick={handleLogout}>Logout</Button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-secondary">
              Login
            </Link>
            <Link to="/register" className="hover:text-secondary">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};
export default Navbar;
```

### File: `src/components/Common/Button.jsx`

**Language:** jsx

**File Size:** 379 bytes
**Created:** 2024-11-11T13:10:49.614441
**Modified:** 2024-11-11T13:10:49.614441

```jsx
import React from 'react';
const Button = ({ type = 'button', children, className = '', ...props }) => {
  return (
    <button
      type={type}
      className={`bg-primary text-white px-4 py-2 rounded hover:bg-secondary transition-colors ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
export default Button;
```

### File: `src/components/Common/ProtectedRoute.jsx`

**Language:** jsx

**File Size:** 2170 bytes
**Created:** 2024-11-13T21:39:20.296117
**Modified:** 2024-11-13T21:39:20.296117

```jsx
import React from 'react';
import { useSelector } from 'react-redux';
import { Navigate, useLocation } from 'react-router-dom';
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useSelector((state) => state.auth);
  const location = useLocation();
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
};
export default ProtectedRoute;
```

### File: `src/components/Extraction/ThresholdSlider.jsx`

**Language:** jsx

**File Size:** 524 bytes
**Created:** 2024-11-14T15:07:51.882679
**Modified:** 2024-11-14T15:07:51.882679

```jsx
import React, { useState } from 'react';
const ThresholdSlider = ({ onThresholdSelect, initialValue = 150 }) => {
  const [value, setValue] = useState(initialValue);
  const handleSliderChange = (event) => {
    const newValue = parseInt(event.target.value);
    setValue(newValue);
    onThresholdSelect(newValue);
  };
  return (
    <input
      type="range"
      min="0"
      max="255"
      value={value}
      onChange={handleSliderChange}
      className="slider"
    />
  );
};
export default ThresholdSlider;
```

### File: `src/components/Extraction/ColorPicker.jsx`

**Language:** jsx

**File Size:** 419 bytes
**Created:** 2024-11-14T15:07:29.152344
**Modified:** 2024-11-14T15:07:29.152344

```jsx
import React, { useState } from 'react';
import { SketchPicker } from 'react-color';
const ColorPicker = ({ onColorSelect }) => {
  const [color, setColor] = useState('#0000ff'); 
  const handleColorChange = (newColor) => {
    setColor(newColor.hex);
    onColorSelect(newColor.hex);
  };
  return <SketchPicker color={color} onChangeComplete={handleColorChange} />;
};
export default ColorPicker;
```

### File: `src/components/Extraction/ExtractionResult.jsx`

**Language:** jsx

**File Size:** 4713 bytes
**Created:** 2024-11-13T14:50:12.737344
**Modified:** 2024-11-13T14:50:12.737344

```jsx
import React from 'react';
import { useSelector } from 'react-redux';
const ExtractionResult = () => {
  const { finalImage, loading, error } = useSelector(
    (state) => state.extraction
  );
  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    return (
      <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded">
        <div className="flex items-start">
          <svg
            className="w-5 h-5 text-red-500 dark:text-red-400 mt-0.5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <h4 className="text-sm font-medium text-red-800 dark:text-red-400">
              Error
            </h4>
            <p className="mt-1 text-sm text-red-700 dark:text-red-300 whitespace-pre-line">
              {error}
            </p>
          </div>
        </div>
      </div>
    );
  }
  if (!finalImage) {
    return null;
  }
  return (
    <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 rounded">
      <h3 className="text-xl font-semibold mb-4 text-primary dark:text-secondary">
        Extracted Signature
      </h3>
      <div className="relative w-full h-48 rounded overflow-hidden">
        <img
          src={finalImage}
          alt="Extracted Signature"
          className="object-contain w-full h-full"
        />
      </div>
    </div>
  );
};
export default ExtractionResult;
```

### File: `src/components/Extraction/ImageUploader.jsx`

**Language:** jsx

**File Size:** 111895 bytes
**Created:** 2024-11-14T13:12:48.079420
**Modified:** 2024-11-14T13:12:48.079420

```jsx
import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axiosInstance from '../../utils/axiosInstance';
import { handleUploadError, logError } from '../../utils/errorHandling';
const ImageUploader = ({ onUpload }) => {
  const [uploading, setUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);
  const createPreview = (file) => {
    const preview = URL.createObjectURL(file);
    setPreviewUrl(preview);
  };
  const handleError = (error) => {
    logError(error, 'ImageUploader');
    setError(handleUploadError(error));
    setUploadProgress(0);
  };
  const onDrop = useCallback(
    async (acceptedFiles) => {
      try {
        setError(null);
        setUploading(true);
        setUploadProgress(0);
        const file = acceptedFiles[0];
        if (!file) {
          throw new Error('No file selected');
        }
        createPreview(file);
        const formData = new FormData();
        formData.append('file', file);
        const response = await axiosInstance.post(
          '/extraction/upload/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(percentCompleted);
            },
          }
        );
        onUpload(response.data);
        setUploadProgress(100);
      } catch (error) {
        handleError(error);
      } finally {
        setUploading(false);
      }
    },
    [onUpload]
  );
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxSize: 10 * 1024 * 1024, 
    multiple: false,
    disabled: uploading,
  });
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-[#f3a340] mb-6">
        Upload Document
      </h2>
      {previewUrl && (
        <div className="mb-6">
          <div className="aspect-video bg-black/20 rounded-lg overflow-hidden">
            <img
              src={previewUrl}
              alt="Preview"
              className="w-full h-full object-contain"
            />
          </div>
        </div>
      )}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 
          transition-all duration-200 ease-in-out
          ${isDragActive ? 'border-[#f3a340] bg-[#f3a340]/10' : 'border-[#f3a340]/50 hover:border-[#f3a340] hover:bg-[#f3a340]/5'}
          ${uploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}
        `}
      >
        <input {...getInputProps()} disabled={uploading} />
        <div className="text-center">
          <p className="text-lg mb-2">
            {uploading
              ? 'Uploading...'
              : 'Drag & drop a document here, or click to select a file'}
          </p>
          <p className="text-sm text-gray-400">
            Supported formats: JPG, PNG (max 10 MB)
          </p>
        </div>
      </div>
      {(uploading || uploadProgress > 0) && (
        <div className="mt-4">
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#f3a340] transition-all duration-300 ease-out"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          <p className="mt-2 text-center text-sm text-gray-600">
            {uploadProgress}% uploaded
          </p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}
    </div>
  );
};
export default ImageUploader;
```

### File: `src/components/Extraction/SignatureCropper.jsx`

**Language:** jsx

**File Size:** 22088 bytes
**Created:** 2024-11-14T15:03:13.818198
**Modified:** 2024-11-14T15:03:13.818198

```jsx
import React, { useState, useCallback } from 'react';
import ReactCrop from 'react-image-crop';
import 'react-image-crop/dist/ReactCrop.css';
const SignatureCropper = ({ imageUrl, onRegionSelect }) => {
  const [crop, setCrop] = useState();
  const [imageRef, setImageRef] = useState(null);
  const onImageLoad = useCallback((img) => {
    setImageRef(img);
  }, []);
  const handleCropComplete = useCallback(
    (crop, pixelCrop) => {
      if (imageRef && crop.width && crop.height) {
        onRegionSelect({
          x: Math.round(crop.x),
          y: Math.round(crop.y),
          width: Math.round(crop.width),
          height: Math.round(crop.height),
        });
      }
    },
    [imageRef, onRegionSelect]
  );
  if (!imageUrl) {
    return <div className="text-gray-600">Please upload an image first</div>;
  }
  return (
    <div className="w-full max-w-4xl mx-auto">
      <ReactCrop
        crop={crop}
        onChange={(c) => setCrop(c)}
        onComplete={handleCropComplete}
        aspect={undefined}
      >
        <img
          src={imageUrl}
          alt="Document for signature extraction"
          onLoad={(e) => onImageLoad(e.target)}
          className="max-w-full h-auto object-contain"
          style={{ maxHeight: '600px' }}
        />
      </ReactCrop>
      {crop && (
        <div className="mt-2 text-sm text-gray-600">
          Selected region: {Math.round(crop.width)} x {Math.round(crop.height)}{' '}
          pixels
        </div>
      )}
    </div>
  );
};
export default SignatureCropper;
```

### File: `src/hooks/redux.js`

**Language:** js

**File Size:** 234 bytes
**Created:** 2024-11-13T21:42:47.265632
**Modified:** 2024-11-13T21:42:47.265632

```js
import { useDispatch, useSelector } from 'react-redux';
export const useAppDispatch = () => useDispatch();
export const useAppSelector = useSelector;
```

### File: `src/pages/NotFound.jsx`

**Language:** jsx

**File Size:** 502 bytes
**Created:** 2024-11-11T13:06:58.236538
**Modified:** 2024-11-11T13:06:58.236538

```jsx
import React from 'react';
import { Link } from 'react-router-dom';
const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full p-6">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <p className="mb-6">The page you are looking for does not exist.</p>
      <Link to="/" className="text-primary hover:text-secondary">
        Go back to Home
      </Link>
    </div>
  );
};
export default NotFound;
```

### File: `src/pages/Dashboard.jsx`

**Language:** jsx

**File Size:** 41300 bytes
**Created:** 2024-11-14T15:43:49.204539
**Modified:** 2024-11-14T15:43:49.204539

```jsx
import React, { useState } from 'react';
import ImageUploader from '../components/Extraction/ImageUploader';
import SignatureCropper from '../components/Extraction/SignatureCropper';
import ColorPicker from '../components/Extraction/ColorPicker';
import ThresholdSlider from '../components/Extraction/ThresholdSlider';
import { useDispatch, useSelector } from 'react-redux';
import {
  selectRegion,
  processImage,
  clearError,
} from '../store/slices/extractionSlice';
import ExtractionResult from '../components/Extraction/ExtractionResult';
const Dashboard = () => {
  const dispatch = useDispatch();
  const [sessionId, setSessionId] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [color, setColor] = useState('#0000ff'); 
  const [threshold, setThreshold] = useState(150); 
  const { finalImage, loading, error } = useSelector(
    (state) => state.extraction
  );
  const handleUploadComplete = (result) => {
    setSessionId(result.id);
    setUploadedImageUrl(`http:
  };
  const handleRegionSelect = (region) => {
    setSelectedRegion(region);
    dispatch(selectRegion({ session_id: sessionId, ...region }));
  };
  const handleProcessImage = () => {
    if (selectedRegion && color && threshold) {
      dispatch(
        processImage({
          session_id: sessionId,
          x1: selectedRegion.x,
          y1: selectedRegion.y,
          x2: selectedRegion.x + selectedRegion.width,
          y2: selectedRegion.y + selectedRegion.height,
          color,
          threshold,
        })
      );
    }
  };
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">
        <h1 className="text-5xl font-bold text-center mb-8 text-white">
          Signature Extractor
        </h1>
        {}
        <section className="bg-gray-800 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-semibold text-center mb-4">
            Step 1: Upload Document
          </h2>
          <ImageUploader onUpload={handleUploadComplete} />
          {uploadedImageUrl && (
            <div className="mt-4 text-center">
              <img
                src={uploadedImageUrl}
                alt="Uploaded Document"
                className="rounded-lg border border-gray-700 shadow-md max-h-80 mx-auto"
              />
            </div>
          )}
        </section>
        {}
        {sessionId && uploadedImageUrl && (
          <>
            <hr className="border-gray-700 my-8" />
            <section className="space-y-8">
              {}
              <div className="bg-gray-800 rounded-lg p-6 space-y-4">
                <h2 className="text-2xl font-semibold text-center">
                  Step 2: Select Signature Area
                </h2>
                <SignatureCropper
                  imageUrl={uploadedImageUrl}
                  onRegionSelect={handleRegionSelect}
                />
              </div>
              <div className="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
                {}
                <div className="bg-gray-800 rounded-lg p-6 flex-1">
                  <h2 className="text-xl font-semibold mb-4">
                    Step 3: Choose Signature Color
                  </h2>
                  <ColorPicker onColorSelect={setColor} />
                </div>
                {}
                <div className="bg-gray-800 rounded-lg p-6 flex-1">
                  <h2 className="text-xl font-semibold mb-4">
                    Step 4: Adjust Threshold
                  </h2>
                  <ThresholdSlider
                    initialValue={threshold}
                    onThresholdSelect={setThreshold}
                  />
                  <p className="text-sm text-gray-400 mt-2">
                    Threshold Value: {threshold}
                  </p>
                </div>
              </div>
              {}
              <div className="flex justify-center">
                <button
                  onClick={handleProcessImage}
                  className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
                >
                  Extract Signature
                </button>
              </div>
            </section>
          </>
        )}
        {}
        {finalImage && (
          <>
            <hr className="border-gray-700 my-8" />
            <section className="bg-gray-800 rounded-lg p-6 space-y-4">
              <h2 className="text-2xl font-semibold text-center">
                Extracted Signature
              </h2>
              <ExtractionResult />
            </section>
          </>
        )}
        {}
        {error && (
          <div className="mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg">
            <h3 className="font-semibold">Error:</h3>
            <p>{error}</p>
            <button
              onClick={() => dispatch(clearError())}
              className="mt-2 bg-red-800 hover:bg-red-700 text-white py-1 px-3 rounded"
            >
              Dismiss
            </button>
          </div>
        )}
        {}
        {loading && (
          <div className="mt-4 text-center">
            <p>Loading...</p>
          </div>
        )}
      </div>
    </div>
  );
};
export default Dashboard;
```

### File: `src/pages/Login.jsx`

**Language:** jsx

**File Size:** 588 bytes
**Created:** 2024-11-13T16:10:26.334326
**Modified:** 2024-11-13T16:10:26.334326

```jsx
import React from 'react';
import LoginForm from '../components/Auth/LoginForm';
const Login = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <LoginForm />
    </div>
  );
};
export default Login;
```

### File: `src/pages/Register.jsx`

**Language:** jsx

**File Size:** 621 bytes
**Created:** 2024-11-13T16:10:35.835102
**Modified:** 2024-11-13T16:10:35.835102

```jsx
import React from 'react';
import RegisterForm from '../components/Auth/RegisterForm';
const Register = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <RegisterForm />
    </div>
  );
};
export default Register;
```

### File: `src/pages/Home.jsx`

**Language:** jsx

**File Size:** 398 bytes
**Created:** 2024-11-11T13:06:43.229095
**Modified:** 2024-11-11T13:06:43.229095

```jsx
import React from 'react';
const Home = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">
        Welcome to the Signature Extraction App
      </h1>
      <p className="text-lg">
        Upload your documents, extract signatures, and manage your subscriptions
        seamlessly.
      </p>
    </div>
  );
};
export default Home;
```

### File: `src/store/index.js`

**Language:** js

**File Size:** 819 bytes
**Created:** 2024-11-13T21:44:26.806285
**Modified:** 2024-11-13T21:44:26.806285

```js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import extractionReducer from './slices/extractionSlice';
import paymentReducer from './slices/paymentSlice';
export const store = configureStore({
    reducer: {
        auth: authReducer,
        extraction: extractionReducer,
        payment: paymentReducer,
    },
});
```

### File: `src/store/slices/paymentSlice.js`

**Language:** js

**File Size:** 1571 bytes
**Created:** 2024-11-11T12:59:09.696155
**Modified:** 2024-11-11T12:59:09.696155

```js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
export const processPayment = createAsyncThunk(
    'payment/processPayment',
    async (paymentData, { rejectWithValue, getState }) => {
        try {
            const { auth } = getState();
            const response = await axios.post('http:
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${auth.token}`,
                },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);
const paymentSlice = createSlice({
    name: 'payment',
    initialState: {
        status: null,
        loading: false,
        error: null,
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(processPayment.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(processPayment.fulfilled, (state, action) => {
                state.loading = false;
                state.status = action.payload.status;
            })
            .addCase(processPayment.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload.message || 'Payment processing failed';
            });
    },
});
export default paymentSlice.reducer;
```

### File: `src/store/slices/extractionSlice.js`

**Language:** js

**File Size:** 45875 bytes
**Created:** 2024-11-14T15:23:28.123256
**Modified:** 2024-11-14T15:23:28.123256

```js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../utils/axiosInstance';
export const uploadImage = createAsyncThunk(
    'extraction/uploadImage',
    async (formData) => {
        const response = await axiosInstance.post('/extraction/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    }
);
export const selectRegion = createAsyncThunk(
    'extraction/selectRegion',
    async ({ session_id, x1, y1, x2, y2 }) => {
        const response = await axiosInstance.post('/extraction/select_region', {
            session_id, x1, y1, x2, y2
        });
        return response.data;
    }
);
export const processImage = createAsyncThunk(
    'extraction/processImage',
    async ({ session_id, x1, y1, x2, y2, color, threshold }) => {
        const response = await axiosInstance.post('/extraction/process_image', {
            session_id, x1, y1, x2, y2, color, threshold
        }, { responseType: 'blob' });
        return URL.createObjectURL(response.data); 
    }
);
const extractionSlice = createSlice({
    name: 'extraction',
    initialState: {
        loading: false,
        error: null,
        uploadProgress: 0,
        finalImage: null,
        sessionId: null,
    },
    reducers: {
        clearError(state) {
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(uploadImage.pending, (state) => { state.loading = true; })
            .addCase(uploadImage.fulfilled, (state, action) => {
                state.loading = false;
                state.sessionId = action.payload.id; 
            })
            .addCase(uploadImage.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
            .addCase(processImage.pending, (state) => { state.loading = true; })
            .addCase(processImage.fulfilled, (state, action) => {
                state.loading = false;
                state.finalImage = action.payload;
            })
            .addCase(processImage.rejected, (state, action) => { state.loading = false; state.error = action.error.message; });
    }
});
export const { clearError } = extractionSlice.actions;
export default extractionSlice.reducer;
```

### File: `src/store/slices/authSlice.js`

**Language:** js

**File Size:** 33483 bytes
**Created:** 2024-11-13T21:22:29.105032
**Modified:** 2024-11-13T21:22:29.105032

```js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../utils/axiosInstance';
export const loginUser = createAsyncThunk(
    'auth/loginUser',
    async ({ email, password }, { rejectWithValue }) => {
        try {
            const data = new URLSearchParams();
            data.append('username', email);
            data.append('password', password);
            const response = await axiosInstance.post('/auth/login', data, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Login error details:', error.response?.data);
            if (error.response?.data?.detail) {
                return rejectWithValue(error.response.data);
            }
            return rejectWithValue({ detail: 'Login failed' });
        }
    }
);
export const registerUser = createAsyncThunk(
    'auth/registerUser',
    async ({ email, password }, { rejectWithValue }) => {
        try {
            const response = await axiosInstance.post('/auth/register', {
                email,
                password
            });
            return response.data;
        } catch (error) {
            console.error('Registration error details:', error.response?.data);
            if (error.response?.data?.detail) {
                return rejectWithValue(error.response.data);
            }
            return rejectWithValue({ detail: 'Registration failed' });
        }
    }
);
const authSlice = createSlice({
    name: 'auth',
    initialState: {
        user: null,
        token: localStorage.getItem('token') || null,
        isAuthenticated: !!localStorage.getItem('token'),
        loading: false,
        error: null,
    },
    reducers: {
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem('token');
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(loginUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.loading = false;
                state.token = action.payload.access_token;
                state.isAuthenticated = true;
                localStorage.setItem('token', action.payload.access_token);
            })
            .addCase(loginUser.rejected, (state, action) => {
                state.loading = false;
                if (Array.isArray(action.payload?.detail)) {
                    state.error = action.payload.detail.map(err => err.msg).join(', ');
                } else {
                    state.error = action.payload?.detail || 'Login failed';
                }
            })
            .addCase(registerUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(registerUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
            })
            .addCase(registerUser.rejected, (state, action) => {
                state.loading = false;
                if (Array.isArray(action.payload?.detail)) {
                    state.error = action.payload.detail.map(err => err.msg).join(', ');
                } else {
                    state.error = action.payload?.detail || 'Registration failed';
                }
            });
    },
});
export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
```

