#include "pressbrakeprocess.hpp"

PressBrakeProcess::PressBrakeProcess(){
  this->tool_changed = 0;
}

void PressBrakeProcess::Behavior(){

  this->start_time = Time;

  while (1){
    //bending
    while(!(PressBrakeStore.Empty())){
      Leave(PressBrakeStore, 1);
      Wait(Normal(0.6, 0.1));
      Enter(PressBrakeOutStore, 1);
    }

    /**
    * if tool has been changed four times, release sources, end process
    * and activate store process
    * else change tool and return all pieces to the press brake store
    */
    if ((this->tool_changed == TOOL_MUST_BE_CHANGED_4)){
      this->end_time = Time;
      double pressbrake_duration = this->end_time - this->start_time;
      (*PressBrakeTimeStat)(pressbrake_duration);

      Leave(EmployeeStore, 1);
      Leave(PressBrake, 1);

      (new StoreProcess())->Activate();

      break;
    }
    else {
      Wait(Uniform(1, 2));
      this->tool_changed++;

      if((PressBrakeOutStore.Full() && PressBrakeStore.Empty())){
        Leave(PressBrakeOutStore, 200);
        Enter(PressBrakeStore, 200);
      }
    }
  }
}
