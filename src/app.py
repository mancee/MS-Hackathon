# from flask import Flask, render_template
#
# app = Flask(__name__)
# app.secret_key = 'ishween'
# app.config.from_object('config')
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
from flask import Flask, render_template, request, jsonify
import requests
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/square/', methods=['POST'])
# def square():
#     num = float(request.form.get('number', 0))
#     square = num ** 2
#     data = {'square': square}
#     data = jsonify(data)
#     return data

# https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/distance_matrix/driving/90.33687,23.470314;90.379249,23.497178;90.497009,23.546286?rtype=1&region=bgd

@app.route('/square/', methods=['GET','POST'])
def square():
    source = request.form.get('source')
    destination = request.form.get('destination')

    #oauth tokens api
    # oauth = "https://outpost.mapmyindia.com/api/security/oauth/token"
    # parameters = {"grant_type": "client_credentials",
    #                 "client_id": "O3wMiHiw95v3LsJ-IiCHxZ2HM2c8F5H8xfdzLnrPdbEkNGsIbvSqKhFUmMHjOz3u1eeu1aIREb42bpDzRij_bA==",
    #                 "client_secret": "QJcH6ymTGazxFG8ml9UT-UFotuIYSvB-rWynBvJFd1HJULek4Si3KfyimmwjmlKcQVMHwVW8e-rO7J9VaufHgY6XBMp0LC1O"}

    # simran di credentials
    parameters = {"grant_type": "client_credentials",
                  "client_id": "uGlZhB6jaQrOIDDpMHcVhtkKs2dwLw6fpxd13ixBaSSSUg3EiW_je679AipUqKc2C4znacDnV7s9Gtc9YrrOZQ==",
                  "client_secret": "9K_q_9Q2GHOu0mO9quT6-F5hcdWkz01xynIjefCM2iBgTgkWb0Ores6ov9ov0E502XLF8UUDyy9bakh2N0bzSaBNYjC-nFAF"}

    resp = requests.post("https://outpost.mapmyindia.com/api/security/oauth/token", params=parameters)
    tokens = resp.json()
    access_token = tokens['access_token']
    token_type = tokens['token_type']
    print(access_token)
    print(token_type)

    #geocoding api
    address_source = "https://atlas.mapmyindia.com/api/places/geocode?address={}".format(source)
    headers = '{}'.format(token_type+" "+access_token)
    location_source = requests.get(address_source, headers={'Authorization':headers})
    json_source = location_source.json()
    source_longitude = json_source['copResults']['longitude']
    source_latitude = json_source['copResults']['latitude']
    print(json_source)

    address_destination = "https://atlas.mapmyindia.com/api/places/geocode?address={}".format(destination)
    headers = '{}'.format(token_type + " " + access_token)
    location_destination = requests.get(address_destination, headers={'Authorization': headers})
    json_destination = location_destination.json()
    destination_longitude = json_destination['copResults']['longitude']
    destination_latitude = json_destination['copResults']['latitude']
    print(json_destination)

    #multiple lat long api
    # arr = {'square':"source_latitude, source_longitude+destination_latitude+,+destination_longitude"}
    # print(arr)

    #find distance
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/77.216721,28.644800;75.778885,26.922070?steps=false&rtype=1&alternatives=3"
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/distance_matrix/driving/{},{};{},{}?rtype=0&region=ind".format(source_longitude, source_latitude, destination_longitude, destination_latitude)

    # simran
    str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/distance_matrix/driving/{},{};{},{}?rtype=0&region=ind".format(source_longitude, source_latitude, destination_longitude, destination_latitude)
    predict = requests.get(str)
    print(predict)
    data = predict.json()
    print(data)
    distance = data['results']['distances'][0][1]
    duration = data['results']['durations'][0][1]

    # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)

    #simran
    str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)

    resp = requests.get(str)
    # print(resp)
    route = resp.json()
    geometry = ''
    min = sys.maxsize
    time = 0
    print(route)
    for element in route['routes']:
        if element['distance']-1000 <= distance and element['distance']+1000 >= distance:
            if element['distance'] < min:
                min = element['distance']
                time = element['duration']
                geometry = element['geometry']
                print(min)

    #BIKING
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/distance_matrix/biking/{},{};{},{}?rtype=0&region=ind".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    # predict = requests.get(str)
    # print(predict)
    # data = predict.json()
    # print(data)
    # distance = data['results']['distances'][0][1]
    # duration = data['results']['durations'][0][1]
    #
    # # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # # simran
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/route_adv/biking/{},{};{},{}?steps=false&rtype=1".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # resp = requests.get(str)
    # # print(resp)
    # route = resp.json()
    # biking_geometry = ''
    # min = sys.maxsize
    # biking_time = 0
    # print(route)
    # for element in route['routes']:
    #     if element['distance'] - 1000 <= distance and element['distance'] + 1000 >= distance:
    #         if element['distance'] < min:
    #             min = element['distance']
    #             biking_time = element['duration']
    #             biking_geometry = element['geometry']
    #             print(min)

    # print("yes")
    #WALKING
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/distance_matrix/walking/{},{};{},{}?rtype=0&region=ind".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    # predict = requests.get(str)
    # print(predict)
    # data = predict.json()
    # print(data)
    # distance = data['results']['distances'][0][1]
    # duration = data['results']['durations'][0][1]
    #
    # # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # # simran
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/route_adv/walking/{},{};{},{}?steps=false&rtype=1".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # resp = requests.get(str)
    # # print(resp)
    # route = resp.json()
    # walking_geometry = ''
    # min = sys.maxsize
    # walking_time = 0
    # print(route)
    # for element in route['routes']:
    #     if element['distance'] - 1000 <= distance and element['distance'] + 1000 >= distance:
    #         if element['distance'] < min:
    #             min = element['distance']
    #             walking_time = element['duration']
    #             walking_geometry = element['geometry']
    #             print(min)
    #
    # print(4)
    #TRUCKING
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/distance_matrix/trucking/{},{};{},{}?rtype=0&region=ind".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    # predict = requests.get(str)
    # print(predict)
    # data = predict.json()
    # print(data)
    # distance = data['results']['distances'][0][1]
    # duration = data['results']['durations'][0][1]
    #
    # # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # # simran
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/9kibr32m4r29uw8sgsjan8rdu89v9yit/route_adv/trucking/{},{};{},{}?steps=false&rtype=1".format(
    #     source_longitude, source_latitude, destination_longitude, destination_latitude)
    #
    # resp = requests.get(str)
    # # print(resp)
    # route = resp.json()
    # trucking_geometry = ''
    # min = sys.maxsize
    # trucking_time = 0
    # print(route)
    # for element in route['routes']:
    #     if element['distance'] - 1000 <= distance and element['distance'] + 1000 >= distance:
    #         if element['distance'] < min:
    #             min = element['distance']
    #             trucking_time = element['duration']
    #             trucking_geometry = element['geometry']
    #             print(min)

    # geometry = route['routes'][0]['geometry']
    arr = {'geometry': geometry, 'time': time}
    arr = jsonify(arr)
    return arr

    # https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/distance_matrix_predictive/driving/77.5998448,12.5090914;77.5800417,12.5092973?dep_time=1531543500
    # https: // apis.mapmyindia.com / advancedmaps / v1 / ejls5j1jcdu6z9w1pabuytir9wwituo8 / route_adv / driving / 77.131123, 28.552413;77.113091, 28.544649?steps = false & rtype = 1

    # str = "https://atlas.mapmyindia.com/api/places/textsearch/json?query={} phase 3&region=ind".format(source)
    # response_source = requests.get(str)
    # str = "https://atlas.mapmyindia.com/api/places/textsearch/json?query={} phase 3&region=ind".format(destination)
    # response_destination = requests.get(str)

    # source_longitude = response_source['suggestedLocations'][0]['longitude']
    # source_latitude = response_source['suggestedLocations'][0]['latitude']
    # destination_longitutde = response_destination['suggestedLocations'][0]['longitude']
    # destination_latitude = response_destination['suggestedLocations'][0]['latitude']
    #
    # print(source)
    # print(destination)
    #
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/77.131123,28.552413;77.113091,28.544649?steps=false&rtype=1"
    # response = requests.get(str)


#
# if __name__ == '__main__':
#     app.run(debug=True)