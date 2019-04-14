<?php
# IPP test script for parse.php, interpret.py
# @author Daniel Stepanek xstepa61@stud.fit.vutbr.cz

//Error Codes
define("ERROR_PARAM",10);
define("ERROR_INPUT",11);
define("ERROR_OUTPUT",12);
define("ERROR_INTERNAL",99);

//Default
$parser = "./parse.php";
$interpret = "./interpret.py";


class Files{

  public $name;

  function __construct($file_name){
    $this->name = strstr($file_name, ".src", true);

    if(!file_exists("$this->name.in")){
      $file = fopen("$this->name.in", 'w+');
      fclose($file);
    }

    if(!file_exists("$this->name.out")){
      $file = fopen("$this->name.out", 'w+');
      fclose($file);
    }

    if(!file_exists("$this->name.rc")){
      $file = fopen("$this->name.rc", 'w+');
      fwrite($file,'0');
      fclose($file);
    }
    return;
  }

}

class Search{
  var $path;
  var $source;
  var $input_file;
  var $ref_out;
  var $out;

}
class NonRecursiveSearch extends Search{

  public function FindFiles($directory){
    $this->source = glob("$directory/*.src");

    foreach($this->source as $input_f){
      $files = new Files($input_f);

      $this->path = $directory;
      $this->input_file = $files->name.".in";
      $this->ref_out = $files->name.".rc";
      $this->out = $files->name.".out";
    }

  }

}

class RecursiveSearch extends Search{

  public function FindFiles($directory){
    $rec_path = new RecursiveDirectoryIterator($directory);
    $this->source = [];

    foreach(new RecursiveIteratorIterator($rec_path) as $input_f){
      $output_array = [];
      preg_match('/(.*.src)/', $input_f, $output_array);
      if($output_array != []){
        array_push($this->source, $output_array[0]);
        $files = new Files($output_array[0]);
        $this->path = $directory;
        $this->input_file = $files->name."in";
        $this->ref_out = $files->name.".rc";
        $this->out = $files->name.".out";
      }


    }
  }

}

class Test{

  static $test_counter;
  static $testPassed;
  static $testFailed;
  var $parse_result;
  var $interpret_result;

  function __construct(){
    $this->parse_result = 0;
    $this->interpret_result = 0;
  }

  public function TestParse($parser, $file, $out){
    exec("php7.3 $parser < $file.src > $file.par", $out, $this->parse_result);
    exec("echo $? > $file.parrc");
  return;
  }

  public function TestInterpret($interpret, $file, $out, $mode){

    switch($mode){
      case 0:
        exec("python3.6 $interpret --source=$file.par < $file.in > $file.int", $out, $interpret_result);
        exec("echo $? > $file.intrc");
      break;

      case 2:
        exec("python3.6 $interpret --source=$file.src < $file.in > $file.int", $out, $interpret_result);
        exec("echo $? > $file.intrc");

      break;

    }
  }

