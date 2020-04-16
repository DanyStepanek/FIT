<?php
/* IPP test file
 * @author: Daniel Stepanek
 * @email: xstepa61@stud.fit.vutbr.cz
 */

ini_set('display_errors', 'stderr');

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
       $file = fopen("$this->name.rc", 'w');
       fwrite($file,'0');
       fclose($file);
     }
     return;
   }

   public function clear_temp_files($file){
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


 }

 abstract class Search{
   protected $path;
   public $source;
   protected $input_file;
   protected $ref_out;
   protected $out;

   public function set_path(){
     $this->path = $path;
   }
 }

 class NonRecursiveSearch extends Search{

   public function search($directory){
     if(!file_exists($directory)){
       exit(11);
     }
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

   public function search($directory){
     if(!file_exists($directory)){
       exit(11);
     }
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

abstract class Test{

  protected $path;
  protected $result;
  protected $jexamxml;
  protected $test_count;
  protected $passed_count;
  protected $failed_count;

  public function set_path($path, $jexamxml){
    $this->path = $path;
    $this->jexamxml = $jexamxml;
  }

  public function set_counters(){
    $this->test_count = 0;
    $this->passed_count = 0;
    $this->failed_count = 0;
  }

  public function get_counters(){
    return array($this->test_count, $this->passed_count, $this->failed_count);
  }

  abstract public function exec($searching, $directory, $html);
  abstract protected function check($path, $file, $html);
}

class ParserTest extends Test{

  public function exec($searching, $directory, $html){
    $searching->search($directory);
    //for each test file create new test and compare results. After that generate HTML code.
    foreach($searching->source as $file){
      $path = $file;
      $file = strstr($file, ".src", true);

      exec("php7.4 $this->path < $file.src > $file.par", $out, $this->result);

      $fp = fopen("$file.parrc", "w");
      fwrite($fp, $this->result);
      fclose($fp);

      $this->check($path, $file, $html);
      Files::clear_temp_files($file);
    }
  }

  protected function check($path, $file, $html){
    $temp = "";
    $test = 0;
    $out = 0;
    $this->test_count += 1;

    exec("diff -q -b $file.rc $file.parrc", $temp, $test);
    if($this->result == 0){
      exec("java -jar $this->jexamxml $file.out $file.par diffs.xml /D /pub/courses/ipp/jexamxml/options
            NAVRATOVA_HODNOTA='$?'", $temp, $out);
    }

    if($test == 0 && $out == 0){
      $html->testPassed($path);
      $this->passed_count += 1;
    }
    else{
      $html->testFailed($path);
      $this->failed_count += 1;
    }
  }
}

class InterpretTest extends Test{

  public function exec($searching, $directory, $html){
    $searching->search($directory);
    //for each test file create new test and compare results. After that generate HTML code.
    foreach($searching->source as $file){
      $path = $file;
      $file = strstr($file, ".src", true);

      exec("python3.8 $this->path --source=$file.src < $file.in > $file.int", $out, $this->result);

      $fp = fopen("$file.intrc", "w");
      fwrite($fp, $this->result);
      fclose($fp);

      $this->check($path, $file, $html);
      Files::clear_temp_files($file);
    }
  }

  protected function check($path, $file, $html){
    $temp = "";
    $test = 0;
    $out = 0;
    $this->test_count += 1;

    exec("diff -q -b $file.rc $file.intrc", $temp, $test);
    exec("diff -q $file.out $file.int", $temp, $out);

    if($test == 0 && $out == 0){
      $html->testPassed($path);
      $this->passed_count += 1;
    }
    else{
      $html->testFailed($path);
      $this->failed_count += 1;
    }
  }
}

class CompleteTest extends Test{

  private $parser;
  private $interpret;

  public function set_paths($parser, $interpret){
      $this->parser = $parser;
      $this->interpret = $interpret;
  }

  public function exec($searching, $directory, $html){
    $searching->search($directory);
  //for each test file create new test and compare results. After that generate HTML code.
    foreach($searching->source as $file){
      $path = $file;
      $file = strstr($file, ".src", true);

      exec("php7.4 $this->parser < $file.src > $file.par", $out, $this->result);

      if($this->result != 0){
        $fp = fopen("$file.intrc", "w");
        fwrite($fp, $this->result);
        fclose($fp);
      }
      else{
        $fp = fopen("$file.parrc", "w");
        fwrite($fp, $this->result);
        fclose($fp);

        exec("python3.8 $this->interpret --source=$file.par < $file.in > $file.int", $out, $this->result);

        $fp = fopen("$file.intrc", "w");
        fwrite($fp, $this->result);
        fclose($fp);
      }

      $this->check($path, $file, $html);
      Files::clear_temp_files($file);
    }
  }

  protected function check($path, $file, $html){
    $temp = "";
    $test = 0;
    $out = 0;
    $this->test_count += 1;

    exec("diff -q -b $file.rc $file.intrc", $temp, $test);
    if(file_exists("$file.int")){
      exec("diff -q $file.out $file.int", $temp, $out);
    }


    if($test == 0 && $out == 0){
      $html->testPassed($path);
      $this->passed_count += 1;
    }
    else{
      $html->testFailed($path);
      $this->failed_count += 1;
    }
  }
}

class Html{
  public function head(){
    echo "<!DOCTYPE HTML>";
    echo "<html>";
    echo "<head>";
    echo "<meta charset=\"utf-8\">";
    echo "<meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\">";
    echo "<title>IPP test script</title>";
    echo "
    <style>
    body {
      background-color:#111111;
    }
    h2 {
      color:#0066ff;
      text-shadow: 1px 1px 1px #ffffff
    }
    h4 {
      color:#0066ff;
      text-align: right;
    }
    #p_passed{
      font-size: 2;
      color: #00ff00;
    }
    #p_failed{
      font-size: 2;
      color: #ff0000;
    }
    #p_statistics{
      font-size: 2;
      color: #ffffff;
    }

    #p_summary{
      font-size: 2;
      color: #ffffff;
    }

    #p_path{
      font-size: 2;
      font-style: italic;
      color: #ffffff;
    }

    table, th, td {
      border: 1px solid white;
      border-collapse: collapse;
      padding-left: 10px;
      padding-right: 10px;
    }

    th {
      text-align: center;
    }

    div {
      padding: 20px;
    }
    </style>
    ";

    echo "</head>";
    echo "<body>";
    echo "<h2>IPP project</h2>";
    echo "<h4>Daniel Stepanek <address>xstepa61@stud.fit.vutbr.cz</address></h4>";
    echo "<hr><br>";
    echo "<div>";
    echo "<table>";
  }

  public function testPassed($path){
    echo "<tr>";
    echo "<th><p id=\"p_passed\">Test Passed</p></th>";
    echo "<th><p id=\"p_path\"><q>" . $path . "</q></p></th>";
    echo "</tr>";
  }

  public function testFailed($path){
    echo "<tr>";
    echo "<th><p id=\"p_failed\">Test Failed</p></th>";
    echo "<th><p id=\"p_path\"><q>" . $path . "</q></p></th>";
    echo "</tr>";
  }

  public function summary($test_count, $test_passed, $test_failed){
    echo "</table>";
    echo "</div>";
    echo "<div>";
    echo "<table>";
    echo "<th>";
    echo "<p id=\"p_summary\">Summary:</p>";
    echo "<p id=\"p_statistics\">Tests total:" . $test_count . "</p>";
    echo "<p id=\"p_statistics\">Tests passed:" . $test_passed . "</p>";
    echo "<p id=\"p_statistics\">Tests failed:" . $test_failed . "</p>";
    echo "</th>";
    echo "</table>";
    echo "</div>";
  }

  public function end(){
    echo "</body>";
    echo "</html>";
  }
}

