<?php
# IPP projekt 1
# @author Daniel Stepanek xstepa61@stud.fit.vutbr.cz

class Instruction{
	public $value;
	public $arg1;
	public $arg2;
	public $arg3;
	public $args;



	private function Fill($value, $arg1 = null, $arg2 = null, $arg3 = null){
		$this->value = strtoupper($value);
		$this->arg1 = $arg1;
		$this->arg2 = $arg2;
		$this->arg3 = $arg3;
		$this->args = array($arg1, $arg2, $arg3);
	}

	public function ToFill($word_arr, $param_count){
		switch($param_count){
			case 0:
				$this->Fill($word_arr[0]);
				break;
			case 1:
				$this->Fill($word_arr[0],$word_arr[1]);
				break;
			case 2:
				$this->Fill($word_arr[0],$word_arr[1],$word_arr[2]);
				break;
			case 3:
				$this->Fill($word_arr[0],$word_arr[1], $word_arr[2], $word_arr[3]);
				break;
		}
	}

	//The instruction method for determinaning what parameter is involved.
	//@params $string_type	var|symb|label|type
	//@params $string
	//@return $output_array	Empty if parameter $string is incorrect.
	public function CheckSyntax($string_type, $string){

		$output_array = [];

		switch ($string_type) {
			case "var":
			//frame@special_characters or alphanumeric characters
				preg_match('/(TF|LF|GF)@([\-\_\$\&\%\*\!\?\w]+)$/', $string, $output_array);
				break;

			case "symb":
			//frame@special_characters or alphanumeric characters
				preg_match('/(TF|LF|GF)@([\-\_\$\&\%\*\!\?\w]+)$/', $string, $output_array);
				if($output_array == []){
					preg_match('/(int)@([+-]?\d+)$/', $string, $output_array);
				}
				if($output_array == []){
					preg_match('/(bool)@(true|false)$/', $string, $output_array);
				}
				if($output_array == []){
					//frame@special_characters or alphanumeric characters or special escape sequences \[0-9][0-9][0-9]
					preg_match('/(string)@((\w*[\<\>\&\'\"\/\-]*(\\\[0-9][0-9][0-9])*\w*)*)$/', $string, $output_array);

				}
				if($output_array == []){
					preg_match('/(nil)@(nil)$/', $string, $output_array);
				}
				break;
			case "label":
				preg_match('/(\w+)$/', $string, $output_array);
				break;
			case "type":
				preg_match('/(int|string|bool)$/', $string, $output_array);
				break;
		}

		return $output_array;
	}


}

class InstructionFactory{

	public static function create(){
		return new Instruction();
	}
}

//Replace special characters to textformat.
function Replace($string){
	$pattern = '/\</';
	$replacement = '${0}&lt;';
	preg_replace($pattern, $replacement, $string);

	$pattern = '/\>/';
	$replacement = '${0}&gt;';
	preg_replace($pattern, $replacement, $string);

	$pattern = '/\&/';
	$replacement = '${0}&amp;';
	preg_replace($pattern, $replacement, $string);

	$pattern = '/\'/';
	$replacement = '${0}&apos;';
	preg_replace($pattern, $replacement, $string);

	$pattern = '/\"/';
	$replacement = '${0}&quot;';
	preg_replace($pattern, $replacement, $string);
}

