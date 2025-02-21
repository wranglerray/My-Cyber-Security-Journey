reptor conf

07/17/24 16:36:17:~ > reptor conf

~~~
Server [http://127.0.0.1:8000]:    
API Token [redacted]:    
Project ID [34fb52d3-35df-471b-9ef3-35407181f5f2]:    
Store to config to /home/ray/.sysreptor/config.yaml? [y/n]:
~~~

API Token

![[sysrepapi.png]]
![[projectid.png]]

Rustscan output to sysreptor

~~~
sudo rustscan -a --accessible $target - -- -n -sV -oX - | tee rust.xml
~~~

~~~
reptor nmap --xml -i rust.xml --upload
~~~

Findings

.toml format

~~~
status = "in-progress"

[data]
cvss = "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"
title = "Unrestricted file uplpad"
summary = ".We detected a unrestricted file upload vulnerability"
references = [ "https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload",]
description = "Leads to Remote Code Execution."
recommendation = "Apply Patching to server."
affected_components = [ "http://lms.permx.htb/main/inc/lib/javascript/bigupload/inc/bigUpload.php",]
~~~

Create .toml templates and upload to sysreptor

~~~
cat finding.toml | reptor finding
~~~

Will upload to current project in conf file