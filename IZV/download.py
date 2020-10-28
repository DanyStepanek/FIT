
import requests, os, zipfile, sys, csv, gzip, pickle, datetime
#from bs4 import BeautifulSoup
import numpy as np

import time
start_time = time.time()

class DataDownloader():
    """
    inicializátor - obsahuje volitelné parametry:
    ○url​ - ukazuje, z jaké adresy se data načítají. Defaultně bude nastavený navýše uvedenou URL.
    ○folder​ - říká, kam se mají dočasná data ukládat. Tato složka nemusí nazačátku existovat!
    ○cache_filename​ - jméno souboru ve specifikované složce, které říká, kam
    se soubor s již zpracovanými daty z funkce ​get_list​ bude ukládat a odkud
    se budou data brát pro další zpracování a nebylo nutné neustále stahovatdata přímo z webu.
     Složené závorky (formátovací řetězec) bude nahrazený
     tříznakovým kódem (viz tabulka níže) příslušného kraje. Pro jednoduchost
     podporujte pouze formát “pickle” s kompresí gzip.
    """
    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename
        self.parsed_regions = dict()
        self.region_code = {"PHA":"00",
                           "STC":"01",
                           "JHC":"02",
                           "PLK":"03",
                           "ULK":"04",
                           "HKK":"05",
                           "JHM":"06",
                           "MSK":"07",
                           "KVK":"19",
                           "LBK":"18",
                           "PAK":"17",
                           "OLK":"14",
                           "ZLK":"15",
                           "VYS":"16",
                          }
        self.header = ['p1',	'p36', 'p37', 'p2a', 'weekday(p2a)', 'p2b',	'p6', 'p7', 'p8',
        	       'p9', 'p10',	'p11', 'p12', 'p13a', 'p13b', 'p13c', 'p14', 'p15',
                   'p16', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p27',
                   'p28', 'p34', 'p35', 'p39', 'p44', 'p45a', 'p47', 'p48a', 'p49',
                   'p50a', 'p50b', 'p51', 'p52', 'p53', 'p55a', 'p57', 'p58', 'a', 'b',
                   'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'o', 'p', 'q', 'r',
                   's', 't', 'p5a', 'region']

        self.data_to_download = ['datagis2016.zip', 'datagis-rok-2017.zip',
                            'datagis-rok-2018.zip', 'datagis-rok-2019.zip',
                             'datagis-09-2020.zip']

        os.makedirs(folder, exist_ok=True)
        self.folder = os.path.abspath(folder)


    """
    funkce stáhne do datové složky ​folder​  všechny soubory s daty z adresy ​url
    """
    def download_data(self):
        """
        cookies = {
            's_pers': '%20c19%3Dsd%253Aproduct%253Ajournal%253Aarticle%7C1586696682765%3B%20v68%3D1586694878778%7C1586696682817%3B%20v8%3D1586694882868%7C1681302882868%3B%20v8_s%3DFirst%2520Visit%7C1586696682868%3B',
            'AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg': '-432600572%7CMCIDTS%7C18365%7CMCMID%7C43823912540983368122529753333098666222%7CMCAID%7CNONE%7CMCOPTOUT-1586702082s%7CNONE%7CvVersion%7C4.5.2',
            'amplitude_id_9f6c0bb8b82021496164c672a7dc98d6_edmvutbr.cz': 'eyJkZXZpY2VJZCI6IjFhNmY3ZDhmLWZlY2MtNGMyNS05MDVhLTYxMTgxYTBjYTQ5MlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU4NjY5NDgyNDUxNiwibGFzdEV2ZW50VGltZSI6MTU4NjY5NTEwMzQ5NSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6Miwic2VxdWVuY2VOdW1iZXIiOjJ9',
            'utag_main': 'v_id:01716e68a53a000b5594be750f7402073004206b00bd0$_sn:1$_ss:1$_st:1586697084027$ses_id:1586695284027%3Bexp-session$_pn:1%3Bexp-session$vapi_domain:vutbr.cz',
            'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg': '1687686476%7CMCIDTS%7C18365%7CMCMID%7C42217145750122169307859303432771442788%7CMCAID%7CNONE%7CMCOPTOUT-1586702484s%7CNONE%7CvVersion%7C3.0.0',
            }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.112 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'cs-CZ,cs;q=0.9',
            }

        response = requests.get(self.url, headers=headers, cookies=cookies)

        soup = BeautifulSoup(response.text, 'html.parser')
    #    soup.find_all('a', class_="btn btn-sm btn-primary")
        """


        for data in self.data_to_download:
            #download data from server
            url = "{}/data/{}".format(self.url, data)
            response = requests.get(url, stream=True)

            file_abs_path = "{}/{}".format(self.folder, data)

            #write zip file to disk
            with open(file_abs_path, 'wb') as fd:
                fd.write(response.content)


    #not used
    def region_to_code(self, region):
        region_code = {"PHA":"00",
                       "STC":"01",
                       "JHC":"02",
                       "PLK":"03",
                       "ULK":"04",
                       "HKK":"05",
                       "JHM":"06",
                       "MSK":"07",
                       "KVK":"19",
                       "LBK":"18",
                       "PAK":"17",
                       "OLK":"14",
                       "ZLK":"15",
                       "VYS":"16",
                      }
        if region in region_code.keys():
            return region_code[region]
        else:
            raise ValueError("Region not recognized!")


    """
    pokud nejsou data pro daný kraj stažená, stáhne je do datové složky ​folder​.
    Potéje pro daný region specifikovaný tříznakovým kódem (viz tabulka níže) ​vždy
    vyparsuje do následujícího formátu dvojice (​tuple​),
     kde první položka je seznam(​list​) řetězců a druhá položka bude seznam (​list​) NumPy polí,
      schematicky:tuple(list[str], list[np.ndarray])
     Seznam řetězců odpovídá názvům jednotlivých datových sloupců, NumPy polebudou obsahovat data.
     Platí, že délka obou seznamů je stejná, ​shape ​všechNumPy polí je stejný.  Při parsování
     přidejte nový sloupec “region”, který bude obsahovat tříznaký kód patřičného kraje,
      tj. odpovídá hodnotě ​region​. Pro každýsloupec zvolte ​vhodný datový typ​ (t.j.
     snažte se vyhnout textovým řetězcům,vyřešte desetinnou čárku atp.).
    """
    def retype_row_data(self, row):
        new_row = np.array([None] * len(row))
        for i in range(len(row)):
            if i in (3, 51, 52, 54, 58, 59, 62):
                new_row[i] = row[i]
            elif i in (47, 48, 49, 50):
                try:
                    new_row[i] = np.double(row[i])
                except:
                    new_row[i] = row[i]
            else:
                try:
                    new_row[i] = np.int_(row[i])
                except:
                    new_row[i] = row[i]

        return new_row

    def parse_region_data(self, region):
        #check if data are downloaded
        downloaded_zip_files = [f for f in os.listdir(self.folder) if f.endswith('.zip')]
        if set(downloaded_zip_files) != set(self.data_to_download):
            self.download_data()

        if region not in self.region_code.keys():
            raise ValueError("Region not recognized!")

        file = "{}.csv".format(self.region_code[region])

        parsed_data = [self.header, []]
        list_of_rows = []

        for zip_file in self.data_to_download:
            path = "{}/{}".format(self.folder, zip_file)
            #open zip and extract csv file with data of region
            with zipfile.ZipFile(path, 'r') as zf:
                zf.extract(file, self.folder)
            #open csv file and parse data
            with open('{}/{}'.format(self.folder, file), encoding = "ISO-8859-2", newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                if len(list_of_rows) == 0:
                    list_of_rows = [ self.retype_row_data(row + [region]) for row in reader ]
                else:
                    np.append(list_of_rows, [ self.retype_row_data(row + [region]) for row in reader ], axis=0)

            #delete extracted csv file
            os.remove("{}/{}".format(self.folder, file))

        parsed_data[1] = list( np.transpose(list_of_rows) )

        return parsed_data

    """
    Vrací zpracovaná data pro vybrané kraje (regiony).
    Argument ​regions ​specifikujeseznam (list) požadovaných krajů jejich třípísmennými kódy.
     Pokud seznam neníuveden (je použito None), zpracují se všechny kraje včetně Prahy.
    Výstupem funkceje dvojice ve stejném formátu,
     jako návratová hodnota funkce parse_region_data​.

     Pro každý kraj získá data s využitím funkce ​parse_region_data ​tak,
      že se budou výsledky uchovávat v paměti (v nějakém atributu instance třídy)
       a ukládat dopomocného cache souboru pomocí následujícího schématu:
       ○pokud už je výsledek načtený v paměti (tj. dostupný ve vámi zvolenématributu), vrátí tuto
        dočasnou kopii
       ○pokud není uložený v paměti, ale je již zpracovaný v cache souboru,
        taknačte výsledek z cache, uloží jej do atributu a vrátí.
       ○jinak se zavolá funkce ​parse_region_data, výsledek volání seuloží do cache,
        poté do paměti a výsledek vrátí
    """
    def get_list(self, regions=None):
        if regions == None:
            regions = self.region_code.keys()

        complete_data = [self.header, []]

        for region in regions:
            cache_file = self.cache_filename.format(region)
            #return data from memory
            if region in self.parsed_regions.keys():
                data = parsed_regions[region]
            #get data from cache
            elif cache_file in os.listdir(self.folder):
                #unpack gzip and load data
                with gzip.open('{}/{}'.format(self.folder, cache_file), 'rb') as cache:
                    p = pickle.Unpickler(cache)
                    data = p.load()
            else: #parse (download) data, store to cache and return them
                #create gzip with pickle data
                p_data = self.parse_region_data(region)
                data = p_data[1]
                self.parsed_regions[region] = data
                with gzip.open('{}/{}'.format(self.folder, cache_file), 'wb') as cache:
                    p = pickle.Pickler(cache)
                    p.fast = True
                    p.dump(data)

            #concatenate data of all regions
            if len(complete_data[1]) == 0:
                complete_data[1] = data
            else:
                np.append(complete_data[1], data)

        return complete_data


if __name__=="__main__":
    downloader = DataDownloader()
    downloader.get_list(['PHA','OLK', 'ZLK'])


print("--- %s seconds ---" % (time.time() - start_time))
