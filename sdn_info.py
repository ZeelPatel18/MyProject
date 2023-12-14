import requests
import json
from git import Repo

def get_topology_info():
	url = 'http://localhost:8080/topology/switches'
	try:
		response = requests.get(url)
		if response.status_code == 200:
			topology_info = response.json()
			return topology_info
		else:
			print("failed to retrive topology info. status code:", response.status_code)
	except requests.exceptions.RequestException as e:
		print("Request Failed:", e)	
	return None
	
def push_to_git(data):
	try:
		repo = Repo.init("/home/student/")
		
		with open('/home/student/data.json', 'w') as file:
			json.dump(data, file)
		
		repo.index.add(['data.json'])
		
		repo.index.commit("Update data")
		
		origin = repo.create.remote('origin', 'https://ZeelPatel18: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@github.com/ZeelPatel18/MyProject.git')
		origin.push(refspac='refs/heads/main', force=True)
		print("Data pushed to git repository successfully")
	except Exception as e:
		print("Failed to push", e)
				
topology_data = get_topology_info()

if topology_data:
	push_to_git(topology_data)
else:
	print("Failed to retrieve topology info.")

