# djangoauthtoken
Django auth solution for Token creation/updation for a session.

## Add Djangoauthtoken in your project.

Add `djangoauthtoken` in your INSTALLED_APPS settings to see in action.

### Run make migratons command:

```
python manage.py makemigrations djangoauthtoken
```

## Run command to migrate:

```
python manage.py migrate
```

## Run command to create superuser

```
python manage.py createsuperuser
```


Things to do:

- [X] Add api for Token.
- [X] Add api for login.
- [X] Add api for RefreshToken.
- [X] Add manager for create token.
- [X] Add serializer for user.
- [X] Add manager for create user.
- [X] Add api for user sign up.
- [X] Add github Actions.
- [X] Add pypi module push in this code base.
- [] Add a custom command to delete invalid tokens.
- [] Update README with screenshots and other details.




