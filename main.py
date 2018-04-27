import requests
import json
import time
from queue import deque

__auth = {

}

##

class Status:
	ACCEPTED = 202
	UNAUTHORIZED = 401
	OVER_THE_LIMIT = 413
	
	KEY_NOT_FOUND = 0

def get_domains_from_api():
	global __auth
	tenant_id = str(__auth["tenant_id"])
	token = str(__auth["token"])
	
	print("Fetching domains for user " + tenant_id)
	
	default_limit = 100
	offset = 0
	domains = deque()
	
	# This function does not cater if we encounter an
	# error and there's still remaining domain to fetch
	
	while True:
		link = "https://dns.api.rackspacecloud.com/v1.0/" + tenant_id+ "/domains?offset=" + str(offset)
		req = requests.request("GET", link, headers={"Accept": "application/json", "X-Auth-Token": token, "Content-type": "application/json"})
		status = req.status_code
		
		if status == 200:
			json_data = json.loads(req.text)
			numDomains = len(json_data["domains"])
			if(numDomains > 0):
				print("Fetching " + str(numDomains) + " domains succesful")
				domains.extend(json_data["domains"])
				offset += default_limit
			else:
				print("All domains have been fetched")
				break
		elif status == 400 or status == 500:
			print("Bad request or DNS fault")
			break
		elif status == 401:
			print("Request Unauthorized")
			break
		elif status == 413:
			print("Fetching domains are over the limit")
			break
		else:
			print("An error has occured")
			break
			
	return domains
		
	

def get_id():
	return 0
	
def delete_domains(domains_to_delete, domains_dict):
	
	deleted_file = open("deleted.txt", "a")
	not_found_file = open("not_found.txt", "a")
	
	while domains_to_delete:
		domain = domains_to_delete.popleft()
		try:
			domain_id = int(domains_dict[domain])
			status = delete_domains_from_server(domain_id)
			
			if status == Status.ACCEPTED:
				print("Domain " + domain + " is deleted from the server")
				deleted_file.write(domain + "\n")
			elif status == Status.OVER_THE_LIMIT:
				print("Delete limit reach. Pausing")
				domains_to_delete.appendleft(domain)
				time.sleep(5) # Pause for 5 seconds
			elif status == Status.UNAUTHORIZED:
				print("Authentication error. Reauthenticating...")
				set_authentication()
				
		except KeyError:
			not_found_file.write(key + "\n")
			print("Domain do not exist!")
	
	deleted_file.close()
	not_found_file.close()
			
			
def delete_domains_from_server(domain_id):
	global __auth
	tenant_id = str(__auth["tenant_id"])
	token = str(_auth["token"])
	
	link = "https://dns.api.rackspacecloud.com/v1.0/" + tenant_id + "/domains/" + str(domain_id)
	req = requests.request("DELETE", link, headers={"Accept": "application/json", "X-Auth-Token": token, "Content-type": "application/json"})
	
	return req.status_code
	
def domains_to_dict(domains):
	
	domains_dict = {}
	
	for domain in domains:
		domains_dict[domain["name"]] = domain["id"] 
		
	return domains_dict
		

def load_domains_from_file(txt_file):
	domain_file = open(txt_file, "r")
	domains = domain_file.readlines()
	d = [s.strip("\n") for s in domains] # strip the new line characters
	return d
	
def set_authentication():
	global __auth
	
	print("Getting authentication credentials")
	req = requests.request("POST", "https://identity.api.rackspacecloud.com/v2.0/tokens", data='{\"auth\":{\"RAX-KSKEY:apiKeyCredentials\":{\"username\":\"' + __auth["username"] + '\",\"apiKey\":\"' + __auth["api_key"] + '\"}}}', headers={"Content-type": "application/json"})
	
	status = req.status_code
	if(status == 200):
		# Set the global credentials
		json_data = json.loads(req.text)
		__auth["tenant_id"] = json_data["access"]["token"]["tenant"]["id"]
		__auth['token'] = json_data["access"]["token"]["id"]
		__auth["expires"]= json_data["access"]["token"]["expires"]
		
		print("Authentication succesful")
		return True
	elif status == 400:
		print("Invalid request body: unable to parse Auth data. Please review XML orJSON formatting")
		return False
	elif status == 401:
		print("Unable to authenticate user with credentials provided.")
		return False
	else:
		print("Unable to process the request")
		return False
		

def start_process():
	return 0
	
def set_credentials(txt_file):
	
	global __auth
	
	credentialFile = open("credentials.txt", "r")
	credentials = credentialFile.readlines()
	
	__auth["username"] = credentials[0].strip("\n")
	__auth["api_key"] = credentials[1].strip("\n")
	
	
	
	return 0

if __name__ == "__main__":
	set_credentials("credentials.txt")
    set_authentication()
       
    domains = get_domains_from_api()
    domains_dict = domains_to_dict(domains)
    
    domains_from_file = load_domains_from_file("domains.txt")
    delete_domains(domains_from_file, domains_dict)
	
