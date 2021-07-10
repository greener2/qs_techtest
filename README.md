# qs_techtest
Written by Rob Greene

## Running this app

Before running the Flask server, please check the `.flaskenv` file first to set your environment variables:

- `FLASK_APP`: should point to `wsgi.py` as it is the app's entry point
- `FLASK_ENV`: should be set to `development`
- `DATABASE_URI`: should be set to a filepath that you have read/write access to

Once this is done, please open `flask shell` in your terminal and run the following code:

```
from qs_techtest.extensions import db
db.create_all()
exit()
```

This will make sure the database has the appropriate table created before using it.

Finally, run the server by running:

```shell
flask run
```

And to run unit tests, run:

```shell
python -m unittest
```