from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/timeline')
def timeline():
    default = '0'
    actor = request.args.get('actor', default)
    actor_url = 'http://localhost:4000/search/actor/' + actor

    json_data = requests.get(actor_url)
    actor_data = json.loads(json_data.text)
    actor_data_dict = {}
    for i in range(0, len(actor_data[:1][0]['cast'])):
        if actor_data[:1][0]['cast'][i]['release_date'] != "":
            movie_info_dict = {
                'rating': actor_data[:1][0]['cast'][i]['vote_average'],
                'title': actor_data[:1][0]['cast'][i]['title'],
                'character': actor_data[:1][0]['cast'][i]['character']
            }
            actor_data_dict[actor_data[:1][0]['cast'][i]['release_date']] = movie_info_dict

    # print(actor_data_dict["1985-12-20"]['title'])

    # print(actor_data[:1][0]['cast'][0]['title'])

    # year_title = actor_data[:1][0]['cast'][i]['release_date'] + ': ' + actor_data[:1][0]['cast'][i]['title']
    # more_info = 'Character: ' + actor_data[:1][0]['cast'][i]['character']

    return render_template("timeline.html", actor=actor, actor_data=actor_data_dict,
                           num_movies=len(actor_data[:1][0]['cast']))


if __name__ == '__main__':
    app.run()
