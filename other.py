import apiai, json

def list_to_str(words):
	s = ''
	for word in words:
		s+=word+' '
	return s

def dialog(text):
	request = apiai.ApiAI('35118249a6984a9e80bef44f0eaa9b04').text_request()
	request.lang = "ru"
	request.session_id = "kirafuka"
	request.query = text
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	if response:
		return response
	else:
		return "Я не поняль"

