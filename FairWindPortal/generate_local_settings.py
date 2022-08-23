from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)

f = open('local_settings.py', mode='w')
f.write("import os\n" + text +
        "\nBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\nDATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.sqlite3',\n        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),\n    }\n}\nDEBUG = True")
f.close()
