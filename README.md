### Description
Python module for getting a list of domains from HackerOne platform.

Source - JSON from https://github.com/arkadiyt/bounty-targets-data

#### Included filters and checks
* Filter by "submission_state" = "open"
* Allowed only domains from Top Level Domain List (https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
* Cut the last dot (".") in the domain
* Cut URL and protocol
* Wildcard domains normalization (*.domain.com > domain.com)
* Exclude domains with blocked characters
* Exclude repositories domains (github.com, gitlab.com)
* Exclude duplicates
* Searching additional subdomains (if wildcard is specified) in certificate and links of website

#### Options
* **bounties** - filter company by "offers_bounties" option in account
  * 'yes' (default value) - get companies that offer bounties
  * 'no' - get all companies
* **swag** - filter company by "offers_swag" option in account
  * 'yes' - get companies that offer swag
  * 'no' (default value) - get all companies
* **number** - (Limit mode) how many companies should be in total
  * 0 (default value) - get all companies
* **start** - (Limit mode) offset from number of companies
  * 0 (default value) - start from 0
* **test** - (Test mode) limit number of first companies (e.g. for test)
  * 0 (default value) - get all companies
* **wildcardresolver** - additional function to searching for subdomains.
  * 'yes' (default value) - enable
  * 'no' - disable
* **log** - save result, verbose log and statistics to files.
  * 'yes' - enable
  * 'no' (default value) - disable

#### Temporary files
The module saves temporary files in "C:/temp/HackerOne_Domains/":
* "HackerOne_Domains_YYYY-MM-DD.json" - Source JSON file.
* "IANA_TLDS_YYYY-MM.txt" - Official list of Top Level Domains.
* "last_domains_main.txt" - List of resulted domains of the last session.
* "last_domains_wildcard.txt" - List of wildcard domains of the last session.
* "last_verbose_log.txt" - Detailed log of the last session.
* "wildcard_cache.txt" - Cache of the Wildcard Resolver function. To avoid frequent requests to websites. Just delete it to flush.

### How to use
#### Import module
```
import HackerOne_Domains as HOD
```
#### Get list of domains with bounty offer (default state)
bounties = 'yes', swag = 'no', number = 0, start = 0, test = 0, wildcardresolver = 'yes', log = 'no'
```
domains = HOD.getdomainlist()
```
#### Test on 10 companies
```
domains = HOD.getdomainlist(log = 'yes', test = 10)
```
#### Get full list of domains (even without bounty and swag)
```
domains = HOD.getdomainlist(bounties = 'no')
```
### To-do
* [x] Exclude iOS & Android links
* [x] Exclude (yoursubdomain)
* [x] Exclude xxxxxx-*.domain.com
* [x] All domains in lowercase
* [x] Exclude ".onion"
* [x] Cut dot "." in the end
* [x] "submission_state" filter
* [x] Consider "offers_bounties" & "offers_swag"
* [x] Exclude IP addresses
* [x] Check top level domain
* [x] Improve statistics
* [x] Improve start/number feature
* [x] Wildcard domains: certificates
### Changelog
## v1.1:
* Parameter "c_limit" of the "getdomainlist" function renamed to "test".
* Improved logging: single parameter "log" for 3 files.
* Improved "Test" and "Limit" modes.
* Added function (parameter "wildcardresolver") Wildcard Resolver to find additional subdomains by parsing website links and certificate (Subject Alternate Name).
## v1.2:
* Fixed issue "cryptography.x509.extensions.ExtensionNotFound: No <class 'cryptography.x509.extensions.SubjectAlternativeName'> extension was found".
* Fixed a few minor issues
* Improved statistics
