# Deploying to PythonAnywhere

These steps host RoadWatch Perth on a free PythonAnywhere account at `https://diptadg.pythonanywhere.com`, using SQLite on disk and demo data that resets every day.

## 1. Clone the repository

Open a **Bash console** on PythonAnywhere (Consoles tab) and run:

```bash
cd ~
git clone https://github.com/diptadg/roadwatch-perth.git
```

## 2. Create the virtual environment

```bash
cd ~/roadwatch-perth
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 3. Create `.env`

```bash
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" > .env
echo "MAIL_SERVER=" >> .env
chmod 600 .env
```

An empty `MAIL_SERVER` turns email sharing off. The share button then reports "not configured" instead of waiting for an SMTP connection that free accounts can't make. WhatsApp sharing still works.

## 4. Create the database and load demo data

```bash
.venv/bin/flask --app app db upgrade
.venv/bin/flask --app app seed-demo
```

`db upgrade` prints each Alembic log line twice. That is a known logging quirk, not an error.

## 5. Create the web app

On the **Web** tab:

1. **Add a new web app** → **Manual configuration** (not the "Flask" option) → **Python 3.13**.
2. **Virtualenv**: `/home/diptadg/roadwatch-perth/.venv`
3. **Static files**: URL `/static/`, directory `/home/diptadg/roadwatch-perth/roadwatch/static`
4. **WSGI configuration file**: open the linked file, delete everything in it, and paste in the contents of [`deploy/pythonanywhere_wsgi.py`](../deploy/pythonanywhere_wsgi.py).
5. **Force HTTPS**: on.
6. Click **Reload**, then open `https://diptadg.pythonanywhere.com`.

If the page shows an error, check the **error log** linked from the Web tab.

## 6. Reset the demo every day

The demo admin password is public in the README, so anyone can change data on the live site. A daily reset puts it back. On the **Tasks** tab, add a daily scheduled task (times are in UTC):

```bash
cd /home/diptadg/roadwatch-perth && .venv/bin/flask --app app reset-demo --yes
```

`reset-demo` deletes all users, reports, comments, confirmations, notifications and status notes, then loads fresh demo data.

## Updating the live site

```bash
cd ~/roadwatch-perth
git pull
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app app db upgrade
```

Then click **Reload** on the Web tab.

## Free-tier limits

- **Keeping it running:** free web apps stop after three months unless you click **Run until 3 months from today** on the Web tab. PythonAnywhere emails a reminder first.
- **Outbound internet:** free accounts can only reach an allowlist of sites. If `photon.komoot.io` isn't on that list, address autocomplete returns no suggestions. Typing an address by hand still works.
- **Visitors' browsers:** Tailwind and Chart.js load from CDNs in the visitor's browser, so the allowlist doesn't affect them.
