/************************************************************************
 *	IFJ projekt: "Implementace prekladace                       	*
 *				  imperativniho jazyka IFJ18."      	*
 *	Author(s): Daniel Stepanek (xstepa61) ,David Triska (xtrisk05) 	*
 *	Date: 25.11.2018                                            	*
 *	VUT FIT Brno 2BIT                                           	*
 *                                                                  	*
 ************************************************************************/


#ifndef SYMTABLE_H_INCLUDED
#define SYMTABLE_H_INCLUDED

#include <stdbool.h>

#include "rstring.h"
#include "dynamic_string.h"
#include "parser.h"


typedef struct Data{
	int id;
	int length;
	int category;
	char* value;
	bool global;
	bool defined;
	DString *params;
	
} Data;

typedef struct Node{
	unsigned long key;
	Data *data;
	struct Node * l_ptr;
	struct Node * r_ptr;
	
	
} Node;



/*
	DJB2 pro vytvoreni unikatniho klice uzlu stromu, z jeho identifikatrou
	http://www.cse.yorku.ca/~oz/hash.html
*/
unsigned long djb2(char* , int );

/*---------------------------------------------------*/
/*				   Node								 */
/****************************************************/
typedef enum{
	tNIL,			//kvuli scanneru (tNIL) protoze tam uz  je NIL jednou definovany
	INT,
	FLOAT,
	CHAR,
	STRING
}dat_type_enum;

typedef enum{
	CONSTANT,
	VARIABLE,
	FUNCTION
}catg_enum;

void Node_init(Node** );
/*
	Funkce vytvori novy uzel, pokud neexistuje, pokud existuje aktualizuje jeho category
*/

/*
	Vraci ukazatel na nove vytvorenou instanci Data, pokud se jedna o funkci volat Data_fce_fill
	@param catg_enum cat - kategorie (constant, variable, function)
	@param Data * data - ukazatel na strukturu Data, ze ktery prekopiruje udaje 

*/
//Data* Data_construct(catg_enum , Data * );
/*	
	@param Node** root - ukazatel na uzel
	
*/
void Node_create(Node** ,int , Token * );
void Node_actualize(Node** , int , Token* );
Node* find_Node(Node** , char* );
Data* toData(Token * );
void print_tree(Node** );
void Node_delete(Node** , char* );
void Tree_delete(Node** );

#endif
