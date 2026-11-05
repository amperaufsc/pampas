from Jetson import GPIO

from ..hardware_controller import HardwareController


# TODO: Implement this according to the HardwareController interface
class JetsonController(HardwareController):
    '''Hardware integration layer for Nvidia's Jetson.'''

    def __init__(self, left, right, PWM):
        GPIO.setmode(GPIO.BOARD)
        self.pwm = GPIO.PWM(PWM, 200)
        self.pwm.start(0)
        self.left = left
        self.right = right
        GPIO.setup(self.left, GPIO.OUT)
        GPIO.setup(self.right, GPIO.OUT)

    def steer(self, control):
        self.pwm.ChangeDutyCycle(abs(control))
        if control >= 0:
            GPIO.output(self.left, True)
            GPIO.output(self.right, False)
        else:
            GPIO.output(self.left, False)
            GPIO.output(self.right, True)

    def shutdown(self):
        GPIO.cleanup()
