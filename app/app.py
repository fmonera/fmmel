#/usr/bin/env python
from aioflask import Flask, redirect, url_for, request, make_response, jsonify
import aiohttp
import asyncio
import pymelcloud
import os
import contextlib
import random
import string
import types
import json

app = Flask(__name__)

devices = None
device = None
zone = None
secret = "x" # Initial value, it will change


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/help', methods=['POST', 'GET'])
def help():
    if secure(request) != "Ok": return "Auth error" 

    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return jsonify(links)

@app.route('/')
def index():
    return jsonify("FMMel - Ecodan Control")

@app.route('/token', methods=['POST', 'GET'])
async def token():
    global devices
    global device
    global zone
    global secret
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
    elif request.method == 'GET':
        user = request.args.get('user')
        password = request.args.get('password')
    else:
        return "Error"

    token = await pymelcloud.login(user, password)
    if len(token) == 0:
        return "Error"
    devices = await pymelcloud.get_devices(token)
    device = devices[pymelcloud.DEVICE_TYPE_ATW][0]
    zone = device.zones[0]

    # Generate random string to be used as temporary password
    chars = 20
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = chars))
    secret = str(ran)

    resp = make_response(jsonify(secret))
    resp.set_cookie('fmmel', secret)

    return resp

def secure(request):
    global secret
    s = "x"
    try:
        s = request.cookies.get('fmmel')
    except:
        pass

    if s != secret:
        # Try to see if there is a param named secret
        if request.method == 'POST':
            try:
                s = request.form['secret']
            except:
                pass
        elif request.method == 'GET':
            try:
                s = request.args.get('secret')
            except:
                pass

    if s != secret:
        return "Auth error"
    else:
        return "Ok"


@app.route('/update', methods=['POST', 'GET'])
async def update():
    if secure(request) != "Ok": return "Auth error"

    global device
    global zone

    await device.update()
    zone = device.zones[0]
    
    return jsonify("Ok")

@app.route('/zone', methods=['POST', 'GET'])
def zone():
    if secure(request) != "Ok": return "Auth error"
    global zone
    _zone_conf = dict()
    _zone_conf['name'] = zone.name
    _zone_conf['operation_mode'] = zone.operation_mode
    _zone_conf['operation_modes'] = zone.operation_modes
    _zone_conf['flow_temperature'] = zone.flow_temperature
    _zone_conf['prohibit'] = zone.prohibit
    _zone_conf['return_temperature'] = zone.return_temperature
    _zone_conf['room_temperature'] = zone.room_temperature
    _zone_conf['status'] = zone.status
    _zone_conf['target_cool_flow_temperature'] = zone.target_cool_flow_temperature
    _zone_conf['target_flow_temperature'] = zone.target_flow_temperature
    _zone_conf['target_heat_flow_temperature'] = zone.target_heat_flow_temperature
    _zone_conf['target_temperature'] = zone.target_temperature
    return jsonify(_zone_conf)

@app.route('/device', methods=['POST', 'GET'])
def device():
    if secure(request) != "Ok": return jsonify("Auth error")
    global device
    return jsonify(device._device_conf)

@app.route('/device/name', methods=['POST', 'GET'])
def device_name():
    if secure(request) != "Ok": return "Auth error"
    global device
    return jsonify(device.name)

@app.route('/zone/name', methods=['POST', 'GET'])
def zone_name():
    if secure(request) != "Ok": return "Auth error"
    global zone
    return jsonify(zone.name)

@app.route('/zone/flow_temperature', methods=['POST', 'GET'])
def zone_flow_temperature():
    if secure(request) != "Ok": return "Auth error"
    global zone
    #return {"flow_temperature": zone.flow_temperature}
    return jsonify(zone.flow_temperature)

@app.route('/zone/return_temperature', methods=['POST', 'GET'])
def zone_return_temperature():
    if secure(request) != "Ok": return "Auth error"
    global zone
    return jsonify(zone.return_temperature)

@app.route('/zone/target_heat_flow_temperature', methods=['POST', 'GET'])
def zone_target_heat_flow_temperature():
    if secure(request) != "Ok": return "Auth error"
    global zone
    return jsonify(zone.target_heat_flow_temperature)

@app.route('/zone/set_target_heat_flow_temperature/<value>', methods=['POST', 'GET'])
async def zone_set_target_heat_flow_temperature(value):
    if secure(request) != "Ok": return "Auth error"
    global zone
    await zone.set_target_heat_flow_temperature(value)
    return jsonify("Ok")

@app.route('/zone/status', methods=['POST', 'GET'])
def zone_status():
    if secure(request) != "Ok": return "Auth error"
    global zone
    return jsonify(zone.status)

@app.route('/device/status', methods=['POST', 'GET'])
def device_status():
    if secure(request) != "Ok": return "Auth error"
    global device
    return jsonify(device.status)

@app.route('/device/tank_temperature', methods=['POST', 'GET'])
def device_tank_temperature():
    if secure(request) != "Ok": return "Auth error"
    global device
    return jsonify(device.tank_temperature)


@app.route('/device/target_tank_temperature', methods=['POST', 'GET'])
def device_target_tank_temperature():
    if secure(request) != "Ok": return "Auth error"
    global device
    return jsonify(device.target_tank_temperature)

@app.route('/device/set/<parameter>/<value>', methods=['POST', 'GET'])
async def device_set(parameter, value):
    if secure(request) != "Ok": return "Auth error"
    global device
    await device.set({parameter: value})
    return jsonify("Ok")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
