/********************************************************************
 *	IFJ projekt: "Implementace prekladace                       	*
 *				  imperativniho jazyka IFJ18."      				*
 *	Author(s): Daniel Stepanek (xstepa61)                       	*
 *	Date: 29.11.2018                                            	*
 *	VUT FIT Brno 2BIT                                           	*
 *                                                                  *
 *******************************************************************/



#ifndef _DYNAMIC_STRING_H_INCLUDED
#define _DYNAMIC_STRING_H_INCLUDED


#include <stdbool.h>
#include <stdio.h>

/**
 * @struct Representation of dynamic string.
 */
typedef struct
{
	char *string; /// string ened by '\0' byte
	unsigned int length; /// lenght of string
	unsigned int alloc; /// number of chars alocated for string
} DString;


/**
 * Inicialization of dynamic string.
 *
 * @param s Pointer to dynamic string.
 * @return True if inicialization was successful, false otherwise.
 */
bool dynamic_string_init(DString* );

/**
 * Frees alocated memory for dynamic string.
 *
 * @param s Pointer to dynamic string.
 */
void dynamic_string_free(DString* );

/**
 * Clear dynamic string content.
 *
 * @param s Pointer to dynamic string.
 */
void dynamic_string_clear(DString* );

/**
 * Add char to the end of dynamic string.
 *
 * @param s Dynamic string.
 * @param c Char to add.
 * @return True if it was successful, false otherwise.
 */
bool dynamic_string_add_char(DString* , char  );

/**
 * Add constant string to the end of dynamic string.
 *
 * @param s Dynamic string.
 * @param const_string Constant string.
 * @return True if it was successful, false otherwise.
 */
bool dynamic_string_add_const_str(DString* , char * );

/**
 * Compare dynamic string with constant string.
 *
 * @param dynamic_string Dynamic string.
 * @param const_string Constant string.
 * @return Returns 1, 0, or -1, according as the s1 is greater than, equal to, or less than the s2.
 */
int dynamic_string_cmp_const_str(DString* , char *);

/**
 * Copy src string to dest string.
 *
 * @param src Source string.
 * @param dest Destination string.
 * @return True if it was successful, false otherwise.
 */
bool dynamic_string_copy(DString * , DString * );


#endif // _DYNAMIC_STRING_H
