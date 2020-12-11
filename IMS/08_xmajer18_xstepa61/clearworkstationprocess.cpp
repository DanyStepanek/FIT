#include "clearworkstationprocess.hpp"

void ClearWorkstationProcess::Behavior(){

    int pieces_count = CutoutPieceStore.Used();
    Leave(CutoutPieceStore, pieces_count);

  }
