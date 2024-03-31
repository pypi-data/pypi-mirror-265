=======
webstor
=======

.. image:: https://img.shields.io/travis/RossGeerlings/webstor.svg
        :target: https://travis-ci.org/RossGeerlings/webstor

.. image:: https://img.shields.io/pypi/v/webstor.svg
        :target: https://pypi.python.org/pypi/webstor


A script to quickly enumerate all websites across all of your organization's networks, store their responses, and query for known web technologies, such as those with zero-day vulnerabilities.

* Free software: MIT license
* Documentation: https://RossGeerlings.github.com/webstor.

Features
--------

WebStor is a tool implemented in Python under the MIT license for quickly enumerating all websites across all of your organization's networks, storing their responses, and querying for known web technologies and versions, such as those with zero-day vulnerabilities. It is intended, in particular, to solve the unique problem presented in mid to large sized organizations with decentralized administration, wherein it can be almost impossible to track all of the web technologies deployed by various administrators distributed across different units and networks.

WebStor achieves its goal by performing the following actions:

1. Performs DNS zone transfers to collect an organization's A and CNAME records.
2. Uses Masscan to scan for open HTTP/HTTPS ports on an organization's net ranges, as well as any IP addresses outside those ranges that were present in the organization's A and CNAME records.
3. Uses the Python requests library to collect all responses and store in a MariaDB database. All DNS names corresponding to an IP with open HTTP/HTTPS ports will be included in requests in addition to the IP address, so that sites using different headers will not cause a website to be missed.
4. Downloads Wappalyzer web technologies database and stores in MariaDB database, enabling users to query the location(s) of a common web technology by name.
5. Allows users to query the location(s) where custom regexes are contained within stored responses.
