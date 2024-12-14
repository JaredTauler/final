import json

from flask import Flask, render_template
from shepherd_course_picker import data_maker

import os

# I really do not understand how to relatively get files within packages.

# Band aid fix
def find_directory(target_dir):
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        if target_dir in dirnames:
            return os.path.join(dirpath, target_dir)
    return None

app = Flask(
    __name__,
    template_folder=find_directory('templates'),
    static_folder=find_directory('static')
)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__json__()

def toJSON(object):
    return json.dumps(object, cls=CustomEncoder)


@app.route('/')
def home3():

    return render_template('programselect.html')

@app.route('/picker/<int:program_id>')
def home(program_id: int):
    return render_template('picker.html', program_id = program_id)

@app.route('/api/programs', methods=['GET'])
def picker():
    programs =data_maker.get_program_list()

    a = toJSON(programs)

    return a


@app.route('/api/programs/<int:program_id>', methods=['GET'])
def picker2(program_id: int):
    try:
        p = data_maker.get_program(
            program_id
        )
    except Exception as e:
        return {"error": str(e)}

    return toJSON(p)





if __name__ == '__main__':
    app.run()