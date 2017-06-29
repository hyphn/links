# Link Shortener

Welcome to the link shortener site, here we have a script that will shorten urls for you and automatically via an API serve the link and redirect you to the new page (whilst displaying an ad for commerce reasons). Being relatively easy to setup all you need to get started is RethinkDB and Python.

**Note** This resource requires the use of a Database (more specifically RethinkDB), you cannot use this service without hosting this.

# Usage

### 1. Make sure you have the required dependencies.

```
pip install -r ./requirements.txt
```

### 2. Setup your configuration file.

```
cp settings.template.json settings.json
nano settings.json
```

### 3. Run the script and see what port it is running on.

```
python3.5 app.py
```

# Todo

- Add a way to configure different page setups.
- Add credits page for other people that contributed to project.
- Support for databases that arent RethinkDB (SQL & Mongo).
- Add POST endpoints for shortening URLs.
- Add a Token/Key system.

# Contributing

1. Fork repo.
2. Edit code.
3. Make a PR.
4. Submit said PR.

# License

A copy of the MIT license can be found in `LICENSE.md`
