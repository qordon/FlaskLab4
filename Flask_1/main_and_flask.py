from flask import Flask, render_template, url_for, request
from flask import jsonify
import random
from db import insert_temperatures, get_temperatures, update_levels, get_limits, clear_database, set_heater_state, \
    get_heater_state
import threading
import time
import Tkinter_Manager

M1 = 14
M2 = 32

min_temperature_limit = 0
max_temperature_limit = 0


def start_tkinter():
    root = Tkinter_Manager.Window()
    root.mainloop()


def check_heater():
    interval = 5
    while True:
        generated_temperature = random.randint(M1, M2)
        insert_temperatures(generated_temperature)
        if generated_temperature < min_temperature_limit:
            set_heater_state(1)
        else:
            set_heater_state(0)
        time.sleep(interval)


app = Flask(__name__)

states_lamp = {'hall': True, 'brightness': 0}
states_temperature = {'hall': 26}


@app.route('/')
def index():
    return render_template('index.html',
                           states=states_lamp,
                           states_temperature=states_temperature,
                           limits=[min_temperature_limit, max_temperature_limit])


@app.route('/lamp')
def switch_lamp():
    states_lamp['hall'] = not states_lamp['hall']
    return jsonify({'hall': states_lamp['hall']})


@app.route('/brightness/<value>', methods=['GET'])
def change_brightness(value):
    states_lamp['brightness'] = int(value)
    return value


@app.route('/temperature/', methods=['GET'])
def temperature():
    last_temperatures = []
    last_dates = []
    min_temperature_limit, max_temperature_limit = get_limits()
    for record in get_temperatures(10):
        last_temperatures.append(record[1])
        last_dates.append(str(record[0][10:19]))
    states_temperature['hall'] = last_temperatures[-1]
    return jsonify({'temperatures': last_temperatures,
                    'dates': last_dates,
                    'heater_state': get_heater_state(),
                    'min': min_temperature_limit,
                    'max': max_temperature_limit})


@app.route('/set_temperature_limits/<values>', methods=['GET'])
def set_temperature_limits(values):
    global min_temperature_limit, max_temperature_limit
    limits = values.split("_")
    min_temperature_limit = float(limits[0])
    max_temperature_limit = float(limits[1])

    print(f"MIN : {min_temperature_limit}, MAX : {max_temperature_limit}")

    update_levels(min_temperature_limit, max_temperature_limit)
    return values


if __name__ == '__main__':
    min_temperature_limit, max_temperature_limit = get_limits()

    tkinter_thread = threading.Thread(target=start_tkinter)
    tkinter_thread.daemon = True
    tkinter_thread.start()

    temperature_thread = threading.Thread(target=check_heater, args=())
    temperature_thread.daemon = True
    temperature_thread.start()

    app.run(debug=False, use_reloader=False)
