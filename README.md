# SimpleMemo
Simple web-based memo application w/ Python Flask &amp; SQLite

## Requirements
Tested on python==3.12, flask==3.1.0, flask-sqlalchemy==3.1.1, flask-jwt-extended==4.1.1, python-dotenv==1.0.1  
```
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended python-dotenv
```
There must be .env file with JWT_SECRET_KEY variable at the root of the repository folder
```
JWT_SECRET_KEY = <your_secret_key>
```

## Note
By default, Flask debug mode is ON. 