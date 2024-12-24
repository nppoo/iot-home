from flask import Flask, render_template, request

app = Flask(__name__)
devices = {
    "cctv": {"status": "off"},
    "watertank": {"level": 10, "status": "off"},
    "light": {"status": "off"},
    "fan": {"status": "off"},
    "fridge": {"status": "off"},
    "doorbell": {"message": ""},
    "ac": {"status": "off", "temperature": 25},
    "temperature_sensor": {"temperature": 34}
}
def check_device_statuses():
    alerts = []
    if devices["cctv"]["status"] == "off":
        alerts.append("CCTV is offline!")
    if devices["watertank"]["level"] < 20:
        alerts.append("Water tank is running low!")
    if devices["watertank"]["level"] > 95:
        alerts.append("Water tank is full!")
    if devices["ac"]["status"] == "off":
        alerts.append("ac is off!")
    if devices["temperature_sensor"]["temperature"] > 28:  # Check temperature
        alerts.append("Temperature exceeds 28°C!")
    return alerts

@app.route('/')
def index():
    alerts = check_device_statuses()    
    return render_template('index.html', devices=devices, alerts=alerts)

@app.route('/update_device', methods=['POST'])
def update_device():
    device_name = request.form['device']
    action = request.form['action']
    if action == 'toggle':
        devices[device_name]['status'] = 'on' if devices[device_name]['status'] == 'off' else 'off'
    elif action == 'message':
        devices["doorbell"]["message"] = request.form['message']
    alerts = check_device_statuses()
    if action == 'ac_temperature':
        devices["ac"]["temperature"] = int(request.form['temperature'])
    if devices['ac']['status'] == 'on':
            devices['temperature_sensor']['temperature'] = devices['ac']['temperature']
    
    alerts = check_device_statuses() 
    return render_template('index.html', devices=devices, alerts=alerts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



