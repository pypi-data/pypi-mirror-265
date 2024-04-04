#include <Otto.h>
Otto Otto;

#define LeftLeg 2 // left leg pin, servo[0]
#define RightLeg 3 // right leg pin, servo[1]
#define LeftFoot 4 // left foot pin, servo[2]
#define RightFoot 5 // right foot pin, servo[3]
#define Buzzer 13 //buzzer pin

void setup() {
  Otto.init(LeftLeg, RightLeg, LeftFoot, RightFoot, true, Buzzer);
  Otto.home();
}

void loop() {
  Otto.moonwalker(3, 1000, 25, 1); //LEFT moonwalk
  delay(1000); // wait for 1 second
  Otto.moonwalker(3, 1000, 25, -1); //RIGHT moonwalk
  delay(1000); // wait for 1 second
}