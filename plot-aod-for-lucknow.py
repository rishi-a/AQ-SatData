#this file will need HDF files from NorthEast Tile of IGP. Further, shapefile of Lucknow is required

#loops through all HDF files listed in the directory
for FILENAME in os.listdir(os.getcwd()+"/data15Oct-15Nov-2019"):
    FILENAME=FILENAME.strip()
    print(FILENAME)
    #user_input=input('\nWould you like to process\n' + FILE_NAME + '\n\n(Y/N)')
    #if(user_input == 'N' or user_input == 'n'):
    #    continue
    #else:

    # A HDF file covering the tile corresponnding to northern India
    #FILE_NAME = 'MCD19A2.A2019334.h24v06.006.2019336233110.hdf'
    #Open the file
    hdf=SD.SD("data15Oct-15Nov-2019/"+FILENAME)
    #Read the subdatasets
    #extract the list of SDS in the hdf4 file
    datasets=hdf.datasets()
    #Print the list
    for i,v in enumerate(datasets):
        print('{0}. {1}'.format(i+1,v))

    # The Corresponding Lat/Long of the file
    FILE_NAME2 = 'MAIACLatlon.h25v06.hdf'
    #Open the file
    hdf2=SD.SD(FILE_NAME2)
    #Read the subdatasets
    #extract the list of SDS in the hdf4 file
    datasets2=hdf2.datasets()
    #Print the list
    for i,v in enumerate(datasets2):
        print('{0}. {1}'.format(i+1,v))
    #Variables for lat/long necessary to plot the AOD
    #Source: https://portal.nccs.nasa.gov/datashare/maiac/DataRelease/MODISTile_lat-lon/
    # Get lat and lon info
    lat = hdf2.select('lat')
    latitude = lat[:,:]
    min_lat=latitude.min()
    max_lat=latitude.max()
    lon = hdf2.select('lon')
    longitude = lon[:,:]
    min_lon=longitude.min()
    max_lon=longitude.max()

    #get SDS, (choose from the list of SDS)
    SDS_NAME = 'Optical_Depth_047'
    sds=hdf.select(SDS_NAME)
    attributes=sds.attributes()
    scale_factor=attributes['scale_factor']

    #get valid range for AOD SDS
    range=sds.getrange()
    min_range=min(range)
    max_range=max(range)
    #get SDS data
    data=sds.get()
    #get data within valid range
    valid_data=data.ravel()
    valid_data=[x for x in valid_data if x>=min_range]
    valid_data=[x for x in valid_data if x<=max_range]
    valid_data=np.asarray(valid_data)
    #scale the valid data
    valid_data=valid_data*scale_factor
    #find the average
    average=sum(valid_data)/len(valid_data)
    #find the standard deviation
    stdev=np.std(valid_data)
    #print information
    print('\nThe valid range of values is: ',round(min_range*scale_factor,3), ' to ',round(max_range*scale_factor,3),'\nThe average is: ',round(average,3),'\nThe standard deviation is: ',round(stdev,3))
    print('The range of latitude in this file is: ',min_lat,' to ',max_lat, 'degrees \nThe range of longitude in this file is: ',min_lon, ' to ',max_lon,' degrees')

    #Filter the AOD values
    attrs = sds.attributes(full=1)
    fillvalue=attrs['_FillValue']
    # fillvalue[0] is the attribute value (-9999)
    fv = fillvalue[0]
    #turn fillvalues to NaN
    data=data.astype(float)
    data[data == fv] = np.nan


    #plot the AOD
    data = np.ma.masked_array(data, np.isnan(data))
    plt.figure(figsize=(12,6))
    #Our focus is on Lucknow, not on whole of the Tile
    m = Basemap(projection='cyl', resolution='l', llcrnrlat=26.5, llcrnrlon=80.5, urcrnrlat = 27.2,  urcrnrlon = 81.5)
    #m = Basemap(projection='cyl', resolution='l', llcrnrlat=min_lat, urcrnrlat = max_lat, llcrnrlon=min_lon, urcrnrlon = max_lon)
    #lets add lucknow shapefile
    m.readshapefile('LucknowDistrict\Lucknow_district', 'lucknw', drawbounds=True)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90., 120., 5.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 181., 5.), labels=[0, 0, 0, 1])
    x, y = m(longitude, latitude)
    quadmesh = m.pcolormesh(x, y, data[2]*scale_factor, cmap=plt.cm.jet)
    # dont autoscale
    #plt.autoscale()
    #create colorbar
    cb = m.colorbar()
    quadmesh.set_clim(vmin=0, vmax=4)
    #label colorboar
    cb.set_label('AOD')

    #title the plot
    plotTitle=FILENAME[:-4]
    plt.title('{0}\n {1}'.format(plotTitle, SDS_NAME))
    fig = plt.gcf()
    # Show the plot window.
    plt.show()
    pngfile = '{0}-aod.png'.format(plotTitle)
    fig.savefig("gif/"+pngfile)
    plt.close()
