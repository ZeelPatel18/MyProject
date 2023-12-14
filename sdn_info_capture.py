import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

def make_request(url):
	session = requests.Session()
	retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
	session.mount('http://', HTTPAdapter(max_retries=retries))
	try:
		response = session.get(url)
		response.raise_for_status()
		return response
	except requests.exceptions.RequestException as e:
		print("Request failed:", e)
		return None

def get_switches_info():
	url = 'http://localhost:8080/stats/switches'
	response = make_request(url)
	if response and response.status_code == 200:
		switches_info = response.json()
		return switches_info
	else:
		if response is not None:
			print("Failed to retrieve switch information. Status Code: {}".format(response.status_code))
			print(response.text)
		else:
			print("Failed to retrieve switch information. Connection error or timeout.")
		return None
		
switches = get_switches_info()

if switches:
	github_repo_url = 'https://github.com/ZeelPatel18/MyProject.git'
	headers = {'Authorization': 'token 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'}
	
	data_to_push = json.dumps(switches)

	response = requests.post(github_repo_url, headers=headers, data=data_to_push)

	if response.status_code == 201:
		print("Data pushed to GitHub successfully!")
	else:
		print("Failed to push data to GitHub")
else:
	print("Failed to retrieve switch information.")
