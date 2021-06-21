# Responsive ambientlight

This software analyses a selected display and sends 3 arrays of colours of as many LEDs as input through serial. This aims to have a control board the the end of it, to receive the data and use LED strips to mimic the border colors of the selected display.

## Usage
The user needs to select which of the detected monitors is the one that wants to be tracked and how many LEDs each strip has. 
After that, there are 2 options available:
* Simulate: Shows a simulation of the LED strips on the screen so that the use can verify the behaviour.
* Start: Runs the tracking in the background and all the data is sent through serial.

## Developer notes
First of all, set up the virutual environment with all the necessary packages.
```
pipenv install --dev
```

To run the program in the developement environment simply run:
```
pipenv run python ambientlight.py
```