function main($searching, $directory, $parser, $interpret, $jexamxml, $p_only, $i_only){
  $html = new Html();
  $test_count = 0;
  $test_passed = 0;
  $test_failed = 0;

  $html->head();

  if($p_only){
    if(!file_exists($parser)){
      exit(11);
    }
    $p_test = new ParserTest();
    $p_test->set_path($parser, $jexamxml);
    $p_test->set_counters();
    $p_test->exec($searching, $directory, $html);
    list($test_count, $test_passed, $test_failed) = $p_test->get_counters();
  }
  else if($i_only){
    if(!file_exists($interpret)){
      exit(11);
    }
    $i_test = new InterpretTest();
    $i_test->set_path($interpret, NULL);
    $i_test->set_counters();
    $i_test->exec($searching, $directory, $html);
    list($test_count, $test_passed, $test_failed) = $i_test->get_counters();
  }
  else{
    if(!file_exists($parser) || !file_exists($interpret)){
      exit(11);
    }
    $c_test = new CompleteTest();
    $c_test->set_paths($parser, $interpret);
    $c_test->set_counters();
    $c_test->exec($searching, $directory, $html);
    list($test_count, $test_passed, $test_failed) = $c_test->get_counters();
  }

  $html->summary($test_count, $test_passed, $test_failed);
  $html->end();
  return 0;
}

 $parameters = getopt("",array("help","directory::","recursive","parse-script::","int-script::","parse-only","int-only", "jexamxml::"));

 $p_script = false;
 $i_script = false;
 $p_only = false;
 $i_only = false;
 $recursive = false;

 $parameters_count = 0;

 $searching = NULL;
 $directory = NULL;
 $parser = NULL;
 $interpret = NULL;
 $jexamxml = NULL;

 if(array_key_exists("help", $parameters)){
   echo "Napoveda pro skript test.php\n\n";
   echo "--help - zobrazi napovedu\n";
   echo "--direcotry=path - hledani testu v tomto adresari <path>, implicitne aktualni adresar\n";
   echo "--recursive - rekurzivni prochazeni podadresaru\n";
   echo "--parse-script=file - parse.php pro testovani, implicitne v aktualnim adresari\n";
   echo "--int-script=file - interpret.py pro testovani, implicitne v aktualnim adresari\n";
   echo "--parse-only - testovani pouze parse.php, nelze kombinovat s --int-only\n";
   echo "--int-only - testovani pouze interpret.py, nelze kombinovat s --parse-only\n";
   echo "--jexamxml=file - soubor s JAR balickem s nastrojem A7Soft JExamXML,
          implicitne /pub/courses/ipp/jexamxml/jexamxml.jar na serveru Merlin.\n";
 }

 if(array_key_exists("directory", $parameters)){
   $parameters_count += 1;
   $directory = $parameters["directory"];
 }
 else{
   $directory = getcwd();
 }

