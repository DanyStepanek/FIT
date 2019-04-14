
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/
#include "RString.h"


RString * init_RString(){

	RString *newRS =  malloc(sizeof(RString));	// misto pro ukazatel
	newRS->aloc = 0;
	newRS->size = 0;
	return newRS;
}

int fill_RString(RString *s, char*c, int length){

	if(s != NULL /*&& s->string != NULL*/ && c != NULL){  // kontrola spravnosti ukazatelu

		s->string =  (char*) malloc(sizeof(char) * length); // alokace pameti pro pole znaku

		if(s->string != NULL){		// kontrola alokace pameti
			strcpy(s->string, c);	// vlozeni stringu do alok. pam
			s->size = length;
			s->aloc = length;
			return 0;
		}else{
			return -1;
		}

	}else {
		return -1;
	}

}

void free_RString(RString *s){
	
	free(s->string);
	free(s);
	s->string = NULL;
	s->size = 0;
	s->aloc = 0;
	s = NULL;
	
}