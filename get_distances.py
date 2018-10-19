# -*- coding: utf-8 -*-

import datetime
import urllib

import requests


def build_request_google_map_url(str_origins, str_destinations, str_api_key, str_google_api_url, str_units = 'imperial'):
    """
    A function to build the request URL to call Google API service.

    inpput:
    str_origins: string, e.g 41.43206,-81.38992, if multiple, connect with '|', e.g. 41.43206,-81.38992|-33.86748,151.20699
    str_destinations: string, similar with str_origins
    api_key: your Google map API key
    units: metric or imperial

    output: a full url string which can be used to get google distance matrix.

    for more please refer to Google doc:
    (https://developers.google.com/maps/documentation/distance-matrix/start

    """
    url_prameters = {'units':str_units, 'origins':str_origins, 'destinations':str_destinations, 'key':str_api_key}
    request_url = str_google_api_url + urllib.parse.urlencode(url_prameters)

    # if len(request_url) > GOOGLE_URL_LIMITATION:
    #     print('**ERROR**: Too many locations, cause the url exceed the accpted URL limitation ' + str(GOOGLE_URL_LIMITATION))
    #     return None

    return request_url

def get_distance_with_pairs_points_ignore(list_pairs_points):
    """
    A function to get distances with pairs of points by using Google Map API at only one HTTP request.

    ignored this fucntion, as Google API will return N*N results, e.g. 3 origins and 3 destinations, will get 9 results.
    But we only want 3, so ignore this.

    input(base on the homework assignment):
    A list contains some pairs of points, [(origin, destination)，]
        e.g. [((51.72756055,5.547473487), (51.673471,5.604358))]
    output: The distance of the pair points

    As described in the Google map API doc:
    "Note: URLs must be properly encoded to be valid and are limited to 8192 characters for all web services."

    So, if the count pair points are too many, will get error.

    """
    #

    if not len(list_pairs_points):
        print('**ERROR**: empty pair points.')
        return None
    list_origins = []
    list_destinations = []

    for pair in list_pairs_points:
        print(pair)
        list_origins.append(str(pair[0]).strip('()'))
        list_destinations.append(str(pair[1]).strip('()'))


    zipped = zip(list_pairs_points)
    str_origins = '|'.join(list_origins).replace(' ', '')
    str_destinations = '|'.join(list_destinations).replace(' ', '')


    # Get the request url with origins and destinations.
    #
    request_url = build_request_google_map_url(str_origins, str_destinations, API_KEY)
    if not request_url:
        print('**ERROR**: could not get the valid request url, please check.')

    response = requests.get(request_url)

    if 200 != response.status_code:
        print('**ERROR**:  Cannot access google service, please check your network, or ping google.com first.')
        return None

    dict_repsone_content = response.json()
    print(dict_repsone_content)
    if dict_repsone_content['status'] != 'OK':
        print('**ERROR**: Response status is: ' + dict_repsone_content['status'])
        return None
    else:
        return dict_repsone_content


def get_distance_with_pairs_points(list_pairs_points, str_key, str_google_api_url):
    """
    A function to get distances with pairs of points by using Google Map API.

    Get the distance of pairs one by one.

    input(base on the homework assignment):
    A list contains some pairs of points, [(origin, destination)，]
        e.g. [((51.72756055,5.547473487), (51.673471,5.604358))]
    output: dict contains of the distance of the pair points, also other infor,
        e.g.


    """
    if not len(list_pairs_points):
        print('**ERROR**: empty pair points.')
        return None

    list_distance_result = []

    for tuple_pair in list_pairs_points:
        # Get the pair of points one by one, send the HTTP request and get the distance.
        #
        str_origin = str(tuple_pair[0]).strip('()').replace(' ', '')
        str_destination = str(tuple_pair[1]).strip('()').replace(' ', '')

        # Get the request url with origins and destinations.
        #
        request_url = build_request_google_map_url(str_origin, str_destination, str_key, str_google_api_url)
        if not request_url:
            print('**ERROR**: could not get the valid request url, please check.')
            continue
        else:

            print('Ruesting the url...and the pair of points is: ')
            print(tuple_pair)
            response = requests.get(request_url)

            if 200 != response.status_code:
                print('**ERROR**:  Cannot access google service, please check your network, or ping google.com first.')
            else:

                dict_repsone_content = response.json()

                if dict_repsone_content['status'] != 'OK':
                    print('**ERROR**: Response status is: ' + dict_repsone_content['status'])

                else:
                    # Return the distance, also other more message to be saved in csv
                    #
                    str_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dict_distance = {'timestamp': str_timestamp, 'origin_latitude_longitude': str_origin, 'destination_latitude_longitude': str_destination}

                    dict_distance.update({'origin_addresses': dict_repsone_content['origin_addresses'][0]})
                    dict_distance.update({'destination_addresses': dict_repsone_content['destination_addresses'][0]})
                    dict_distance.update({'distance_value': dict_repsone_content['rows'][0]['elements'][0]['distance']['value']})

                    list_distance_result.append(dict_distance)

    return list_distance_result
