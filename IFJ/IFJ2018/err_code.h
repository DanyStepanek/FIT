/******************************************************************** 
 *  About: Error codes for all source files                         *
 *		                                                    *
 ********************************************************************
 *	IFJ projekt: "Implementace prekladace                       *
 *				  imperativniho jazyka IFJ18."      *
 *	Author(s): Daniel Stepanek (xstepa61)                       *
 *	Date: 18.11.2018                                            *
 *	VUT FIT Brno 2BIT                                           *
 *                                                                  *
 *******************************************************************/

#ifndef ERR_CODE_H_INCLUDED
#define ERR_CODE_H_INCLUDED

#include<stdio.h>
#include<stdlib.h>
#include<stdarg.h>



typedef enum err_code{
    ERR_LEX               = 20,
    ERR_SYNTAX            = 40,
    ERR_SEMANTIC          = 60,
    ERR_ZERO_DIVISION     = 80,
   
  
} ERR_CODE;

int call_error(int ,int );
#endif
