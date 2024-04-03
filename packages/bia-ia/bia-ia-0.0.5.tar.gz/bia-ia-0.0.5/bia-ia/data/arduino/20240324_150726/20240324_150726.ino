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
  Otto.crusaito(2, 1000, 20, 1); // Left crusaito dance move
  Otto.crusaito(2, 1000, 20, -1); // Right crusaito dance move
  Otto.shakeLeg(1, 1500, 1); // Left leg shake dance move
  Otto.shakeLeg(1, 2000, -1); // Right leg shake dance move
  Otto.moonwalker(3, 1000, 25, 1); // Left moonwalker dance move
  Otto.moonwalker(3, 1000, 25, -1); // Right moonwalker dance move
  Otto.swing(2, 1000, 20); // Swing dance move
  Otto.tiptoeSwing(2, 1000, 20); // Tiptoe swing dance move
  Otto.jitter(2, 1000, 20); // Jitter dance move
  Otto.updown(2, 1500, 20); // Up and down dance move
  Otto.ascendingTurn(2, 1000, 50); // Ascending turn dance move
  Otto.playGesture(OttoHappy); // Happy dance gesture
  Otto.playGesture(OttoSuperHappy); // Super happy dance gesture
  Otto.playGesture(OttoSad); // Sad dance gesture
  Otto.playGesture(OttoVictory); // Victory dance gesture
  Otto.playGesture(OttoAngry); // Angry dance gesture
  Otto.playGesture(OttoSleeping); // Sleeping dance gesture
  Otto.playGesture(OttoFretful); // Fretful dance gesture
  Otto.playGesture(OttoLove); // Love dance gesture
  Otto.playGesture(OttoConfused); // Confused dance gesture
  Otto.playGesture(OttoFart); // Fart dance gesture
  Otto.playGesture(OttoWave); // Wave dance gesture
  Otto.playGesture(OttoMagic); // Magic dance gesture
  Otto.playGesture(OttoFail); // Fail dance gesture
}