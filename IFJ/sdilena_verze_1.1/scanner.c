/* TODO: neurcita velikost poli,
		viceradkovy komentar,
		desetinna cisla,
		upravit funkci na stringy(pokud chybi druha uvozovka " tak to detekuje jako promennou (isVar())
spoustet jako: ./vystupTest nejakysoubor
*/
#include "scanner.h"

FILE *file;



int isKeyWord(char *str){
	if(strcmp("def",str)==0)
		return DEF;
	if(strcmp("do",str)==0)
		return DO;
	if(strcmp("else",str)==0)
		return ELSE;
	if(strcmp("end",str)==0)
		return END;
	if(strcmp("if",str)==0)
		return IF;
	if(strcmp("not",str)==0)
		return NOT;
	if(strcmp("nil",str)==0)
		return NIL;
	if(strcmp("then",str)==0)
		return THEN;
	if(strcmp("while",str)==0)
		return WHILE;
	
	return -1;	//if "str" is not a keyword
}

void isOthers(int c){

	while(c != ' ' && c != '\n'){
		c = fgetc(file);
	}
	printf("ignoring\n");
}

void isDigit(int c){
	int num[10];
	int i = 0;
		
	while(c >= 48 && c <= 57){
		num[i] = c - 48;
		c = fgetc(file);
		i++;
			
	}
	for(int j=0;j<i;j++){
		printf("cislo: %d\n",num[j]);
	}
}

void isOperator(int c){

	printf("operator: %c\n",c);
}

void isComment(int c){
	int com[20];
	int i = 0;
	
	while((c = fgetc(file)) != '\n'){
		com[i] = c;
		i++;
	}
	printf("comment: ");
	for(int j=0;j<i;j++){
		printf("%c",com[j]);
	}
	printf("\n");
}

void isString(int c){
	int string[20];
	int i = 0;
	int correct = 1;	//if correct then == "1"
	while((c = fgetc(file)) != '"'){
		if(c == '\n'){		//If string doesn't have second ",so it's not a string.
			correct = 0;
			for(int j=0;j<i;j++){
				string[j] = '\0';
			}
			break;		
		}
		string[i] = c;
		i++;
		
	}
	if(correct == 1){
		string[i++] = '\0';
		printf("string: ");
	
		for(int j=0;j<i;j++){
			printf("%c",string[j]);
		}
		printf("\n");	
	}
	
}

void isVar(int c){
	int var[30];
	int i = 0;
	char str[30];
	int keyword = -1;

	while(c !=' ' && c != '\n'){
		var[i] = c;
		c = fgetc(file);
		i++;
	}
	var[i++] = '\0';
	//convert to char array "str"
	for(int j=0;j<=i;j++){
		str[j] = var[j];
	}

	//keyword checking
	keyword = isKeyWord(str);
	enum defaultWords key = keyword;
	
	switch (key){

	case 0:
		printf("DEF\n");
		break;
	case 1:
		printf("DO\n");
		break;
	case 2:
		printf("ELSE\n");
		break;
	case 3:
		printf("END\n");
		break;
	case 4:
		printf("IF\n");
		break;
	case 5:
		printf("NOT\n");
		break;
	case 6:
		printf("NIL\n");
		break;
	case 7:
		printf("THEN\n");
		break;
	case 8:
		printf("WHILE\n");
		break;
	default:
		printf("variable: ");
		for(int j=0;j<i;j++){
			printf("%c",var[j]);
		}
	
		printf("\n");
	}
	
}



/* Precte kazdy znak v souboru a identifikuje ho.
 *@param - vstupni soubor "file"
 */
void read(FILE* file){
	int c = 0;
	//potom nahradim if(c != EOF)....		
	while ((c = fgetc(file)) != EOF){
		
//		printf("c: %c\n",c);
//		printf("hodnota c: %d\n",c);		

		//Condition for numbers
		if(c >= 48 && c <= 57){
			isDigit(c);
			//break;
		}
		//Condition for operators
		if(c == '='|| c== '*'|| c== '/' || c == '+' || c == '-'){
			isOperator(c);
			//break;
		}
		//Condition for identifiers
		if((c == '_') || (c >= 97 && c <= 122)){
			isVar(c);
			//break;
		}
		//Condition for strings
		if(c == '"'){
			isString(c);
			//break;
		}
		
		if(c == 35){
			isComment(c);
		}		
		
		if(c >= 65 && c <= 90){
			isOthers(c);
		}
	}		
}

void sendToken(){

}

int main(int argc,char *argv[]){

	if(argc == 2){
		file = fopen(argv[1],"r");
		if (file == NULL){
			fprintf(stderr,"The file cannot be opened.\n");
			exit(1);
		}

		read(file);	

		fclose(file);
	}
return 0;
}