//Parse each line, checking syntax by CheckSyntax function
//creating XML format of each instruction
//@param $line 	input line
//@param &$num_line	number of actual line
//@param $xml	XML main element
//@param $program XML root element containing all instructions.
//@return $err_code Corresponding output error values.
function Parse($line, &$num_line, $xml, $program){
	$err_code = 0;
	$KeyWords = array(
		"move" => array(2,"var","symb"),
		"createframe" => 0,
		"pushframe" => 0,
		"popframe" => 0,
		"defvar" => array(1,"var"),
		"call" => array(1,"label"),
		"return" => 0,
		"pushs" => array(1,"symb"),
		"pops" => array(1,"var"),
		"add" => array(3,"var","symb","symb"),
		"sub" => array(3,"var","symb","symb"),
		"mul" => array(3,"var","symb","symb"),
		"idiv" => array(3,"var","symb","symb"),
		"lt" => array(3,"var","symb","symb"),
		"gt" => array(3,"var","symb","symb"),
		"eq" => array(3,"var","symb","symb"),
		"and" => array(3,"var","symb","symb"),
		"or" => array(3,"var","symb","symb"),
		"not" => array(3,"var","symb","symb"),
		"int2char" => array(2,"var","symb"),
		"stri2int" => array(3,"var","symb","symb"),
		"read" => array(2,"var","type"),
		"write" => array(1,"symb"),
		"concat" => array(3,"var","symb","symb"),
		"strlen" => array(2,"var","symb"),
		"getchar" => array(3,"var","symb","symb"),
		"setchar" => array(3,"var","symb","symb"),
		"type" => array(2,"var","symb"),
		"label" => array(1,"label"),
		"jump" => array(1,"label"),
		"jumpifeq" => array(3,"label","symb","symb"),
		"jumpifneq" => array(3,"label","symb","symb"),
		"exit" => array(1,"symb"),
		"dprint" => array(1,"symb"),
		"break" => 0,
	);

	//creating new instance of class Instruction
	$instruction = InstructionFactory::create();

	//split line by variable number of spaces or tabs
	$word_arr = preg_split('/\s+/', $line);

	$word_arr[0] = strtolower($word_arr[0]);
	$word_count = count($word_arr);

	if(array_key_exists($word_arr[0], $KeyWords)){

		//Check if count of parameters is ok, higher or lower than should be.
		$param_count = $KeyWords[$word_arr[0]][0];
		$check = ($word_count-1) - $param_count;
		switch($check){
			case 0:
				$instruction->ToFill($word_arr, $param_count);
				$err_code = 0;
				break;
			case ($check > 0):
				if(strpos($word_arr[$param_count+1],"#") !== false){
					$instruction->ToFill($word_arr, $param_count);
					$err_code = 0;
				}
				else
				{
						fwrite(STDERR, "Wrong parameter(s) on ".$num_line." line.\n");
						$err_code = 22;
				}
				break;
				case ($check < 0):
				fwrite(STDERR, "Wrong count of parameters on ".$num_line." line.\n");
				$err_code = 23;
				break;
		}

		//XML Instruction
		if($err_code == 0){
			$xml_instruction = $xml->createElement("instruction");
			$xml_instruction->setAttribute("order", $num_line-1);
			$xml_instruction->setAttribute("opcode", $instruction->value);
			$program->appendChild($xml_instruction);

			for($i = 1; $i <= $param_count; $i++){
				$arg_desc = $instruction->CheckSyntax($KeyWords[$word_arr[0]][$i], $instruction->args[$i-1]);
				if(count($arg_desc)== 0){
					fwrite(STDERR, "Wrong parameters on ".$num_line." line.\n");
					return 22;
				}

				switch ($i) {
					case 1:
					//xml 1st parameter
					if($KeyWords[$word_arr[0]][$i] === "var" || $arg_desc[1] === "LF" || $arg_desc[1] === "GF" ||
						$arg_desc[1] === "TF"){
						$arg1 = $xml->createElement("arg1",$arg_desc[0]);
						$arg1->setAttribute("type", "var");
					}
					elseif($KeyWords[$word_arr[0]][$i] === "nil"){
						$arg1 = $xml->createElement("arg1",$arg_desc[2]);
						$arg1->setAttribute("type", "nil");
					}
					elseif($KeyWords[$word_arr[0]][$i] === "label"){
						$arg1 = $xml->createElement("arg1",$arg_desc[1]);
						$arg1->setAttribute("type", "label");
					}
					elseif($KeyWords[$word_arr[0]][$i] === "type"){
						$arg1 = $xml->createElement("arg1",$arg_desc[1]);
						$arg1->setAttribute("type", "type");
					}
					else{
						Replace($arg_desc[2]);
						$arg1 = $xml->createElement("arg1",$arg_desc[2]);
						$arg1->setAttribute("type",$arg_desc[1]);
					}
						$xml_instruction->appendChild($arg1);
						break;
					case 2:
						//xml 2nd parameter
						if($KeyWords[$word_arr[0]][$i] === "var" || $arg_desc[1] === "LF" || $arg_desc[1] === "GF" ||
							$arg_desc[1] === "TF"){
							$arg2 = $xml->createElement("arg2",$arg_desc[0]);
							$arg2->setAttribute("type", "var");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "nil"){
							$arg2 = $xml->createElement("arg2",$arg_desc[2]);
							$arg2->setAttribute("type", "nil");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "label"){
							$arg2 = $xml->createElement("arg2",$arg_desc[1]);
							$arg2->setAttribute("type", "label");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "type"){
							$arg2 = $xml->createElement("arg2",$arg_desc[1]);
							$arg2->setAttribute("type", "type");
						}
						else{
							Replace($arg_desc[2]);
							$arg2 = $xml->createElement("arg2",$arg_desc[2]);
							$arg2->setAttribute("type",$arg_desc[1]);
						}
						$xml_instruction->appendChild($arg2);
						break;
					case 3:
						//xml 3rd parameter
						if($KeyWords[$word_arr[0]][$i] === "var" || $arg_desc[1] === "LF" || $arg_desc[1] === "GF" ||
							$arg_desc[1] === "TF"){
							$arg3 = $xml->createElement("arg3",$arg_desc[0]);
							$arg3->setAttribute("type", "var");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "nil"){
							$arg3 = $xml->createElement("arg3",$arg_desc[2]);
							$arg3->setAttribute("type", "nil");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "label"){
							$arg3 = $xml->createElement("arg3",$arg_desc[1]);
							$arg3->setAttribute("type", "label");
						}
						elseif($KeyWords[$word_arr[0]][$i] === "type"){
							$arg3 = $xml->createElement("arg3",$arg_desc[1]);
							$arg3->setAttribute("type", "type");
						}
						else{
							Replace($arg_desc[2]);
							$arg3 = $xml->createElement("arg3",$arg_desc[2]);
							$arg3->setAttribute("type",$arg_desc[1]);
						}
						$xml_instruction->appendChild($arg3);
						break;
				}
			}



		}
	}
	//Comments
	elseif($word_arr[0][0] === "#"){
		$num_line = $num_line - 1;
		$err_code = 0;
	}
	else{
		fwrite(STDERR, "Wrong opcode on ".$num_line." line.\n");
		$err_code = 22;
	}

	return $err_code;
}

