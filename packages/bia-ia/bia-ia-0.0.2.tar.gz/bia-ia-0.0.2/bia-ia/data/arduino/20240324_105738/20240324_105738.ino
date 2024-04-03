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
  Otto.walk(2,1000,1);
  Otto.walk(2,1000,-1);
  Otto.turn(2,1000,1);
  Otto._tone(10, 3, 1);
  Otto.bendTones (100, 200, 1.04, 10, 10);
  Otto.home();
  delay(100);
  Otto.turn(2,1000,-1);
  Otto.bend (1,500,1);
  Otto.bend (1,2000,-1);
  Otto.shakeLeg (1,1500, 1);
  Otto.home();
  delay(100); 
  Otto.shakeLeg (1,2000,-1);
  Otto.moonwalker(3, 1000, 25,1);
  Otto.moonwalker(3, 1000, 25,-1);
  Otto.crusaito(2, 1000, 20,1);
  Otto.crusaito(2, 1000, 20,-1);
  delay(100);
  Otto.flapping(2, 1000, 20,1);
  Otto.flapping(2, 1000, 20,-1);
  delay(100);
  Otto.swing(2, 1000, 20);
  Otto.tiptoeSwing(2, 1000, 20);
  Otto.jitter(2, 1000, 20);
  Otto.updown(2, 1500, 20);
  Otto.ascendingTurn(2, 1000, 50);
  Otto.jump(1,500);
  Otto.home();
  delay(100);
  Otto.sing(S_cuddly);
  Otto.sing(S_OhOoh);
  Otto.sing(S_OhOoh2);
  Otto.sing(S_surprise);
  Otto.sing(S_buttonPushed);
  Otto.sing(S_mode1);
  Otto.sing(S_mode2);
  Otto.sing(S_mode3);
  Otto.sing(S_sleeping);
  Otto.sing(S_fart1);
  Otto.sing(S_fart2);
  Otto.sing(S_fart3);
  Otto.sing(S_happy);
  Otto.sing(S_happy_short);
  Otto.sing(S_superHappy);
  Otto.sing(S_sad);
  Otto.sing(S_confused);
  Otto.sing(S_disconnection);
  delay(100);
  Otto.playGesture(OttoHappy);
  Otto.playGesture(OttoSuperHappy);
  Otto.playGesture(OttoSad);
  Otto.playGesture(OttoVictory);
  Otto.playGesture(OttoAngry);
  Otto.playGesture(OttoSleeping);
  Otto.playGesture(OttoFretful);
  Otto.playGesture(OttoLove);
  Otto.playGesture(OttoConfused);
  Otto.playGesture(OttoFart);
  Otto.playGesture(OttoWave);
  Otto.playGesture(OttoMagic);
  Otto.playGesture(OttoFail);
}