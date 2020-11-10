
import requests, os, zipfile, re, sys, csv, gzip, pickle, datetime
from bs4 import BeautifulSoup
import numpy as np

class DataDownloader():

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
        """
            header items description
            https://www.policie.cz/soubor/polozky-formulare-hlavicky-souboru-xlsx.aspx
        """
        self.header = ['p1', 'p36', 'p37', 'p2a', 'weekday(p2a)', 'p2b', 'p6', 'p7', 'p8',
        	       'p9', 'p10',	'p11', 'p12', 'p13a', 'p13b', 'p13c', 'p14', 'p15',
                   'p16', 'p17', 'p18', 'p19', 'p20', 'p21', 'p22', 'p23', 'p24', 'p27',
                   'p28', 'p34', 'p35', 'p39', 'p44', 'p45a', 'p47', 'p48a', 'p49',
                   'p50a', 'p50b', 'p51', 'p52', 'p53', 'p55a', 'p57', 'p58', 'a', 'b',
                   'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'o', 'p', 'q', 'r',
                   's', 't', 'p5a', 'region']

        self.data_to_download = []
        self.downloaded_zip_files = []

        os.makedirs(folder, exist_ok=True)
        self.folder = os.path.abspath(folder)

    """
    Find last zip files with data of each year
    """
    def find_data_to_download(self, response):

        soup = BeautifulSoup(response.text, 'html.parser')
        a_data = soup.find_all('a', class_="btn btn-sm btn-primary")
        if len(a_data) < 1:
            sys.stderr.write('Downloaded data are not valid.\n')
            exit(-1)

        for link in a_data:
            href = link.get('href')
            path =  re.match(r'data\/(datagis\d{4}.zip)', href)
            if path != None:
                self.data_to_download.append(path.group(1))
            else:
                path =  re.match(r'data\/(datagis-rok-\d{4}.zip)', href)
                if path != None:
                    self.data_to_download.append(path.group(1))

        last_data_of_actual_year = a_data[-1]
        href = last_data_of_actual_year.get('href')
        link = re.match(r'data\/(datagis-\d{2}-2020.zip)', href)
        if link != None:
            self.data_to_download.append(link.group(1))
        else:
            sys.stderr.write('Downloaded data are not valid.\n')
            exit(-1)



    def download_data(self):

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

        response = requests.get(self.url, headers=headers)
        self.find_data_to_download(response)

        for data in set(self.data_to_download) - set(self.downloaded_zip_files):
            #download data from server
            url = "{}/data/{}".format(self.url, data)
            response = requests.get(url, stream=True)

            file_abs_path = "{}/{}".format(self.folder, data)

            #write zip file to disk
            with open(file_abs_path, 'wb') as fd:
                fd.write(response.content)

            if data not in self.downloaded_zip_files:
                self.downloaded_zip_files.append(data)

    def retype_col_data(self, arr):
        dt = ['int', 'int', 'int', 'datetime64', 'int', 'int', 'int', 'int',
              'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int',
              'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int',
              'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int',
              'int', 'int', 'int', 'int', 'int', 'int', 'int', 'int',
              'int', 'int', 'int', 'int', 'int', 'float64', 'float64', 'float64',
              'float64', 'float64', 'float64', 'object', 'object', 'int', 'object',
              'object', 'object', 'float64', 'object', 'object', 'int', 'int', 'object',
              'int', 'object']

        new_arr = [None] * len(arr)

        for i in range(len(dt)):
            col_to_object = arr[i].astype('object')
            if dt[i] != 'object':
                col_to_object[col_to_object==''] = '-1'
                col_to_object[col_to_object=='XX'] = '-1'
                col_to_object[col_to_object=='A:'] = '-1'
                col_to_object[col_to_object=='B:'] = '-1'
                col_to_object[col_to_object=='D:'] = '-1'
                col_to_object[col_to_object=='E:'] = '-1'
                col_to_object[col_to_object=='F:'] = '-1'
                col_to_object[col_to_object=='G:'] = '-1'
                col_to_object[col_to_object=='L:'] = '-1'

            if dt[i] == 'float64':
                dot_numbers = np.array([num.replace(',','.') for num in col_to_object])
                col_to_object = dot_numbers

            new_arr[i] = col_to_object.astype(dt[i])

        return np.array(new_arr)

    def parse_region_data(self, region, data_downloaded=False):
        #check if data are downloaded
        if not data_downloaded:
            zip_files_in_folder = set([f for f in os.listdir(self.folder) if f.endswith('.zip')])
            years = ['2016', '2017', '2018', '2019', '2020']
            for file in zip_files_in_folder:
                match = re.match(r'datagis(.{0}|-rok-|-\d{2}-)(20\d{2})', file)
                if match == None:
                    continue
                else:
                    saved_year = match.group(2)
                    if saved_year in years:
                        years.remove(saved_year)
                        self.downloaded_zip_files.append(file)

            #if some year is not downloaded
            if years:
                self.download_data()

        if region not in self.region_code.keys():
            raise ValueError("Region not recognized!")

        file = "{}.csv".format(self.region_code[region])
        parsed_data = [self.header, []]
        list_of_rows = []

        for zip_file in self.downloaded_zip_files:
            path = "{}/{}".format(self.folder, zip_file)
            #open zip and extract csv file with data of region
            with zipfile.ZipFile(path, 'r') as zf:
                zf.extract(file, self.folder)
            #open csv file and parse data
            with open('{}/{}'.format(self.folder, file), encoding = "windows-1250", newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                data = [tuple(row + [region]) for row in reader]
                list_of_rows += data

        list_of_rows = np.transpose(np.array(list_of_rows))


        #delete extracted csv file
        os.remove("{}/{}".format(self.folder, file))

        parsed_data[1] = list(self.retype_col_data(list_of_rows))

        # return ([header], [data])
        return tuple(parsed_data)


    def get_list(self, regions=None):
        #if regions are not specified, get data for all regions
        if regions == None:
            regions = self.region_code.keys()

        #in 1st calling of 'parse_region_data' check if data are downloaded, then switched to True
        data_downloaded = False

        for region in regions:
            cache_file = self.cache_filename.format(region)
            #return data from memory
            if region in self.parsed_regions.keys():
                data = self.parsed_regions[region]
            #get data from cache
            elif cache_file in os.listdir(self.folder):
                #unpack gzip and load data
                with gzip.open('{}/{}'.format(self.folder, cache_file), 'rb') as cache:
                    p = pickle.Unpickler(cache)
                    data = p.load()
                self.parsed_regions[region] = data
            else: #parse (download) data, store to cache and return them
                #create gzip with pickle data
                p_data = self.parse_region_data(region, data_downloaded)
                data_downloaded = True
                data = p_data[1]
                self.parsed_regions[region] = data
                with gzip.open('{}/{}'.format(self.folder, cache_file), 'wb') as cache:
                    p = pickle.Pickler(cache)
                    p.fast = True
                    p.dump(data)


        #concatenate all data
        complete_data = [self.header, []]
        for reg in self.parsed_regions.values():
            if len(complete_data[1]) == 0:
                complete_data[1] = reg
            else:
                complete_data[1] = np.concatenate((complete_data[1], reg), axis=1)

        return tuple(complete_data)


if __name__ == "__main__":
    downloader = DataDownloader()
    regions = ['ZLK', 'JHM', 'HKK']
    data = downloader.get_list(regions)

    print('Data pro kraje: {}, {}, {}'.format(regions[0], regions[1], regions[2]))
    print('Pocet zaznamu: {}'.format(len(data[1][0])))
    print('Pocet sloupcu: {}'.format(len(data[0])))
    print('Nazvy sloupcu:')
    print(*data[0], sep=', ')
