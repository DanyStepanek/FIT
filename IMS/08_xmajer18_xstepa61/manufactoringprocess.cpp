#include "manufactoringprocess.hpp"

ManufacturingProcess::ManufacturingProcess(unsigned employee_count, unsigned pressbrake_count, unsigned sheet_count){
  this->pressbrake_count = pressbrake_count;
  this->employee_count = employee_count;
  this->sheet_count = sheet_count;

}

void ManufacturingProcess::Behavior() {
  PressBrake.SetCapacity(this->pressbrake_count);
  EmployeeStore.SetCapacity(this->employee_count);

  total_start_time = Time;

  //Sheet delivery from storage to laser
  Wait(Normal(5, 1));
  Enter(SheetStore, this->sheet_count);

  if (SheetStore.Used() == this->sheet_count){
    (new LaserProcess(this->employee_count, this->pressbrake_count))->Activate();
  }



}
