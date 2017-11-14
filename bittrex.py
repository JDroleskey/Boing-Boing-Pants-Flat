import requests
import csv

def API_poster(  ):
	authorization = '451035212a9b469dbe858ec0da4fb511'
	#print authorization
	api_public = 'https://bittrex.com/api/v1.1/public/'
	headers = {}
	body = { 'market': 'BTC-BCC' }
	r = requests.post('https://bittrex.com/api/v1.1/public/getmarkethistory', body, headers=headers )
	response = r.json()
	return response

def responseParser( values ):
	#values[dict][array][dict]
	values = values['result']
	values_array = []
	quantities_array = []
	for entry in values:
		values_array.append(entry['Price'])
		quantities_array.append(entry['Quantity'])
	#print len(values_array), len(quantities_array)
	return values_array, quantities_array

def weighValues( values, quantities ):
	i = 0
	totalQty = 0
	weightedValues = [0] * len(values)
	for item in quantities:
		totalQty = totalQty + item
	#print totalQty, len(values)
	for item in values:
		weightedValues[i] = ( quantities[i] * 100) / totalQty
		i = i + 1
	#print weightedValues
	return weightedValues
	
def movingAverageExponential(values, alpha, epsilon ):
   if not 0 < alpha < 1:
      raise ValueError("out of range, alpha='%s'" % alpha)
   if not 0 <= epsilon < alpha:
      raise ValueError("out of range, epsilon='%s'" % epsilon)
   result = [None] * len(values)
   for i in range(len(result)):
       currentWeight = 1.0
       numerator     = 0
       denominator   = 0
       for value in values[i::-1]:
           numerator     += value * currentWeight
           denominator   += currentWeight
           currentWeight *= alpha
           if currentWeight < epsilon: 
              break
       result[i] = numerator / denominator
   return result
   
def main():
	alpha = input("Enter a value between 0 and 1 for alpha: ")
	data = API_poster()
	order_values, order_quantities = responseParser( data )
	weights = weighValues( order_values, order_quantities )
	moving_average = movingAverageExponential( order_values, alpha, 0 )
	print order_values
	print moving_average
main()