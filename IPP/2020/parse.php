<?php

/* IPP projekt 1
 * @author Daniel Stepanek xstepa61@stud.fit.vutbr.cz
 */

ini_set('display_errors', 'stderr');

//rozsireni -->
class StatP{
  public $is_stats;
  public $is_lines;
  public $is_comments;
  public $is_labels;
  public $is_jumps;
  public $file;

  private $lines;
  private $comments;
  private $labels;
  private $labels_array;
  private $jumps;

  public function set_lines(){
    $this->lines = 0;
  }
  public function set_comments(){
    $this->comments = 0;
  }
  public function set_labels(){
    $this->labels_array = array();
    $this->labels = 0;
  }
  public function set_jumps(){
    $this->jumps = 0;
  }

  public function add_line(){
    $this->lines += 1;
  }
  public function add_comment(){
    $this->comments += 1;
  }
  public function add_label($new_label){
    $is_new = true;
    foreach($this->labels_array as $l){
      if($l === $new_label){
        $is_new = false;
      }
    }
    if($is_new){
      $this->labels_array[$this->labels] = $new_label;
      $this->labels += 1;
    }

  }
  public function add_jump(){
    $this->jumps += 1;
  }

  public function get_lines(){
    return $this->lines;
  }
  public function get_comments(){
    return $this->comments;
  }
  public function get_labels(){
    return $this->labels;
  }
  public function get_jumps(){
    return $this->jumps;
  }

}
// <-- rozsireni

class Code{
  public static $Instructions_pattern = array(
    "move" => array(2,"var","symb"),
    "createframe" => array(0),
    "pushframe" => array(0),
    "popframe" => array(0),
    "defvar" => array(1,"var"),
    "call" => array(1,"label"),
    "return" => array(0),
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
    "not" => array(2,"var","symb"),
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
    "break" => array(0),
  );
}

class Parser{

  private $xml_instruction;
  private $word_arr;

  public function Instruction($line, $num_line, $xml, $program, $statp){
    $this->xml_instruction = $xml->createElement("instruction");
    $this->xml_instruction->setAttribute("order", $num_line);
    $program->appendChild($this->xml_instruction);

    //split line by variable number of spaces or tabs
    $this->word_arr = preg_split('/\s+/', $line);

    if(array_key_exists(strtolower($this->word_arr[0]), Code::$Instructions_pattern)){
      $this->xml_instruction->setAttribute("opcode", strtoupper($this->word_arr[0]));
      if($statp != null){
        if($statp->is_stats){
          switch(strtolower($this->word_arr[0])){
            case "jump":
              $statp->add_jump();
              break;
            case "jumpifeq":
              $statp->add_jump();
              break;
            case "jumpifneq":
              $statp->add_jump();
              break;
            case "call":
              $statp->add_jump();
              break;
            default:
              break;
          }
        }
      }
      $this->Arguments($xml, $statp);
      return 0;
    }
    else{
      exit(22);
    }
  }

  private function Arguments($xml, $statp){
    $kw_index = strtolower($this->word_arr[0]);
    $arg_count = Code::$Instructions_pattern[$kw_index][0];

    //count of parameters is lower than expected.
    if($arg_count > count($this->word_arr) - 1){
      exit(23);
    }
    //count of parameters is higher than expected
    //must check if it is comment (ok) or parameter (error).
    else if($arg_count < count($this->word_arr) - 1){
      $output_arr = [];
      preg_match('/\#.*/', $this->word_arr[$arg_count + 1], $output_arr);
      if($output_arr == []){
        preg_match('/.*\#.*/', $this->word_arr[$arg_count], $output_arr);
        if($output_arr == []){
          exit(23);
        }
        else{
          $this->word_arr[$arg_count] = preg_replace('/\#.*/', '', $this->word_arr[$arg_count]);
        }
      }
      if($statp != null){
        if($statp->is_stats) { $statp->add_comment(); }
      }
    }
    //cutting the comment after parameter without whitespace between them.
    else{
      $output_arr = [];
      preg_match('/.*\#.*/', $this->word_arr[$arg_count], $output_arr);
      if($output_arr != []){
        if($statp != null){
          if($statp->is_stats) { $statp->add_comment(); }
        }
      }
      $this->word_arr[$arg_count] = preg_replace('/\#.*/', '', $this->word_arr[$arg_count]);
    }

    for($i = 1; $i <= $arg_count; $i++){
      $type = "";
      $output = $this->Syn_Lex_check($kw_index, $i, $type, $statp);

      if($output == []){
        exit(23);
      }
      else{
        //Replace special characters in string.
        if($output[1] === "string"){
          if(isset($output[2])){
            $output[2] = $this->Replace($output[2]);
          }
        }

        if($type == "var"){
          $this->word_arr[$i] = $this->Replace($this->word_arr[$i]);
          $arg = $xml->createElement("arg$i", $this->word_arr[$i]);
        }
        else if($type == "type"){
          $arg = $xml->createElement("arg$i", $output[1]);
        }
        else if($type == "label"){
          $arg = $xml->createElement("arg$i", $output[1]);
        }
        else{
          $arg = $xml->createElement("arg$i", $output[2]);
        }

        $arg->setAttribute("type", $type);
        $this->xml_instruction->appendChild($arg);
      }
    }

    return;
  }

