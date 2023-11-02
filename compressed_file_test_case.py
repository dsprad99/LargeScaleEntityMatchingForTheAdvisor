import gzip

with gzip.open('Papers.txt.gz', 'rb') as gzfile:

    #takes 62 seconds to jump to 10MG within the MAG file

    #move to 10 MG within the MAG file from the beggining
    gzfile.seek(10 * 1024 * 1024 * 1024) 

    #data1 = gzfile.read(20)
    #data2 = gzfile.read(50)
    #data3 = gzfile.read(1000)

    #print("Data1 ",data1)
    #print("Data2 ",data2)
    #print("Data3 ",data3)

