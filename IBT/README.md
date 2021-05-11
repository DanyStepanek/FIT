
Physiological Data to Analyze and Improve the User Experience
-------------------------------------------------------------
Author: Daniel Štěpánek (xstepa61@stud.fit.vutbr.cz) \
Supervisor: Ing. Zdeněk Materna, Ph.D., UPGM FIT VUT \
Reviewer: Ing. Beran Vítězslav, Ph.D., UPGM FIT VUT

Date: 12.5.2021 \
BUT, Faculty of information technology

Specification:
---------------
1. Proveďte rešerši existujících řešení využívajících měření fyziologických dat (například variabilita srdečního tepu) pro účely detekce stresu, únavy, predikce UX metrik apod. 
2. Seznamte se se zařízeními pro měření fyziologických dat, zejména s Empatica E4. 
3. Na základě rešerše vyberte vhodné metriky / typy událostí, které by bylo možné za pomocí fyziologických dat odhadovat / detekovat. 
4. Navrhněte experiment pro získání vhodné datové sady. 
5. Proveďte navržený experiment a získanou datovou sadu anotujte. 
6. Diskutujte dosažené výsledky, kvalitu získaných dat, možná vylepšení a rozšíření. 
7. Vytvořte stručný plakát nebo video prezentující vaši bakalářskou práci, její cíle a výsledky. 

Hierarchy:
----------
  latex/ - LaTeX source code \
  src/ - scripts \
  data/ - data obtained in the experiment \
  plakat.pdf - thesis poster 


How to run: 
------------
For session with participant run: './src/session.py'. \
For data processing + statistics run: './src/processing_nk.py'. 

Implementation info:
--------------------
Implementation language: Python 3.8.5 \
Libraries: Pandas, NeuroKit2, matplotlib, numpy, seaborn, scipy, scikit-learn (./src/requirements.txt) \
To install libraries run: './src/requirements.sh' 

For more info about scripts see: './src/README.md' 
