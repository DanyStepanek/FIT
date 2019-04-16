#include <student/gpu.h>

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <iostream>


/// \addtogroup gpu_side Implementace vykreslovacího řetězce - vykreslování trojúhelníků
/// @{

/**
 * @brief This function should draw triangles
 *
 * @param gpu gpu 
 * @param nofVertices number of vertices
 */
void gpu_drawTriangles(GPU *const gpu, uint32_t nofVertices)
{

  /// \todo Naimplementujte vykreslování trojúhelníků.
  /// nofVertices - počet vrcholů
  /// gpu - data na grafické kartě
  /// Vašim úkolem je naimplementovat chování grafické karty.
  /// Úkol je složen:
  /// 1. z implementace Vertex Pulleru
  /// 2. zavolání vertex shaderu pro každý vrchol
  /// 3. rasterizace
  /// 4. zavolání fragment shaderu pro každý fragment
  /// 5. zavolání per fragment operací nad fragmenty (depth test, zápis barvy a hloubky)
  /// Více v připojeném videu.
  (void)gpu;
  (void)nofVertices;

}

/// @}
