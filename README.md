### Description
Python module for getting a list of domains from HackerOne platform.

Source - JSON from https://github.com/arkadiyt/bounty-targets-data

#### Included filters and checks
* Filter by "submission_state" = "open"
* Allowed only domains from Top Level Domain List (https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
* Cut the last dot (".") in the domain
* Cut URL and protocol
* Wildcard domains normalization
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
  * <any other> - get all companies
* swag = 'no' - Filter company by "offers_swag" option in account
* number = 0
* start = 0
* c_limit = 0 - Limit number of first companies

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
#### Get full list (default)
```
domains = HOD.getdomainlist()
```
#### Get list of wildcard domains
```
domains = HOD.getdomainlist(mode = 'wildcard')
```
#### Get only statistics
```
domains = HOD.getdomainlist(mode = 'statistics')
```
#### Get only statistics
```
domains = HOD.getdomainlist(mode = 'statistics')
```
### To-do
* [x] Exclude iOS & Android links
* [x]  Exclude (yoursubdomain)
* [x]  Exclude xxxxxx-*.domain.com
* [x]  All domains in lowercase
* [x] Exclude ".onion"
* [x] Cut dot "." in the end
* [x] "submission_state" filter
* [x] Consider "offers_bounties" & "offers_swag"
* [x] Exclude IP addresses
* [x] Check top level domain
* [ ] Source - URL or file
* [ ] Check JSON
* [ ] Improve statistics
* [ ] Check domains in DNS
* [ ] Support Linux
### Changelog
