#include <stdlib.h>
#include <string.h>

#include "dynamic_string.h"


#define DYNAMIC_STRING_LEN 8 /// Inicialization lenght of string.


void dynamic_string_clear(DString*s)
{
	s->length = 0;
	s->string[s->length] = '\0';
}


bool dynamic_string_init(DString*s)
{
	if (!(s->string = (char *) malloc(DYNAMIC_STRING_LEN)))
	{
		return false;
	}

	dynamic_string_clear(s);
	s->alloc = DYNAMIC_STRING_LEN;

	return true;
}


void dynamic_string_free(DString*s)
{
	free(s->string);
}


bool dynamic_string_add_char(DString*s , char c){
	if (s->length + 1 >= s->alloc)
	{
		unsigned int new_size = s->length + DYNAMIC_STRING_LEN+1;
		if (!(s->string = (char *) realloc(s->string, new_size)))
		{
			return false;
		}
		s->alloc = new_size;
	}

	s->string[s->length++] = c;
	s->string[s->length] = '\0';

	return true;
}


bool dynamic_string_add_const_str(DString*s ,char *input_string)
{

	unsigned int str_length = strlen(input_string);

	if (s->length + str_length + 1 >= s->alloc)
	{
		unsigned int new_size = s->length + str_length + 1;
		if (!(s->string = (char *) realloc(s->string, new_size)))
		{
			return false;
		}
		s->alloc= new_size;
	}

	s->length += str_length;
	strcat(s->string, input_string);
	s->string[s->length] = '\0';

	return true;
}


int dynamic_string_cmp_const_str(DString*s , char *input_string)
{
	return strcmp(s->string, input_string);
}


bool dynamic_string_copy(DString *src, DString *dest)
{
	unsigned int new_length = src->length;
	if (new_length >= dest->alloc)
	{
		if (!(dest->string = (char *) realloc(dest->string, new_length + 1)))
		{
			return false;
		}
		dest->alloc = new_length + 1;
	}

	strcpy(dest->string, src->string);
	dest->length = new_length;

	return true;
}
