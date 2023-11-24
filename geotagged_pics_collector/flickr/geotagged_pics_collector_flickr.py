from flickrapi import FlickrAPI
import json
import pandas as pd
import requests
import time

key = "a6xxcbxxxxx6cc78xxxxxx48c18xxxd7" # Replace with your API key
secret = "1f1xxxxxxbc7b884" # Replace with your API secret

# Span to access the flickr server
wait_time = 10
keyword = 'oostvaardersplassen' # Change the keyword for your study area
boundary = '5.284280450593758,52.38235005699285, 5.44123138402426, 52.51217455196319', #Please change the here for your study area in the order. LonLL, LatLL, LonUR, LatUR. LL:Lower Left corner, UR:Upper Right corner

# connecting to Flickr
flickr = FlickrAPI(key, secret, format='parsed-json')

for year in range(2010, 2024):
    output = f'{keyword}_{year}'
     ## Please change the output file name

    photos = []
    l = 0
    
    i = 1
    while True:
        ##Loop start
        # Check the parameters of flickr.photos.search at https://www.flickr.com/services/api/flickr.photos.search.html
        result = flickr.photos.search(
            text = keyword,    # keyword
            per_page = 400,            # number of data per page
            has_geo = 1,               # Photo that has geo location
            min_taken_date = f'{year}-01-01', # collecting photos from the first day of the year
            max_taken_date = f'{year}-12-31', # collecting photos till the last day of the year
            bbox = boundary,           #boundary box 
            media = 'photos',         # collecting photos without video
            sort =  'date-taken-desc',       # collecting photos from latest
            privacy_filter =1,
            safe_search = 1,          # Photos without violence
            extras = 'geo,url_n,date_taken,views,license',
            page = i
        )

        # export result
        #photos = ChainMap(photos, result['photos'])
        #photos = result['photos']
        j = result['photos']
        
        print('total_photo', j['total'])
        print('Current_pages', i)
        
        photos += j['photo']

        #you can download up to 4000 photos in one query. per_page * page <= 4000
        if i > 10 :
            print('Your query has been exceeded the limit of photos: 4000 photos' + str(i))
            break
        elif i >= j['pages'] :
            break
        i += 1

    # export as Json format
    d = json.dumps(photos, sort_keys = True, indent = 2)
    #print(d)
    fp = open(output+'.json', 'w' )
    fp.write( d )
    fp.close()

    # export as csv
    df = pd.read_json(d)
    df.to_csv(output+'.csv', encoding='utf-8')

    # wait for 10 seconds
    time.sleep(wait_time)

    urls = df['url_n']

    for i, url in enumerate(urls.values):
        filename = f'{year}_image-{i}.jpg'
        r = requests.get(url)
        with open('Images/'+filename, 'wb') as outfile:
            outfile.write(r.content)

    # wait for 10 seconds
    time.sleep(wait_time)