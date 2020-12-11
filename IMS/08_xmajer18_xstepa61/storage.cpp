#include "storage.hpp"

void StoreProcess::Behavior(){

  if(PressBrakeOutStore.Full()){

    Enter(EmployeeStore, 1);
    unsigned pressbrakeout_used = PressBrakeOutStore.Used();
    Leave(PressBrakeOutStore, pressbrakeout_used);

    Wait(Normal(5, 1));

    Leave(EmployeeStore, 1);

    total_end_time = Time;
  }

}
