### Description
Python module for getting a list of domains from HackerOne platform.

Source - JSON from https://github.com/arkadiyt/bounty-targets-data

Filters/checks:
* Filter by "submission_state" = "open"
* Allowed only domains from Top Level Domain List (https://data.iana.org/TLD/tlds-alpha-by-domain.txt)
* Cut the last dot (".") in the domain
* Cut URL and protocol
* Wildcard domains normalization
* Exclude domains with blocked characters
* Exclude repositories domains (github.com, gitlab.com)
* Exclude duplicates

Options:
* Filter company by "offers_bounties" option in account
* Filter company by "offers_swag" option in account
* Limit number of first companies

### How to use
```
import HackerOne_Domains as HOD
domains = HOD.getdomainlist()
```
### To-do
* [+] Exclude iOS & Android links
* [+] Exclude (yoursubdomain)
* [+] Exclude xxxxxx-*.domain.com
* [+] All domains in lowercase
* [+] Exclude ".onion"
* [+] Cut dot "." in the end
* [+] "submission_state" filter
* [+] Consider "offers_bounties" & "offers_swag"
* [+] Exclude IP addresses
* [+] Check top level domain
* [-] Source - URL or file
* [-] Check JSON
* [-] Improve statistics
* [-] Check domains in DNS
* [-] Support Linux
### Changelog
