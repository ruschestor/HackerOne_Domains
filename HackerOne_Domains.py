### MAIN ###
# Name: 		HackerOne_Domains
# Description:	Python module for getting a list of domains from HackerOne platform.
# Version: 		1.1 | Date: 11.03.2023
# GitHub: 		https://github.com/ruschestor/HackerOne_Domains

### TESTED ENVIRONMENT ###
# Windows 10 Enterprise 2016 LTSB 1607 | Python 3.10.4 | Pip 22.0.4 | wget 3.2 | urllib3 1.26.7 | bs4 0.0.1 | cryptography 36.0.1

### VARIABLES LEGEND ###
# g_ - GLOBAL variables
# t_ - TEMP variables
# s_ - STATISTIC variables
# f_ - FILES

### MODULES ###
import json
import os
import wget
import ssl
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from cryptography import x509
from urllib.parse import urlparse
from cryptography.hazmat.backends import default_backend

### VARIABLES ###
g_url = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/hackerone_data.json"
g_url_TLDS = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
g_blocked_domains = ["hackerone.com", "github.com","gitlab.com", "*.*"]
g_blocked_symbols = ["!","@","#","$","%","^","&","(",")",";",":",",","?","=","+","<",">"]
g_protocols = ["https://","http://","ftp://"]

### FILES ###
f_temp_file_folder = "C:/temp/HackerOne_Domains/"
f_temp_file = f_temp_file_folder + "/HackerOne_Domains_" + str(datetime.now().strftime("%Y-%m-%d")) + ".json"			# Once per day
f_temp_file_top_level_domains = f_temp_file_folder + "/IANA_TLDS_" + str(datetime.now().strftime("%Y-%m")) + ".txt"		# Once per month
f_last_domainlist = f_temp_file_folder + "last_domains_main.txt"
f_last_wildcard = f_temp_file_folder + "last_domains_wildcard.txt"
f_last_log = f_temp_file_folder + "last_verbose_log.txt"
f_cache_wildcard = f_temp_file_folder + "wildcard_cache.txt"
os.makedirs(f_temp_file_folder, exist_ok=True)

### FUNCTIONS ###

# WildCard Resolver
def wcr(domain = ''):
	### PARSE CERTIFICATE ###
	wcr_result = []
	san = ""

	if domain == '':
		return None

	try:
		origin_certificate: bytes = ssl.get_server_certificate((domain, 443)).encode('utf-8')
	except:
		return None
	else:
		origin_loaded_cert = x509.load_pem_x509_certificate(origin_certificate, default_backend())
		san = (origin_loaded_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)).value.get_values_for_type(x509.DNSName)

	if "www." not in domain:
		www_domain = "www." + domain
		try:
			www_certificate: bytes = ssl.get_server_certificate((www_domain, 443)).encode('utf-8')
		except:
			pass
		else:
			www_loaded_cert = x509.load_pem_x509_certificate(www_certificate, default_backend())
			www_san = (www_loaded_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)).value.get_values_for_type(x509.DNSName)
			san = san + www_san

	# Проверка на валидность
	for i in san:
		# Remove wildcard to exclude loop
		if "*" in i:
			continue

		# Remove if SAN domain is not subdomain of original
		t_originaldomain = "." + domain
		if t_originaldomain not in i:
			continue

		if i not in wcr_result:
			wcr_result.append(i.strip().lower())


	### PARSE WEBSITE ### 
	domain_url = "https://" + domain
	try:
		reqs = requests.get(domain_url, timeout=5)
		soup = BeautifulSoup(reqs.text, 'html.parser')
	except Exception as e:
		pass
	else:
		for link in soup.find_all('a'):
			# Getting all domains from URLs on the website
			link_text = urlparse(str(link.get('href'))).netloc

			# Searching only for subdomains
			if t_originaldomain in link_text:

				# Skip duplicates
				if link_text not in wcr_result:
					wcr_result.append(link_text.strip().lower())

	# SAVE CACHE
	if wcr_result != []:
		wcr_result_text = '\n'+ '\n'.join(wcr_result)
		with open(f_cache_wildcard,"a", encoding="utf-8") as t_file:
			t_file.write(wcr_result_text)

	return wcr_result

