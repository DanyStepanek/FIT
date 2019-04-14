/************************************************************ 
 *  About: Scanner is the first part of Lexical analysis.   *
 *		   Scanner takes input file and analyze each line.  *
 *		   Detects lexems and divides them into the tables. *
 *	Tables: identifiers: x, a, i, sum,                      *
 *			literals: "music", 5, 5.2,                      *
 *			keywords: IF, THEN, DO, WHILE, BEGIN,           *
 *					  END, NILL,                            *	
 *	 		separators: (),{},                              *
 *			operators: +, -, *, /, =,                       *
 *			comments:                                       *
 ************************************************************
 *	IFJ projekt: "Implementace prekladace                   *
 *				  imperativniho jazyka IFJ18."              *
 *	Author(s): Daniel Stepanek (xstepa61)                   *
 *	Date: 11.10.2018                                        *
 *	VUT FIT Brno 2BIT                                       *
 *                                                          *
 ***********************************************************/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include "Token.h"


enum defaultWords{
	DEF,	//0
	DO,	
	ELSE,
	END,
	IF,
	NOT,
	NIL,
	THEN,
	WHILE
};