if(array_key_exists("recursive", $parameters)){
  $recursive = true;
  $parameters_count += 1;
  $searching = new RecursiveSearch();
}
else{
  $searching = new NonRecursiveSearch();
}

 if(array_key_exists("parse-script", $parameters)){
   $parameters_count += 1;
   $parser = $parameters["parse-script"];
   $p_script = true;
 }
 else{
   $parser = "./parse.php";
 }

 if(array_key_exists("int-script", $parameters)){
   $parameters_count += 1;
   $interpret = $parameters["int-script"];
   $i_script = true;
 }
 else{
   $interpret = "./interpret.py";
 }

 if(array_key_exists("parse-only", $parameters)){
   $parameters_count += 1;
   $p_only = true;
 }

 if(array_key_exists("int-only", $parameters)){
   $parameters_count += 1;
   $i_only = true;
 }

 if(array_key_exists("jexamxml", $parameters)){
   $parameters_count += 1;
   $jexamxml = $parameters["jexamxml"];
   if(!$i_only)
    if(!file_exists($jexamxml)){
      exit(11);
    }
 }
 else{
   if(!$i_only){
     $jexamxml = "/pub/courses/ipp/jexamxml/jexamxml.jar";
     if(!file_exists($jexamxml)){
       exit(11);
     }
   }
 }

 if(($p_only && $i_script) || ($i_only && $p_script) || ($p_only && $i_only) || ($parameters_count < ($argc - 1))){
   fwrite(STDERR, "Invalid parameters\n");
   return 10;

 }

 if($i_only){
   $jexamxml = NULL;
 }

 main($searching, $directory, $parser, $interpret, $jexamxml, $p_only, $i_only);
 exit(0);

?>
