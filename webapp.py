from flask import Flask,render_template,redirect,request
import os
import subprocess

app = Flask(__name__, instance_relative_config=True)
print("Done")

## ROOT Route

@app.route('/')
def index():
    # Grab "menu_on" get param
    menu_on = request.args.get('menu_on')
    return render_template('webpage.html', menu_on=menu_on)

## GPIO Monitor Controls Routes

@app.route('/q')
def pwrPress():
    os.system ("raspi-gpio set 12 op dl && sleep 0.1 && raspi-gpio set 12 op dh")
    return redirect('/')

@app.route('/w')
def menuPress():
    os.system ("raspi-gpio set 1 op dl && sleep 0.1 && raspi-gpio set 1 op dh")
    return redirect('/?menu_on=1')

@app.route('/e')
def leftPress():
    os.system ("raspi-gpio set 8 op dl && sleep 0.1 && raspi-gpio set 8 op dh")
    return redirect('/?menu_on=1')
@app.route('/aim_assist')
def aimAssistPress():
    os.system ("raspi-gpio set 8 op dl && sleep 0.1 && raspi-gpio set 8 op dh")
    return redirect('/')

@app.route('/r')
def rightPress():
    os.system ("raspi-gpio set 7 op dl && sleep 0.1 && raspi-gpio set 7 op dh")
    return redirect('/?menu_on=1')
@app.route('/view_mode')
def viewModePress():
    os.system ("raspi-gpio set 7 op dl && sleep 0.1 && raspi-gpio set 7 op dh")
    return redirect('/')

@app.route('/t')
def autoPress():
    os.system ("raspi-gpio set 25 op dl && sleep 0.1 && raspi-gpio set 25 op dh")
    return redirect('/?menu_on=1')
@app.route('/input_select')
def inputSelectPress():
    os.system ("raspi-gpio set 25 op dl && sleep 0.1 && raspi-gpio set 25 op dh")
    return redirect('/')

@app.route('/service-menu')
def comboPress():
    os.system("raspi-gpio set 1 op dl && sleep 0.1 && raspi-gpio set 12 op dl && sleep 0.1 && raspi-gpio set 12 op dh && sleep 1 && raspi-gpio set 1 op dh")
    return redirect('/')

## API Routes

@app.route('/api/audio-output')
def statusAudioOuput():
    state = subprocess.check_output(
        'if cat /proc/asound/card*/pcm*p/sub*/hw_params | grep -q "access"; then echo 1; else echo 0; fi',
        shell=True
    )
    return {
        "service": "audio_output",
        "status": state.strip()
    }

@app.route('/api/display-state')
def statusDisplay():
    state = subprocess.check_output(
        'if tvservice --status | grep -q "HDMI CEA"; then echo 1; else echo 0; fi',
        shell=True
    )
    return {
        "service": "display_state",
        "power": state.strip()
    }

@app.route('/api/display-on')
def switchDisplayOn():
    state = subprocess.check_output(
        'if tvservice --status | grep -q "HDMI CEA"; then echo 1; else echo 0; fi',
        shell=True
    )
    # Turn the display on if off
    if state.strip() == b'0': os.system('tvservice --preferred && sudo chvt 6 && sudo chvt 7')
    return statusDisplay()

@app.route('/api/display-off')
def switchDisplayOff():
    state = subprocess.check_output(
        'if tvservice --status | grep -q "HDMI CEA"; then echo 1; else echo 0; fi',
        shell=True
    )
    # Turn the display off if on
    if state.strip() == b'1': os.system('tvservice -o')
    return statusDisplay()

if __name__=="__main__":
    print("Start")
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    app.run(host='0.0.0.0', port=80)