  private function Syn_Lex_check($kw_index, $i, &$type, $statp){
    $output_arr = [];

    switch(Code::$Instructions_pattern[$kw_index][$i]){
      case "var":
			//frame@special_characters or alphanumeric characters
				preg_match('/(TF|LF|GF)@([\-\_\$\&\%\*\!\?[a-zA-Z]+[\-\_\$\&\%\*\!\?\w]*)$/', $this->word_arr[$i], $output_arr);
        $type = "var";
				break;

			case "symb":
			//could be var
				preg_match('/(TF|LF|GF)@([\-\_\$\&\%\*\!\?[a-zA-Z]+[\-\_\$\&\%\*\!\?\w]*)$/', $this->word_arr[$i], $output_arr);
        $type = "var";
				if($output_arr == []){
					preg_match('/(int)@([+-]?\d+)$/', $this->word_arr[$i], $output_arr);
          $type = "int";
				}
				if($output_arr == []){
					preg_match('/(bool)@(true|false)$/', $this->word_arr[$i], $output_arr);
          $type = "bool";
        }
				if($output_arr == []){
					//string@special_characters or alphanumeric characters or special escape sequences \[0-9][0-9][0-9]
					preg_match('/(string)@((\w*[\<\>\&\'\"\/\-\§\,\;\)\(\=]*[áéěíýóúůžščřďťňÁÉĚÍÝÓÚŮŽŠČŘĎŤŇ]*(\\\[0-9][0-9][0-9])*\w*)*)$/u', $this->word_arr[$i], $output_arr);
          $type = "string";
        }
				if($output_arr == []){
					preg_match('/(nil)@(nil)$/', $this->word_arr[$i], $output_arr);
          $type = "nil";
        }
				break;

			case "label":
				preg_match('/^([\-\_\$\&\%\*\!\?[a-zA-Z]+[^@][\-\_\$\&\%\*\!\?[a-zA-Z]*)$/', $this->word_arr[$i], $output_arr);
        if(strtolower($this->word_arr[0]) === "label"){
          if($output_arr != []){
            if($statp != null){
              if($statp->is_stats) { $statp->add_label($this->word_arr[$i]); }
            }
          }
        }
        $type = "label";
				break;

			case "type":
				preg_match('/(int|string|bool)$/', $this->word_arr[$i], $output_arr);
        $type = "type";
				break;
		}

    return $output_arr;
  }

  //Replace special characters to textformat.
  private function Replace($string){
  	$patterns = [];
    $replacements = [];

  	$patterns[0] = '/\&/';
    $patterns[1] = '/\>/';
    $patterns[2] = '/\</';
    $patterns[3] = '/\'/';
    $patterns[4] = '/\"/';

    $replacements[0] = '&amp;';
    $replacements[1] = '&gt;';
    $replacements[2] = '&lt;';
  	$replacements[3] = '&apos;';
  	$replacements[4] = '&quot;';

    $string = preg_replace($patterns, $replacements, $string);

    return $string;
  }
}

