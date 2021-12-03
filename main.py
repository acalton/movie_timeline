from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


def get_movie_data(actor_name):
    actor_url = 'http://localhost:4000/search/actor/' + actor_name  # Actor's movie data service
    json_data = requests.get(actor_url)
    actor_data = json.loads(json_data.text)
    return actor_data


def get_upper_limit(actor_data):
    upper_limit = 20  # prevent data overload on web app
    if len(actor_data[:1][0]['cast']) < 20:
        upper_limit = len(actor_data[:1][0]['cast'])
    return upper_limit


def create_movie_data_dict(actor_data):
    actor_data_dict = {}
    upper_limit = get_upper_limit(actor_data)

    for i in range(0, upper_limit):
        if "release_date" in actor_data[:1][0]['cast'][i]:
            if actor_data[:1][0]['cast'][i]["release_date"] != "":
                movie_info_dict = {
                    'rating': actor_data[:1][0]['cast'][i]['vote_average'],
                    'title': actor_data[:1][0]['cast'][i]['title'],
                    'character': actor_data[:1][0]['cast'][i]['character']
                }
                actor_data_dict[actor_data[:1][0]['cast'][i]['release_date']] = movie_info_dict

    return actor_data_dict


def get_personal_data(actor_name):
    first_name, last_name = actor_name.split()
    personal_url = 'http://127.0.0.1:5000/' + first_name + '/' + last_name  # Wiki scraper service
    personal_data = requests.get(personal_url)
    return personal_data.text


def get_birth_date(personal_data):
    birth_date = personal_data[0][personal_data[0].find("(") + 1:personal_data[0].find(")")]
    return birth_date


def get_death_date(personal_data):
    death_date = "Alive"
    for i in range(0, len(personal_data)):
        if personal_data[i].startswith('Died'):
            death_date = personal_data[i][personal_data[i].find("(") + 1:personal_data[i].find(")")]
    return death_date


def get_years_active(personal_data):
    years_active = "Unknown"
    for i in range(0, len(personal_data)):
        if personal_data[i].startswith('Years'):
            years_active = personal_data[i].split()
            years_active = years_active[2]
    return years_active


def get_spouse(personal_data):
    spouse = "Unmarried"
    for i in range(0, len(personal_data)):
        if personal_data[i].startswith('Spouse'):
            spouse = personal_data[i].split(' ', 1)
            spouse = spouse[1]
    return spouse


def remove_html_char(personal_data):
    personal_data = personal_data.replace("<body>", "")
    personal_data = personal_data.replace("<p>", "")
    personal_data = personal_data.split("<br>")
    return personal_data


def create_personal_data_dict(personal_data):
    personal_data = remove_html_char(personal_data)

    personal_data_dict = {
        'birth_date': get_birth_date(personal_data),
        'death_date': get_death_date(personal_data),
        'years_active': get_years_active(personal_data),
        'spouse': get_spouse(personal_data)
    }

    return personal_data_dict


@app.route('/timeline')
def timeline():
    default = '0'
    actor = request.args.get('actor', default)

    actor_data = get_movie_data(actor)
    personal_data = get_personal_data(actor)

    personal_data_dict = create_personal_data_dict(personal_data)
    actor_data_dict = create_movie_data_dict(actor_data)

    return render_template("timeline.html", actor=actor, actor_data=actor_data_dict,
                           personal_data=personal_data_dict)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
