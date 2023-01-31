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

#### Options
* **mode**
  * 'default' (default value) - get full domain list
  * 'wildcard' - get only wildcard domains
  * 'statistics' - get only statistics
* **bounties** - filter company by "offers_bounties" option in account
  * 'yes' (default value) - get companies that offer bounties
  * 'no' - get all companies
* **swag** - filter company by "offers_swag" option in account
  * 'yes' - get companies that offer swag
  * 'no' (default value) - get all companies
* **number** - how many domains should be in total
  * 0 (default value) - get all domains
* **start** - offset from number of domains
  * 0 (default value) - start from 0
* **c_limit** - Limit number of first companies (e.g. for test)
  * 0 (default value) - get all companies

#### Temporary files
The module saves temporary files in "C:/temp/HackerOne_Domains/":
* "HackerOne_Domains_YYYY-MM-DD.json" - Source JSON file.
* "IANA_TLDS_YYYY-MM.txt" - Official list of Top Level Domains.
* "results.txt" - Result of last run.

### How to use
#### Import module
```
import HackerOne_Domains as HOD
```
#### Get list of domains with bounty offer (default state)
mode = 'default', bounties = 'yes', swag = 'no', number = 0, start = 0, c_limit = 0
```
domains = HOD.getdomainlist()
```
#### Get list of wildcard domains
```
domains = HOD.getdomainlist(mode = 'wildcard')
```
#### Get only statistics
```
stat = HOD.getdomainlist(mode = 'statistics')
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
* [ ] Source - URL or file
* [ ] Check JSON
* [ ] Improve statistics
* [ ] Domain validation in DNS
* [ ] Support Linux
* [ ] Improve start/number feature
* [ ] Wildcard domains: certificates
### Changelog
