from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

# datetime_object = datetime.strptime

to=''
@app.route('/')
def home():
    return render_template('template.html')


@app.route('/submit', methods=['POST'])
def search():
        global to
        From = str(request.form['from'])
        to = str(request.form['to'])
        date = str(request.form['date'])
        date = date.replace("-", "/")
        adult = str(request.form['adult'])  
        child = str(request.form['child'])
        #API KODE AIRPORT
        if len(From)>3:
            url = f"https://world-airports-directory.p.rapidapi.com/v1/airports/{From}"

            querystring = {"page":"1","limit":"20","sortBy":"AirportName:asc"}

            headers = {
                "X-RapidAPI-Key": "9cc8be294bmsh502182750eb8c0dp1d1afcjsn7c3940e4e5b5",
                "X-RapidAPI-Host": "world-airports-directory.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            iata=response.json()
            iata_f=iata['results']
            if len(iata_f)>1:
                iata_f=iata['results'][3]['AirportCode']
            else:
                iata_f=iata['results'][0]['AirportCode']
            From=iata_f
            From=str(From)
        if len(to)>3:
            url = f"https://world-airports-directory.p.rapidapi.com/v1/airports/{to}"

            querystring = {"page":"1","limit":"20","sortBy":"AirportName:asc"}

            headers = {
                "X-RapidAPI-Key": "9cc8be294bmsh502182750eb8c0dp1d1afcjsn7c3940e4e5b5",
                "X-RapidAPI-Host": "world-airports-directory.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            iata=response.json()
            iata_t=iata['results']
            if len(iata_t)>1:
                iata_t=iata['results'][2]['AirportCode']
            else:
                iata_t=iata['results'][0]['AirportCode']
            to=iata_t
            to=str(to)
        #END OF API KODE AIRPORT

        #API SEARCH FLIGHT
        url = "https://flight-fare-search.p.rapidapi.com/v2/flights/"

        # querystring = {f"from":"SUB","to":"HND","date":"2024/03/23","adult":"1","child":"0","infant":"0","type":"economy","currency":"USD"}
        querystring = {f"from":{From},"to":{to},"date":{date},"adult":{adult},"child":{child},"infant":"0","type":"economy","currency":"USD"}
        headers = {
            "X-RapidAPI-Key": "9cc8be294bmsh502182750eb8c0dp1d1afcjsn7c3940e4e5b5",
            "X-RapidAPI-Host": "flight-fare-search.p.rapidapi.com"
        }

        response_flight = requests.get(url, headers=headers, params=querystring)

        flight=response_flight.json()
        flight=flight['results']

        url = "https://currency-exchange.p.rapidapi.com/exchange"

        querystring = {"from":"USD","to":"IDR","q":"1.0"}

        headers = {
            "X-RapidAPI-Key": "9cc8be294bmsh502182750eb8c0dp1d1afcjsn7c3940e4e5b5",
            "X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
        }

        response_ex = requests.get(url, headers=headers, params=querystring)
        exchange_rate=response_ex.json()

        # for flight_details in flight:
        #     flight_details['totals']['total'] = int(flight_details['totals']['total']) * int(exchange_rate)
        #     flight_details['totals']['total']=str(flight_details['totals']['total'])
        for i in flight:
            i['totals']['total']= int(i['totals']['total'])
            i['totals']['total']= (i['totals']['total'])*exchange_rate

        # return flight
        return render_template('tes.html', data=flight)
        
        #END OF API SEARCH FLIGHT
        

@app.route('/itinerary', methods=['POST'])
def itinerary():
    global to 
    dest=to   
    url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
        {
            "content": "Hello! I'm an AI assistant bot based on ChatGPT 3. How may I help you?",
            "role": "system"
        },
        {
            "content": f"Create an itinerary for Holiday in {dest}",
            "role": "user"
        }
    ]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "d903ff2c4cmsh002c3fd9b5f384fp19e678jsned9aa22936be",
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    text=response.json()


    return render_template('itinerary.html', data = text)



   
        



if __name__== '__main__':
    app.run(debug=True)