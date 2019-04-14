
/********************************************************************
 *	IFJ projekt: "Implementace prekladace                       	*
 *				  imperativniho jazyka IFJ18."      				*
 *	Author(s): Daniel Stepanek (xstepa61)                       	*
 *	Date: 10.11.2018                                            	*
 *	VUT FIT Brno 2BIT                                           	*
 *                                                                  *
 *******************************************************************/
#include<stdio.h>
#include<stdlib.h>

#include "scanner.h"
#include "parser.h"
#include "err_code.h"
#include "generator.h"



int main(){
	int check = 0;
	
	//inicializace struktury pro ukladani nactenych tokenu
	Tlist *t = init_Tlist();

	
	buffer = (char *) malloc(sizeof(char)*100);
	

	if(buffer == NULL){
		fprintf(stderr,"Buffer allocation failed\n");
		exit(1);
	}
	
	check = syntax();
		
	if(check != 0){
		if(check < 0)
			fprintf(stderr,"\n***\tTarget is incorrect\t***\n***\tOn line [%d]: Compilation failed.\t***\n",  -check);
		else
			fprintf(stderr,"\n***\tTarget is incorrect\t***\n***\tCompilation failed.\t***\n");
	}
	else { 
		generator_output_stream(stdout);
		fprintf(stdout, "\n***\tTarget is correct.\t***\n***\tCompilation succeeded.\t***\n");
	}

	
	//dealokace veskere alokovane pameti pouzite v Tlist
	free_Tlist(t);

	// dealokace pro scanner a parser
	free(buffer);
	//generator_clear_stream();
	
return 0;
}
