#include "err_code.h"


int call_error(int code, int specific){
	

	ERR_CODE type = code;
	
	switch (type){

	case 20:
		fprintf(stderr,"%d: LEX_ERROR\n", specific);
		break;
	case 40:
		fprintf(stderr,"%d: SYNTAX_ERROR\n",specific);
		break;
	case 60:
		fprintf(stderr,"%d: SEMANTIC_ERROR\n",specific);
		break;
	case 80:
		fprintf(stderr,"%d: INTERNAL_ERROR\n",specific);
		break;
	
	}
	
	return code;
	
}	
