# To use this file, first head over to https://ladsweb.modaps.eosdis.nasa.gov/search/order and generate the csv file containing the list of hdf files

# Generate your token from https://ladsweb.modaps.eosdis.nasa.gov/profile/#app-keys


CSV_FILE = "fileList.csv"

#Give your destination folder
DEST = "data/" 
listofFiles=pd.read_csv(CSV_FILE)['fileUrls for custom selected']
for f in listofFiles:
    # -45 till end selects the filename only
    filename=f[-45:]
    headers = {
    'Authorization': 'Bearer <your-token-here without <> >',
    }
    response = requests.get('https://ladsweb.modaps.eosdis.nasa.gov'+f, headers = headers)

    with open(DEST+filename, 'wb') as outfile: 
        outfile.write(response.content)
        print(filename+" saved")