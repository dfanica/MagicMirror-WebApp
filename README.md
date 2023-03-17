# MagicMirror-WebApp
Display Controls &amp; API


# Raspberry Pi GPIO Control with Flask

This is a Flask web application designed to control various features of a Raspberry Pi using GPIO pins. The application serves two purposes: first, it provides a web-based UI for controlling the Raspberry Pi GPIO pins, and second, it provides a REST API for controlling the Raspberry Pi from external programs.

## Getting Started

To run the application, you will need to install Flask and ddcutil. Once you have installed these packages, you can start the application by running `python webapp.py`.

## Application Structure

The application is structured as follows:

* `webapp.py`: This is the main application file. It contains the Flask routes and the API endpoints.
* `templates/`: This directory contains the HTML templates used by the application.
* `static/`: This directory contains static files used by the application, such as CSS stylesheets and JavaScript files.

### GPIO Monitor Controls Routes

- `/q`: Power press.
- `/w`: Menu press.
- `/e`: Left press.
- `/aim_assist`: Aim assist press.
- `/r`: Right press.
- `/view_mode`: View mode press.
- `/t`: Auto press.
- `/input_select`: Input select press.
- `/service-menu`: Combo press.

### API Routes

- `/api/audio-output`: Returns the current audio output status.
- `/api/display-state`: Returns the current display state (power on or off).
- `/api/display-on`: Switches the display on if it is currently off.
- `/api/display-off`: Switches the display off if it is currently on.
- `/api/display-brightness`: Returns the current display brightness level.
- `/api/display-brightness/<int:brightness_level>`: Sets the display brightness level to the specified value.

## GPIO Pins

The following GPIO pins are used by the application:

* Pin 1: Used for the menu button.
* Pin 7: Used for the right button and the view mode button.
* Pin 8: Used for the left button and the aim assist button.
* Pin 12: Used for the power button.
* Pin 25: Used for the input select button.

## Display Control

The display is controlled using ddcutil. The following commands are used:

* `ddcutil detect`: Detects the connected display.
* `ddcutil setvcp d6 1`: Turns on the display.
* `ddcutil setvcp d6 5`: Turns off the display.
* `ddcutil getvcp 10`: Gets the current brightness level of the display.
* `ddcutil setvcp 10 10`: Sets the brightness of the display to low.
* `ddcutil setvcp 10 100`: Sets the brightness of the display to high.

## Audio Output Control

The audio output is controlled using the ALSA API. The following commands are used:

* `cat /proc/asound/card*/pcm*p/sub*/hw_params`: Gets the current audio output state.
* `grep -q "access"`: Checks if the audio output is enabled.

## Service Menu

The service menu is accessed by pressing the menu and power buttons simultaneously. The following commands are used:

* `raspi-gpio set 1 op dl`: Sets GPIO pin 1 to low.
* `raspi-gpio set 12 op dl`: Sets GPIO pin 12 to low.
* `raspi-gpio set 12 op dh`: Sets GPIO pin 12 to high.
* `raspi-gpio set 1 op dh`: Sets GPIO pin 1 to high.

## Development

To run the application in development mode, uncomment the `app.run(debug=True, host="0.0.0.0", port="5000")` line in `webapp.py`.

## Production

To run the application in production mode, uncomment the `app.run(host='0.0.0.0', port=80)` line in `app.py`. Note that you will need to run the application as root to use port 80.

