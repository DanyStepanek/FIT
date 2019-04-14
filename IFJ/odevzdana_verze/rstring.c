
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/
#include "rstring.h"


RString * init_RString(){

	RString *newRS =  malloc(sizeof(struct rstring));	// misto pro ukazatel
	newRS->aloc = 0;
	newRS->size = 0;
	return newRS;
}

int fill_RString(RString *s, char*c, int length){

	if(s != NULL /*&& s->string != NULL*/ && c != NULL){  // kontrola spravnosti ukazatelu

		s->string = (char*) calloc((length+1),sizeof(char)); // alokace pameti pro pole znaku

		if(s->string != NULL){		// kontrola alokace pameti
			strcpy(s->string, c);	// vlozeni stringu do alok. pam
			s->size = length;
			s->aloc = length+1;
			return 0;
		}else{
			return -1;
		}

	}else {
		return -1;
	}

}

bool addstr_RString(RString *s, char* inputs){

	int inputs_len = strlen(inputs);
	
	if(s->size <= (inputs_len + 1)){
		int new_size = s->size + inputs_len + 1;		
		s->string = (char*) realloc(s->string, new_size);
		if(s->string == NULL){
			fprintf(stderr,"Reallocation failed\n");
			return false;
		}

		s->aloc = new_size;
	}
	
	
	s->size += strlen(inputs);
	strcat(s->string, inputs);
	s->string[s->size] = '\0';

	return true;
}

void free_RString(RString *s){
	
	free(s->string);
	s->string = NULL;
	s->size = 0;
	s->aloc = 0;
	free(s);
}