/**************************************/

//Main Function

if($argc < 2){
	$num_line = 0;
	$code = 0;
	$xml = "";
	$program = "";

	while($line = fgets(STDIN)){
		$line = trim($line);
		//check if the line is not empty
		if(strlen($line) > 1)
		{
			//Correct header ".IPPcode19" format checking
			if(($num_line) == 0){
				preg_match('/^(.ippcode19)(\s*$|\s+(?=#\w*))/', strtolower($line), $output_array);
				if($output_array != []){
					$language = "IPPcode19";
					//Creating XML form.
					$xml = new DomDocument("1.0","UTF-8");
					$xml->formatOutput = true;

					$program = $xml->createElement("program");
					$program->setAttribute("language",$language);

					$xml->appendChild($program);

					$num_line++;
				}
				else{
					fwrite(STDERR, "Wrong header\n");
					//Fixed
					exit(21);
				}
			}
			elseif(($num_line) == 0 && strtolower($line) !== ".ippcode19"){
				fwrite(STDERR, "Wrong header\n");
				//Fixed
				exit(21);
			}

			else{
				$num_line++;
				if(($code = Parse($line, $num_line, $xml, $program))!= 0){
					//Fixed
					exit($code);
				}
			}

		}
		else{
			continue;
		}

	}

}elseif($argc == 2 && $argv[1] == "--help"){
	echo("Napoveda ke skriptu Parse.php \n
Skript typu filtr nacte ze standardniho vstupu zdrojovy kod v IPPcode19,
zkontroluje lexikalni a syntaktickou spravnost kodu a vypise na standardni
vystup XML reprezentaci programu dle specifikace. \n
Chybove vystupy: \n
21 - chybna nebo chybejici hlavicka ve zdrojovem kodu zapsanem v IPPcode19 \n
22 - neznamy nebo chybny operacni kod ve zdrojovem kodu zapsanem v IPPcode19 \n}
23 - jina lexikalni nebo syntakticka chyba zdrojoveho kodu zapsaneho v IPPcode19.\n");
	return 0;
}
else {
	//Wrong parameters
	fwrite(STDERR, "Wrong input parameters.\n");
	//Fixed
	exit(10);
}

//XML output
	echo $xml->saveXML();


return 0;

//End of Main

?>
