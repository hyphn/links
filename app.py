"""

URL/LINK SHORTENER.

:copyright: (c) 2017 Jakeoid.
:license: MIT, see LICENSE.md for details.

"""

# KYOUKAI
from kyoukai import Kyoukai
from kyoukai import util
# HOUSEKEEPING
from random import randint
from os import walk, path
import json
import time
# MIMETYPE
import mimetypes
# DATABASE
import rethinkdb as r

# ############################

settings = None

with open('settings.json') as settingsfile:
    settings = json.load(settingsfile)

# ############################

# SERVER.
ip = settings['server']['ip']
port = settings['server']['port']

# DATABASE.
dbname = settings['database']['name']
tbname = settings['database']['redirect_table']

# META.
siteurl = settings['meta']['siteurl']

# ############################

app = Kyoukai(__name__)
conn = r.connect(db=dbname)

# ############################


def insertMeta(fileinput):
    """Insert meta tags for the webpage."""
    output = fileinput

    output = output.replace(
        '{{NAME}}', settings['meta']['name'])
    output = output.replace(
        '{{DESCRIPTION}}', settings['meta']['description'])
    output = output.replace(
        '{{TYPE}}', settings['meta']['type'])
    output = output.replace(
        '{{TYPE-PLURAL}}', settings['meta']['plural'])
    output = output.replace(
        '{{SITEURL}}', settings['meta']['siteurl'])

    return output

# ############################


# Site Index.
@app.route("/")
async def index(ctx):
    """Display the homepage of the website."""
    with open("templates/index.html") as file:
        readfile = file.read()

        database = list(r.table(tbname).run(conn))

        totalchars = 0
        totaluses = 0

        linkstable = "<table>\n<thead>\n<th>Original</th>\n<th>Date</th>\n<th>Link</th>\n<th>Uses</th>\n</thead>\n<tbody>\n"

        for value in database:
            totalchars = totalchars + \
                int(len(value['redirect_url']) - len(value['id']))

            try:
                totaluses = totaluses + value['count']
            except:
                pass

            linkstable = linkstable + "<tr>"
            linkstable = linkstable + "<td><a href=\"" + \
                value['redirect_url'] + "\">" + \
                value['redirect_url'] + "</a></td>"

            linkstable = linkstable + "<td>" + \
                time.strftime('%B %-d, %Y',
                              time.localtime(value['epoch'])) + "</td>"

            linkstable = linkstable + "<td><a href=\"" + siteurl + \
                value['id'] + "\">" + siteurl + "/" + \
                value['id'] + "</a></td>"

            try:
                linkstable = linkstable + "<td>" + \
                    str(value['count']) + "</td>"
            except:
                linkstable = linkstable + "<td>0</td>"

            linkstable = linkstable + "</tr>"

        linkstable = linkstable + "\n</tbody>"
        linkstable = linkstable + "\n</table>"

        readfile = readfile.replace("{ URLS_SHORTENED }", str(len(database)))
        readfile = readfile.replace("{ CHARACTERS }", str(totalchars))
        readfile = readfile.replace("{ TOTAL_USES }", str(totaluses))
        readfile = readfile.replace(
            "{ TOTAL_CHAR_SAVED }", str(totalchars * totaluses))
        readfile = readfile.replace("{ TABLE }", linkstable)

        return util.as_html(readfile)


# Redirect & Assets.
@app.route('/<ourid>')
async def assets(ctx, ourid):
    """Serve the content of the server."""
    try:
        location = 'static/' + ourid
        filetype = ourid.split('.')[1]

        with open(location, mode='rb') as file:
            stream = file.read()

        header = {
            'Content-Type': mimetypes.guess_type(location)[0]
        }

        return util.Response(stream, status=200, headers=header)
    except:
        response = r.table(tbname).get(ourid).run(conn)

        statisticTable = r.table(tbname).get(ourid).run(conn)

        try:
            newcount = statisticTable['count'] + 1
        except:
            newcount = 1

        r.table(tbname).get(ourid).update({"count": newcount}).run(conn)

        if response is None:
            return util.Response(status=404)

        if settings['monetise']['enabled']:
            with open(settings['templates']['monetise']) as file:
                stream = file.read()

            stream = stream.replace("{ LINK }", statisticTable['redirect_url'])

            header = {
                'Content-Type': "text/html"
            }

            return util.Response(stream, status=200, headers=header)
        else:
            return util.Response("<meta http-equiv=\"refresh\" content=\"0; url=" + statisticTable['redirect_url'] + "/\" />", status=200)

# ############################

# Run our App.
app.run(ip=ip, port=port)