  public function CheckResult($file, $mode){
    $temp = "";

    switch($mode){
      //Both
      case 0:
        exec("diff -q \"$file.rc\" \"$file.intrc\"", $temp, $test);
        exec("diff -q \"$file.out\" \"$file.int\"", $temp, $out);
      //  echo ("diff both: ".$test);
        if($test == 0 & $out == 0){
          echo "<br><font size=\"2\" color=\"green\">Test Passed</font><br>";
          Test::$testPassed++;
        }
        else{
          echo "<br><font size=\"2\" color=\"red\">Test Failed</font><br>";
          Test::$testFailed++;
        }
        break;
      //Parse-only
      case 1:
        exec("diff -q \"$file.rc\" \"$file.parrc\"", $temp, $test);
        exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar <$path.out> <$path.temp> diffs.xml  /D /pub/courses/ipp/jexamxml/options NAVRATOVA_HODNOTA='$?'");
        //  echo ("diff parse: ".$test);
        if($test == 0){
          echo "<br><font size=\"2\" color=\"green\">Test Passed</font><br>";
          Test::$testPassed++;
        }
        else{
          echo "<br><font size=\"2\" color=\"red\">Test Failed</font><br>";
          Test::$testFailed++;
        }
        break;
      //Int-only
      case 2:
        exec("diff -q \"$file.rc\" \"$file.intrc\"", $temp, $test);
        exec("diff -q \"$file.out\" \"$file.int\"", $temp, $out);
      //  echo ("diff int: ".$test);
        if($test == 0 | $out == 0){
          echo "<br><font size=\"2\" color=\"green\">Test Passed</font><br>";
          Test::$testPassed++;
        }
        else{
          echo "<br><font size=\"2\" color=\"red\">Test Failed</font><br>";
          Test::$testFailed++;
        }
        break;
    }


  }

}


  $parameters = getopt("",array("help","directory::","recursive","parse-script::","int-script::","parse-only","int-only"));

  $p_script = false;
  $i_script = false;
  $p_only = false;
  $i_only = false;
  $recursive = false;


  if(array_key_exists("help", $parameters)){
    echo "Napoveda pro skript test.php\n\n";
    echo "--help - zobrazi napovedu\n";
    echo "--direcotry=path - hledani testu v tomto adresari <path>, implicitne aktualni adresar\n";
    echo "--recursive - rekurzivni prochazeni podadresaru\n";
    echo "--parse-script=file - parse.php pro testovani, implicitne v aktualnim adresari\n";
    echo "--int-script=file - interpret.py pro testovani, implicitne v aktualnim adresari\n";
    echo "--parse-only - testovani pouze parse.php, nelze kombinovat s --int-only\n";
    echo "--int-only - testovani pouze interpret.py, nelze kombinovat s --parse-only\n";
  }
  if(array_key_exists("directory", $parameters)){

    $directory = $parameters["directory"];
  }
  else{
    $directory = getcwd();
  }

  if(array_key_exists("recursive", $parameters)){
    $recursive = true;
    $searching = new RecursiveSearch();
  }
  else{
    $searching = new NonRecursiveSearch();
  }

  if(array_key_exists("parse-script", $parameters)){

    $parser = $parameters["parse-script"];
    $p_script = true;
  }

  if(array_key_exists("int-script", $parameters)){

    $interpet = $parameters["int-script"];
    $i_script = true;
  }

  if(array_key_exists("parse-only", $parameters)){
    $p_only = true;
  }

  if(array_key_exists("int-only", $parameters)){
    $i_only = true;
  }

  if($p_only && $i_script || $i_only && $p_script || $p_only && $i_only){
    fwrite(STDERR, "Invalid parameters\n");
    return ERROR_PARAM;

  }
  echo "<!DOCTYPE HTML>";
  echo "<html>";
  echo "<head>";
  echo "<meta charset=\"utf-8\">";
  echo "<meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\">";
  echo "<title>IPP project</title>";
  echo "</head>";
  echo "<body>";
  echo "<font size=\"3\" color=\"blue\">IPP project -- test.php -- Daniel Stepanek xstepa61@stud.fit.vutbr.cz</font><br>";

  $test_counter = 0;
  $testPassed = 0;
  $testFailed = 0;

  $searching->FindFiles($directory);

  //pro kazdy testovaci soubor vytvor novy test a podle parametru proved testy a vygeneruj html kod
  //vcetne poctu uspesnych a neuspesnych testu

  foreach($searching->source as $file){

    $result = 0;
    $file = strstr($file, ".src", true);
    $mode = 0;


    $testPassed = 0;
    $testFailed = 0;
    $out = 0;

    Test::$test_counter++;

    echo "<br><br><br><font size=\"2\" color=\"black\">Test #" . Test::$test_counter . " (Path: " . $directory . "/" . $file . ")</font><br>";

    if($p_only){
      $mode = 1;
      Test::TestParse($parser, $file, $searching->out);
      Test::CheckResult($file, $mode);
    }
    else if($i_only){
      $mode = 2;
      Test::TestInterpret($interpret, $file, $searching->out, $mode);
      Test::CheckResult($file, $mode);
    }
    else{
      Test::TestParse($parser, $file, $searching->out);
      Test::TestInterpret($interpret, $file, $searching->out, $mode);
      Test::CheckResult($file, $mode);
    }




    //Delete all temp files
    if(file_exists("$file.parrc")){
      unlink("$file.parrc");
    }
    if(file_exists("$file.par")){
      unlink("$file.par");
    }
    if(file_exists("$file.intrc")){
      unlink("$file.intrc");
    }
    if(file_exists("$file.int")){
      unlink("$file.int");
    }

  }





//  generovani html kodu, pocet uspesnych a neuspesnych testu, pripadne nazev testovaneho souboru atd..


  echo "<br><br><br>Summary: <br>------------<br>";

  echo "<font size=\"2\" color=\"black\">Tests total: " . Test::$test_counter . "</font><br>";
  echo "<font size=\"2\" color=\"black\">Tests passed: " . Test::$testPassed . "</font><br>";
  echo "<font size=\"2\" color=\"black\">Tests failed: " . Test::$testFailed . "</font><br>";

  echo "</body>";
  echo "</html>";


 ?>
