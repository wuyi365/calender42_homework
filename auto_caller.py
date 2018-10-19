# -*- coding: utf-8 -*-

import csv
import os.path
import time

from get_distances import *

if __name__ == '__main__':
    # need to apply your own api key, this is mine, and works well
    API_KEY = 'AIzaSyBn9ujsIDxFTNedLfN-wNcrfGu7_A-Tzag'
    GOOGLE_MAP_API_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    csv_file = 'distance.csv'

    file_exists = os.path.isfile(csv_file)


    # Call the function in another script(as requirement) and write into csv file in this script
    #
    list_pairs_points = [((51.72756055,5.547473487), (51.673471,5.604358)), ((51.72756055,5.547473487), (51.673471,5.604358)), ((50.6772072,5.5959908), (50.814113,5.166075)), ((50.9442881,5.4674197), (50.814113,5.166075)), ((52.3802093,4.872755698), (51.953257,4.55655)), ((52.34397807,4.825849925), (51.953257,4.55655))]


    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'origin_latitude_longitude', 'destination_latitude_longitude', 'origin_addresses', 'destination_addresses', 'distance_value']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

        if not file_exists:
            writer.writeheader()

        while True:

            # Call the function to get the distance
            #
            dict_result = get_distance_with_pairs_points(list_pairs_points, API_KEY, GOOGLE_MAP_API_URL)

            for dic_row in dict_result:
                writer.writerow(dic_row)

            # run the script every 10 minutes(the recommended way is to calling the function)
            #
            print('Sleeping...will execute again after 10 minutes...')
            time.sleep(600)
