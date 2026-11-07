// Steering actuator I/O board.
// Laptop -> Arduino:  "S,<duty>\n"   duty in [-90, 90], positive = steer left
// Arduino -> Laptop:  "T,<raw>,<limL>,<limR>\n"  every TELEMETRY_PERIOD_MS

// ---- Pins ----
const uint8_t PWM_PIN         = 9;   // motor driver PWM
const uint8_t LEFT_PIN        = 7;   // direction: left
const uint8_t RIGHT_PIN       = 8;   // direction: right
const uint8_t SENSOR_PIN      = A0;  // steering position sensor (analog)
const uint8_t LIMIT_LEFT_PIN  = 2;   // limit switch at the left end stop
const uint8_t LIMIT_RIGHT_PIN = 3;   // limit switch at the right end stop

const uint8_t LIMIT_TRIGGERED = LOW;
const unsigned long LIMIT_RELEASE_DEBOUNCE_MS = 10;  // triggers instantly, releases after 10 ms stable

// ---- Settings ----
const float MAX_DUTY = 90.0; // same cap as the PD saturation on the laptop
const unsigned long TIMEOUT_MS = 100 // no steering for this long -> stop
const unsigned long TELEMETRY_PERIOD_MS = 10; // 100 Hz

float steeringReference = 0.0;
unsigned long lastSteeringMs = 0;
unsigned long lastTelemetryMs = 0;
char buf[24];
uint8_t len = 0;

struct Limit {
  uint8_t pin;
  bool state;
  unsigned long lastTriggerMs;
};
Limit leftLimit  = {LIMIT_LEFT_PIN,  false, 0};
Limit rightLimit = {LIMIT_RIGHT_PIN, false, 0};

// Contact bounce: trigger immediately (safe direction), release only after a
// stable period.
bool readLimit(Limit &limit, unsigned long now) {
  if (digitalRead(limit.pin) == LIMIT_TRIGGERED) {
    limit.state = true;
    limit.lastTriggerMs = now;
  } else if (now - limit.lastTriggerMs > LIMIT_RELEASE_DEBOUNCE_MS) {
    limit.state = false;
  }
  return limit.state;
}

void steer(float reference) {
  reference = constrain(reference, -MAX_DUTY, MAX_DUTY);
  digitalWrite(LEFT_PIN,  reference >= 0);
  digitalWrite(RIGHT_PIN, reference <  0);
 // 0-100 % -> 0-255
 analogWrite(PWM_PIN, (uint8_t)(fabs(reference) * 2.55 + 0.5));
}

// Non-blocking line parser (readStringUntil would block up to 1 s).
void readSerial() {
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      buf[len] = '\0';
      if (len > 2 && buf[0] == 'S' && buf[1] == ',') {
        steeringReference = atof(buf + 2);
        lastSteeringMs = millis();
      }
      len = 0;
    } else if (len < sizeof(buf) - 1) {
      buf[len++] = ch;
    } else {
      len = 0;  // overflow: discard the garbage line
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PWM_PIN, OUTPUT);
  pinMode(LEFT_PIN, OUTPUT);
  pinMode(RIGHT_PIN, OUTPUT);
  pinMode(LIMIT_LEFT_PIN, INPUT_PULLUP);
  pinMode(LIMIT_RIGHT_PIN, INPUT_PULLUP);
  steer(0);
}

void loop() {
  readSerial();
  unsigned long now = millis();

  // Watchdog: laptop silent -> stop.
  steeringReference = (
      (now - lastSteeringMs > TIMEOUT_MS) ? 0.0 : steeringReference
  );

  // Limit switches: block motion further into a triggered end stop,
  // but still allow moving back out. Checked every loop, independent of the
  // laptop.
  bool left = readLimit(leftLimit, now);
  bool right = readLimit(rightLimit, now);
  if (left && steeringReference > 0) steeringReference = 0;
  if (right && steeringReference < 0) steeringReference = 0;

  steer(steeringReference);

  if (now - lastTelemetryMs >= TELEMETRY_PERIOD_MS) {
    lastTelemetryMs = now;
    Serial.print("T,");
    Serial.print(analogRead(SENSOR_PIN));
    Serial.print(',');
    Serial.print(left ? 1 : 0);
    Serial.print(',');
    Serial.println(right ? 1 : 0);
  }
}
