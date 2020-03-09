# CRM-Backend-Flask

## Backend Set Up
```sh
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## DB Set Up
```sh
export DATABASE_URL="mysql+mysqlconnector://[user]:[password]@localhost/evolv"
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Start server
```sh
python3 manage.py runserver
```


## Thanks
forked from https://github.com/dternyak/React-Redux-Flask
 