def getdomainlist(bounties = 'yes', swag = 'no', number = 0, start = 0, test = 0, wildcardresolver = 'yes', log = 'no'):
	# bounties 			- "offers_bounties" from JSON file
	# swag 				- "offers_swag"from JSON file
	# wildcardresolver 	- Enable Wilcard Resolver function to get more subdomains of wildcard domain
	# log				- Save verbose logs
	# number:			- (Limit) How many companies will be processed: 0 - Unlimited
	# start				- (Limit) Offset
	# test				- (Test) Number of first in-scope companies. Has bigger priority intead of Limit.

	s_number_scope = 0
	s_number_scope_companies = 0
	g_target_domains = []
	g_wildcard_domains = []
	g_TLDS = []
	log_verbose = ""

	# Start log
	log_verbose += "----------------------------------\n"
	log_verbose += "Date & time: " + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "\n"
	log_verbose += "Parameters:\n"
	log_verbose += "- Bounties: " + bounties + "\n"
	log_verbose += "- Swag: " + swag + "\n"
	log_verbose += "- Wildcard Resolver: " + wildcardresolver + "\n"
	log_verbose += "- Verbose logging enabled: " + log + "\n"
	log_verbose += "- (Test) Number of first companies: " + str(test) + "\n"
	log_verbose += "- (Limit) Range of companies: " + str(start) + " - " + str(start + number) + "\n"

	# Read wildcard cache file
	if os.path.exists(f_cache_wildcard) is True:
		with open(f_cache_wildcard, "r") as t_file:
			cache_wildcard = t_file.read()
			cache_wildcard_lines = cache_wildcard.split("\n")
	else:
		cache_wildcard = ""

	# Download HACKERONE domain list from GitHub (https://github.com/arkadiyt/bounty-targets-data)
	# Download only one file per day
	if not os.path.exists(f_temp_file):
		wget.download(g_url, f_temp_file)
		log_verbose += "New JSON file downloaded = " + f_temp_file + "\n"

	# Download TLDS file only one file per month
	if not os.path.exists(f_temp_file_top_level_domains):
		wget.download(g_url_TLDS, f_temp_file_top_level_domains)
		log_verbose += "New TLDS file downloaded = " + f_temp_file_top_level_domains + "\n"

	# Reading TLDS file
	with open(f_temp_file_top_level_domains, 'r') as t_f2:
		t_TLDS = t_f2.read().splitlines(True)[:-1]
		t_TLDS = t_TLDS[1:]
		for i in t_TLDS:
			g_TLDS.append(i.strip())

	# Reading JSON source file
	with open(f_temp_file, "r", encoding='utf-8') as t_f:
		t_json_raw = json.load(t_f)
	s_number_companies = len(t_json_raw)

	# "Test" and "Limit" mode
	if test == 0:
		if number == 0:
			t_range_in_scope_companies = range(s_number_companies)
		else:
			t_range_in_scope_companies = range(start, start + number)
	else:
		t_range_in_scope_companies = range(test)

	log_verbose += "----------------------------------\n"

	for i in t_range_in_scope_companies:

		# Filter by "submission_state" = "open"
		t_json_submission_state = t_json_raw[i]['submission_state']
		if t_json_submission_state != "open":
			log_verbose += ("Company '" + t_json_raw[i]['name'] + "' skipped. submission_state = closed\n")
			continue

		# Filter company by "offers_bounties" option in account
		t_json_offers_bounties = t_json_raw[i]['offers_bounties']
		if (bounties == "yes") and (t_json_offers_bounties is False):
			log_verbose += ("Company '" + t_json_raw[i]['name'] + "' skipped. offers_bounties = false\n")
			continue

		# Filter company by "offers_swag" option in account
		t_json_offers_swag = t_json_raw[i]['offers_swag']
		if (swag == "yes") and (t_json_offers_swag is False):
			log_verbose += ("Company '" + t_json_raw[i]['name'] + "' skipped. offers_swag = false\n")
			continue

		s_number_scope_companies += 1

		t_json_raw_company = t_json_raw[i]['targets']['in_scope']

		for j in range(len(t_json_raw_company)):
			it_is_wildcard = "no"
			wcr_result_ext = []
			s_number_scope += 1
			if t_json_raw_company[j]['asset_type'] != 'URL':
				continue

			t_json_raw_domain = t_json_raw_company[j]['asset_identifier']

			# Cut URL and protocol
			if "/" in t_json_raw_domain:

				# Cut protocol (HTTP, HTTPS)
				for k in g_protocols:
					if k in t_json_raw_domain:
						t_json_raw_domain = t_json_raw_domain[len(k):]

				# Cut URL
				t_pos = t_json_raw_domain.find("/")
				if t_pos != -1:
					t_json_raw_domain = t_json_raw_domain[:-(len(t_json_raw_domain)-t_pos)]

			# Check top-level domain
			t_i = (t_json_raw_domain.split("."))[-1].upper()
			if (t_i not in g_TLDS):
				continue

			# Exclude blocked (we shouldn't check them) domains
			if t_json_raw_domain in g_blocked_domains:
				continue

			# Check wildcard
			if "*" in t_json_raw_domain:
				g_wildcard_domains.append(t_json_raw_domain)

				# Cut first "*." | Examples: *.platfoo.com"
				if t_json_raw_domain[:2] == "*.":
					t_json_raw_domain = t_json_raw_domain[2:]

				# Skip "*." | Example: "paypal-*.com"
				if "*." in t_json_raw_domain:
					continue

				# Cut first "*" | Examples: "*deere.com", "*jdisonline.com"
				if t_json_raw_domain[0] == "*":
					t_json_raw_domain = t_json_raw_domain[1:]

				# Skip ".*" | Examples: "www.*mongodb.com", "sothebysrealty.*"
				if ".*" in t_json_raw_domain:
					continue

				# Checkpoint "Is this domain wildcard?" to run "wcr" function next
				it_is_wildcard = "yes"

			# Cut the last dot (".") in the domain
			if t_json_raw_domain[-1] == ".":
				t_json_raw_domain = t_json_raw_domain[:-1]

			# Skip non-domain = without "."
			if "." not in t_json_raw_domain:
				continue

			# Exclude domains with blocked characters
			t_skip = 0
			for m in g_blocked_symbols:
				if m in t_json_raw_domain:
					t_skip = 1
			if t_skip == 1:
				continue

			# Exclude duplicates
			if t_json_raw_domain in g_target_domains:
				continue

			if it_is_wildcard == "yes":
				# Skip wcr (wildcard resolver function) if domain was checked before
				if t_json_raw_domain in cache_wildcard:
					# Get domain list from file
					for i in cache_wildcard_lines:
						if t_json_raw_domain in i:
							wcr_result_ext.append(i)
				else:
					# Run Wildcard Resolver function
					wcr_result_ext = wcr(t_json_raw_domain)


				if (wcr_result_ext != []) and (wcr_result_ext != None):
					g_target_domains += wcr_result_ext

			g_target_domains.append(t_json_raw_domain.strip().lower())

	# SAVE RESULTS
	if log == "yes":

		# SAVE DOMAIN LIST DOMAIN LIST TO THE LOG FILE
		log_domainlist = '\n'.join(g_target_domains)
		with open(f_last_domainlist,"w", encoding="utf-8") as t_file:
			t_file.write(log_domainlist)

		# SAVE WILDCARD DOMAIN LIST TO THE LOG FILE
		log_wildcard = '\n'.join(g_wildcard_domains)
		with open(f_last_wildcard,"w", encoding="utf-8") as t_file:
			t_file.write(log_wildcard)

		# SAVE VERBOSE LOGS + STATISTICS TO THE LOG FILE
		log_verbose += "----------------------------------\n"
		log_verbose += "Total number of companies: " + str(s_number_companies) + "\n"
		log_verbose += "Number of in-scope companies: " + str(s_number_scope_companies) + " of " + str(len(t_range_in_scope_companies)) + "\n"
		log_verbose += "Number of in-scope objects: " + str(s_number_scope) + "\n"
		log_verbose += "Number of real in-scope domains: " + str(len(g_target_domains)) + "\n"
		log_verbose += "Number of wildcard domains: " + str(len(g_wildcard_domains)) + "\n"
		with open(f_last_log,"w", encoding="utf-8") as t_file:
			t_file.write(log_verbose)

	# EXIT
	return g_target_domains

### START ###
if __name__ == '__main__':
	result = getdomainlist(log = 'yes', test = 10)