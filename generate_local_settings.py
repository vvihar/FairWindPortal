from django.core.management.utils import get_random_secret_key

SECRET_KEY = get_random_secret_key()
TEXT = f'SECRET_KEY = "{SECRET_KEY}"'

f = open("FairWindPortal/local_settings.py", mode="w", encoding="utf-8")
f.write(
    "import os\n"
    + TEXT
    + "\nBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\nDATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.sqlite3',\n        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),\n    }\n}\nDEBUG = True"
)
f.close()
