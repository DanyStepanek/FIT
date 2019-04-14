#include <iostream>

using namespace std;




int main(int argc, char** argv){
  
  if(argc == 8){
    for(int i = 0;i < 8;i++){
        cout << argv[i];
        cout << "\n";
    }
  }
  else if(argc == 6){
    for(int i = 0;i < 6;i++){
      cout << argv[i];
      cout << " ";
    }
    cout << "\n";
  }
  else{
    cerr << "Wrong count of parameters\n";
    exit(1);
  }

  return 0;
}
