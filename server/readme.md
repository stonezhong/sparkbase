# To build server
```bash
npm run-script build-dev
```

# Configuration
Configurations are stored in file `config.json`.
<table>
<tr>
    <th>Config name</td>
    <th>Type</td>
    <th>Description</th>
    <th>Example</th>
</tr>

<tr>
    <td>enable_js_debug</td>
    <td>bool</td>
    <td>Set to true if you want to debug javascript, for production, pls set to false</td>
    <td>true</td>
</tr>

<tr>
    <td>secret_key</td>
    <td>string</td>
    <td>secrect key for django password encryption. See doc <a href="https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY">here</a></td>
    <td>"blah..."</td>
</tr>

</table>

# Create superuser
```bash
python manage.py createsuperuser
```

# Make migrations
You need to do it once you change the model.
```bash
python manage.py makemigrations
```

```bash
# once you do the makemigrations, you need to push the change to db
python manage.py migrate
```