function main($statp){
  $num_line = 0;
  $xml = "";
  $program = "";
  $parser = new Parser();

  while($line = fgets(STDIN)){
    //strip whitespaces(or other characters) from the beginning and end of a string
    $line = trim($line);
    //check if the line is not empty
    if(strlen($line) >= 1){
      //Correct header ".IPPcode20" format checking
      if(($num_line) == 0){
        if($line[0] === "#"){
          if($statp != null){
            if($statp->is_stats) { $statp->add_comment(); }
          }
          $line = fgets(STDIN);
        }

        preg_match('/^(?i)(.IPPcode20)(\s*$|\s*(?=#\w*))/', $line, $output_arr);
        if($output_arr != []){
          $language = "IPPcode20";
          //check comment after header
          preg_match('/.*\#.*/', $line, $output_arr);
          if($output_arr != []){
            if($statp != null){
              if($statp->is_stats) { $statp->add_comment(); }
            }
          }

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
          exit(21);
        }
      }
      elseif(($num_line) == 0 && strtolower($line) !== ".ippcode20"){
        fwrite(STDERR, "Wrong header\n");
        exit(21);
      }
      elseif($line[0] === "#"){
        if($statp != null){
          if($statp->is_stats) { $statp->add_comment(); }
        }
        continue;
      }
      else{
        $parser->Instruction($line, $num_line, $xml, $program, $statp);
        if($statp != null){
          if($statp->is_stats) { $statp->add_line(); }
        }
        $num_line++;
      }
    }
    else{
      continue;
    }
  }

  //XML output
  if($num_line > 0){
    echo $xml->saveXML();
  }

  return 0;
}

//Parameters parsing
if($argc < 2){
  $statp = null;
  main($statp);
  exit(0);
}
else if($argc >= 2){
  $longopts = array(
    "stats:",
    "loc",
    "comments",
    "labels",
    "jumps",
    "help"
  );
  $parameters = getopt("", $longopts);
  if(array_key_exists("help", $parameters)){
    if($argc == 2){
      echo("Napoveda ke skriptu parse.php \n
        Skript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPPcode20,
      zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní
      výstup XML reprezentaci programu. \n

    Ukazka spusteni: \n
      php7.4 parse.php < file.src \n

    Chybove vystupy: \n
      21 - chybna nebo chybejici hlavicka ve zdrojovem kodu zapsanem v IPPcode20. \n
      22 - neznamy nebo chybny operacni kod ve zdrojovem kodu zapsanem v IPPcode20. \n
      23 - jina lexikalni nebo syntakticka chyba zdrojoveho kodu zapsaneho v IPPcode20.\n");
      exit(0);
    }
    else{
      exit(10);
    }
  }

  $statp = new StatP();
  $opt_array = array();
  if(array_key_exists("stats", $parameters)){
    $statp->is_stats = true;
  }

  if($statp->is_stats){
    if(array_key_exists("loc", $parameters)){
      $statp->is_lines = true;
      $statp->set_lines();
    }

    if(array_key_exists("comments", $parameters)){
      $statp->is_comments = true;
      $statp->set_comments();
    }

    if(array_key_exists("labels", $parameters)){
      $statp->is_labels = true;
      $statp->set_labels();
    }

    if(array_key_exists("jumps", $parameters)){
      $statp->is_jumps = true;
      $statp->set_jumps();
    }
  }
  else if(!$statp->is_stats && $argc > 2){
    exit(10);
  }

  main($statp);
//writing to file
  $statp->file = fopen($parameters["stats"], "w");
  if($statp->file === false){
    exit(12);
  }
  foreach($argv as $opt){
    switch($opt){
      case "--loc":
        fwrite($statp->file, $statp->get_lines());
        fwrite($statp->file, "\n");
        break;
      case "--comments":
        fwrite($statp->file, $statp->get_comments());
        fwrite($statp->file, "\n");
        break;
      case "--labels":
        fwrite($statp->file, $statp->get_labels());
        fwrite($statp->file, "\n");
        break;
      case "--jumps":
        fwrite($statp->file, $statp->get_jumps());
        fwrite($statp->file, "\n");
        break;
    }
  }
  fclose($statp->file);
  exit(0);
}
else {
	//Wrong parameters
	fwrite(STDERR, "Wrong input parameters.\n");
	exit(10);
}

exit(0);

?>
