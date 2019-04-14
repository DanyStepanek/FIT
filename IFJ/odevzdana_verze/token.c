
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/
#include "token.h"



Token * init_Token(){

	Token *t = malloc(sizeof(Token));
	t->value = init_RString();
	t->id = 0;

	return t;
}

int fill_Token(Token* t, char* value, int length, int type){

	if(t != NULL){
		t->id = type;
		if(fill_RString(t->value, value, length) == 0){ // kontrola, zda vlozeni probeho v poradku
			return 0;
		} else {
			return -1;
		}
	}else {
		return -1;
	}

}

void free_Token(Token *t){
	free_RString(t->value);
	free(t);

}
