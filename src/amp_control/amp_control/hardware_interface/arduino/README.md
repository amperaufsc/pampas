# Arduino Controller

This is a simple Arduino sketch that implements a serial interface to control the steering of the robot. It is used by the `ArduinoController` class in the `control` package.

## Requirements

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
arduino-cli core update-index
arduino-cli core install arduino:avr
```

## Flashing the Arduino

First, find the port of the Arduino board:

```bash
arduino-cli board list
````

Then, compile and upload the sketch to the Arduino board:

```bash
arduino-cli compile --fqbn arduino:avr:uno src/amp_motion/control/hardware/arduino/arduino_controller.ino
arduino-cli upload -p /dev/<PORT> --fqbn arduino:avr:uno src/amp_motion/control/hardware/arduino/arduino_controller.ino
```

## Troubleshooting

To monitor the serial output of the Arduino board, you can use the following command:

```bash
arduino-cli monitor -p /dev/<PORT> -c baudrate=115200
```
