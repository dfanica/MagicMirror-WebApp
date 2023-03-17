from flask import Flask,render_template,redirect,request
import os
import subprocess

app = Flask(__name__, instance_relative_config=True)

# GPIO Commands
pwr_press = "raspi-gpio set 12 op dl && sleep 0.1 && raspi-gpio set 12 op dh"
menu_press = "raspi-gpio set 1 op dl && sleep 0.1 && raspi-gpio set 1 op dh"
left_press = "raspi-gpio set 8 op dl && sleep 0.1 && raspi-gpio set 8 op dh"
aim_assist_press = "raspi-gpio set 8 op dl && sleep 0.1 && raspi-gpio set 8 op dh"
right_press = "raspi-gpio set 7 op dl && sleep 0.1 && raspi-gpio set 7 op dh"
view_mode_press = "raspi-gpio set 7 op dl && sleep 0.1 && raspi-gpio set 7 op dh"
auto_press = "raspi-gpio set 25 op dl && sleep 0.1 && raspi-gpio set 25 op dh"
input_select_press = "raspi-gpio set 25 op dl && sleep 0.1 && raspi-gpio set 25 op dh"
combo_press = "raspi-gpio set 1 op dl && sleep 0.1 && raspi-gpio set 12 op dl && sleep 0.1 && raspi-gpio set 12 op dh && sleep 1 && raspi-gpio set 1 op dh"

# Helper functions
def getDisplayState():
    state = subprocess.check_output(  
        'ddcutil getvcp d6 | grep -Po "(?<=sl=)(0x[0-9a-f]+)"',
        shell=True
    )
    if state.strip() == b'0x01':
        return 'on'
    elif state.strip() == b'0x05':
        return 'off'
    else:
        return 'unknown'

def getAudioOutputState():
    state = subprocess.check_output(
        'if cat /proc/asound/card*/pcm*p/sub*/hw_params | grep -q "access"; then echo 1; else echo 0; fi',
        shell=True
    )
    if state.strip() == b'1':
        return 'on'
    else:
        return 'off'

def setDisplayBrightness(brightness_level):
    state = getDisplayState()
    # Turn the display on if off
    if state == 'off':
        os.system('ddcutil setvcp d6 1')
    os.system('ddcutil setvcp 10 {0}'.format(brightness_level))
    return {
        "service": "display_brightness_level", 
        "online": state,
        "value": '{0}'.format(brightness_level)
    }

# Root Route
@app.route('/')
def index():
    # Grab "menu_on" get param
    menu_on = request.args.get('menu_on')
    return render_template('webpage.html', menu_on=menu_on)

# GPIO Monitor Controls Routes
@app.route('/q')
def pwrPress():
    os.system(pwr_press)
    return redirect('/')

@app.route('/w')
def menuPress():
    os.system(menu_press)
    return redirect('/?menu_on=1')

@app.route('/e')
def leftPress():
    os.system(left_press)
    return redirect('/?menu_on=1')

@app.route('/aim_assist')
def aimAssistPress():
    os.system(aim_assist_press)
    return redirect('/')

@app.route('/r')
def rightPress():
    os.system(right_press)
    return redirect('/?menu_on=1')

@app.route('/view_mode')
def viewModePress():
    os.system(view_mode_press)
    return redirect('/')

@app.route('/t')
def autoPress():
    os.system(auto_press)
    return redirect('/?menu_on=1')

@app.route('/input_select')
def inputSelectPress():
    os.system(input_select_press)
    return redirect('/')

@app.route('/service-menu')
def comboPress():
    os.system(combo_press)
    return redirect('/')

# API Routes
@app.route('/api/audio-output')
def statusAudioOuput():
    return {
        "service": "audio_output",
        "status": getAudioOutputState()
    }

@app.route('/api/display-state')
def statusDisplay():
    return {
        "service": "display_state",
        "power": getDisplayState()
    }

@app.route('/api/display-on')
def switchDisplayOn():
    state = getDisplayState()
    # Turn the display on if off
    if state == 'off':
        os.system(combo_press)
    return statusDisplay()

@app.route('/api/display-off')
def switchDisplayOff():
    state = getDisplayState()
    # Turn the display off if on
    if state == 'on':
        os.system('ddcutil setvcp d6 5')
    return statusDisplay()

@app.route('/api/display-brightness')
def getDisplayBrightness():
    brightness = '0'
    # Check online state of display
    state = getDisplayState()
    # Set brighness to current level only if online
    if state == 'on':
        brightness = subprocess.check_output(
            'ddcutil getvcp 10 | grep -Po "(?<=\\s)([0-9]+)(?=\,)"',
            shell=True
        )
    return {
        "service": "display_brightness_level", 
        "online": state,
        "value": brightness.strip()
    }

@app.route('/api/display-brightness/<int:brightness_level>')
def setDisplayBrightnessAPI(brightness_level):
    return setDisplayBrightness(brightness_level)

if __name__ == '__main__':
    print("Start")
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    app.run(host='0.0.0.0', port=80)

