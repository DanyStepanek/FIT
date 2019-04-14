/****************************************************************
 *	Author: Daniel Stepanek										*
 *	FIT VUT Brno												*
 *	Date: 15. 11. 2018											*
 *																*	
 ****************************************************************
 *	Filtrovani signalu 											*
 ****************************************************************
 *  parametry: File Rows Lines Constant							*
 *	File: vstupni soubor										*
 *	Rows: <0;x> (unsigned int)									*
 *	Lines: souradnice y(x)	(unsigned int)						*
 *	Constant: uprava signalu (y(x)= y(x) * C) (unsigned int)	*
 ****************************************************************/ 


#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<ctype.h>


FILE *input_f;

int filter(int c, int Constant){

	return (c *= Constant);

}

int fill_in(int **spectrum, FILE *file, int R, unsigned int L, int Constant, int filtering){
	int i = 0;
	int c = 0;
	int d = 0;
	int lines = 0;
	
	
	while((c = fgetc(file)) != EOF && i < R){
		if(isdigit(c)){
			c -= 48.0;
			while(isdigit(d = fgetc(file))){
				c = (c * 10) + (d - 48);
			}
			
			if(filtering == 1){
				c = filter(c, Constant);
			}
			
			if(c < L)
				spectrum[i][c]= c;
			else {
				printf("Range is smaller than input number!\n");
				exit(1);
			}

			i++;	
		}			
	}
	lines = i;
	return lines;

}

void print_matrix(int **spectrum, int R, unsigned int L, int rows){
	
	int k = 0;
	
	for(int i=0;i<rows;i++){
		for(int j=0;j<L;j++){
			if(spectrum[i][j] >= 0){
				for(int l=0;l<j;l++){
					if(spectrum[i-1][l] != -1 || spectrum[i+1][l] != -1){
						k=l;
						while(k<j){
							printf("x");
							k++;
						}
						l = k;
					}
					else {
						
						printf("|");
					}
					
				}
				printf("x");
				printf(" %d", (i+1));
			}
		}
		printf("\n");
	}
}


int main(int argc, char *argv[]){
	int R = atoi(argv[2]);
	unsigned int L = atoi(argv[3]) + 1; 
	unsigned int C = 0;
	int filtering = 0;
	int *spectrum[R];

	
/*********************************************************/

	if(argc < 4)
		return(1);

	if(argc == 5){
		C = atoi(argv[4]);
		filtering = 1;
	}

	for(int i=0;i<R;i++){
		spectrum[i] = (int *) malloc(sizeof(int)*L);
		for(int j=0;j<L;j++)
			spectrum[i][j] = -1;
	}

	input_f = fopen(argv[1], "r");

/********************************************************/
	
	int lines = fill_in(spectrum, input_f, R, L, C, filtering);

	print_matrix(spectrum, R, L, lines);	

/*******************************************************/		
	for(int i=0;i<R;i++)
		free(spectrum[i]);
	
	fclose(input_f);

return 0;
}
