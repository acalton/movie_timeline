from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/timeline')
def timeline():
    default = '0'
    actor = request.args.get('actor', default)
    print(actor == 'Arnold Schwarzenegger')
    actor_data = 'null'
    if actor == 'Arnold Schwarzenegger':
        actor_data = {'hercules': {'title': 'Hercules in New York',
                                   'year': 1970,
                                   'director': "Arthur Allan Seidelman"},
                      'conan': {'title': 'Conan the Barbarian',
                                'year': 1982,
                                'director': "John Milius"},
                      'terminator': {'title': 'The Terminator',
                                     'year': 1984,
                                     'director': "James Cameron"},
                      'running': {'title': 'The Running Man',
                                  'year': 1987,
                                  'director': "Paul Michael Glaser"},
                      'kinder': {'title': 'Kindergarten Cop',
                                 'year': 1990,
                                 'director': "Ivan Reitman"},
                      'terminator2': {'title': 'Terminator 2: Judgement Day',
                                      'year': 1991,
                                      'director': "James Cameron"},
                      'jingle': {'title': 'Jingle All the Way',
                                 'year': 1996,
                                 'director': "Brian Levant"},
                      'batman': {'title': 'Batman & Robin',
                                 'year': 1997,
                                 'director': "Joel Schumacher"}
                      }
        for key, value in actor_data.items():
            print(key, value)
            print(value['title'])
    return render_template("timeline.html", actor=actor, actor_data=actor_data)


if __name__ == '__main__':
    app.run()