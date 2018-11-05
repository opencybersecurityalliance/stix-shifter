BigFix Relevance Query
```
<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"> 
	<ClientQuery>
	<ApplicabilityRelevance>true</ApplicabilityRelevance>
	<QueryText>( name of it | "n/a", process id of it as string | "n/a", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes</QueryText>
	<Target>
		<CustomRelevance>true</CustomRelevance>
	</Target>
	</ClientQuery>
</BESAPI>
```

Queries for Processes Possibly we accept more hashes, md5sum and other sha's

Search by name and hash

```
[process:name = 'node' and file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5']
```

```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes whose (name of it as lowercase contains "node" as lowercase AND sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5" as lowercase )
```

An Outside OR for STIX I do not think AND makes sense here to have a process with 2 different names.

```
[process:name = 'node' and file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5'] or [process:name = 'node' and file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5']
```

```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes whose ((name of it as lowercase contains "node" as lowercase AND sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5" as lowercase) or (name of it as lowercase contains "qna" as lowercase AND sha256 of image file of it as lowercase = "33454e4fbe5b8e490512c1f6e8ac9be652341699324ee345cfed0e372a44d2d2" as lowercase))
```

Name or hash
```
[process:name = 'node' or file:hashes.sha256 = '74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88edc29cda3db3cdeb5']
```
```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes whose (name of it as lowercase contains "node" as lowercase OR sha256 of image file of it as lowercase = "74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88edc29cda3db3cdeb5" as lowercase )
```
Name
```
[process:name = 'node']
```
```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes whose (name of it as lowercase contains "node" as lowercase )
```
Just Hash
```
[process:name = * and file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5']
```
```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes whose (sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393b6ca4fb7fa5c3b682c7e5" as lowercase )
```
Return all processes on all machines

```
[process:name = * ] return all processes
```
```
( name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes
```


Big fix out

```
{'success': True, 'data': [{'computerID': 12369754, 'computerName': 'bigdata4545.canlab.ibm.com', 'subQueryID': 1, 'isFailure': False, 'result': '.err, d41d8cd98f00b204e9800998ecf8427e, /.err', 'ResponseTime': 1000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '12520437.cpx, 0a0feb9eb28bde8cd835716343b03b14, C:\\Windows\\system32\\12520437.cpx', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '12520850.cpx, d69ae057cd82d04ee7d311809abefb2a, C:\\Windows\\system32\\12520850.cpx', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '@AudioToastIcon.png, 82c37c3e27020af6c2e018e944284676, C:\\Windows\\system32\\@AudioToastIcon.png', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '@EnrollmentToastIcon.png, 495c1f072039b434827a5fe0d9761e4d, C:\\Windows\\system32\\@EnrollmentToastIcon.png', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '@VpnToastIcon.png, 1622de67156496c78d6b7be9b471645b, C:\\Windows\\system32\\@VpnToastIcon.png', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': '@WirelessDisplayToast.png, db71001fc261f6685be410527dae3942, C:\\Windows\\system32\\@WirelessDisplayToast.png', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': 'aadauthhelper.dll, f6ab187f265ce12d5fafd1019d95e7d0, C:\\Windows\\system32\\aadauthhelper.dll', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': 'aadtb.dll, 3a9d6c5d11d349cc22be7f14321fb253, C:\\Windows\\system32\\aadtb.dll', 'ResponseTime': 63000}, {'computerID': 14821900, 'computerName': 'DESKTOP-C30V1JF', 'subQueryID': 1, 'isFailure': True, 'result': 'aadWamExtension.dll, 726a345ab6086f185ddb1f3d81b363d6, C:\\Windows\\system32\\aadWamExtension.dll', 'ResponseTime': 63000}]}
```

Stix out:

```
{
  "type": "bundle",
  "id": "bundle--01af7c1a-f2c3-4214-92af-d7b463b85c7f",
  "objects": [
    {
      "type": "identity",
      "id": "identity--8db05e60-7b1b-11e8-adc0-fa7ae01bbebc",
      "identity_class": "system",
      "name": "BigFix"
    },
	{
      "type": "identity",
      "id": "identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebc",
      "identity_class": "system",
      "name": "14821900-DESKTOP-C30V1JF",
      "created_by_ref": "identity--8db05e60-7b1b-11e8-adc0-fa7ae01bbebc"
    },
    {
      "id": "observed-data--bf045a61-b750-415d-9e4a-bdd1df0fbdfa",
      "type": "observed-data",
      "created_by_ref": "identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebcc",
      "objects": {
        "0": {
          "type": "file",
          "Name": "BESClient",
          "hashes": {
            "SHA-256": "0b1f406cb743b0121d78a232bf5039e3bf93d5884caf3253ec61ecfc4f0d4692"
          },
          "parent_directory_ref": "2"
        },
        "1": {
          "type": "process",
          "pid": 15129,
          "name": "BESClient",
          "binary_ref": "0"
        },
        "2": {
          "type": "directory",
          "path": "/opt/BESClient/bin"
        }
      }
    },
    {
      "id": "observed-data--bf045a61-b750-415d-9e4a-bdd1df0fbdfa",
      "type": "observed-data",
      "created_by_ref": "identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebcc",
      "objects": {
        "0": {
          "type": "file",
          "Name": "BESClient",
          "hashes": {
            "SHA-256": "0b1f406cb743b0121d78a232bf5039e3bf93d5884caf3253ec61ecfc4f0d4692"
          },
          "parent_directory_ref": "2"
        },
        "1": {
          "type": "process",
          "pid": 15129,
          "name": "BESClient",
          "binary_ref": "0"
        },
        "2": {
          "type": "directory",
          "path": "/opt/BESClient/bin"
        }
      }
    }
  ]
}
```

Queries for Files Possibly we accept more hashes, md5sum and other sha's

Search for files in a directory via file name, hash, hash and filename, hash or filename

```
Stix in :  [file:name = 'arbitrary_file_name.txt' AND file:parent_directory_ref.path = '/etc']
```
```
(name of it | "n/a", "sha256", sha256 of it | "n/a", pathname of it | "n/a") of files whose (name of it as lowercase contains "arbitrary_file_name.txt" as lowercase) of folder ("/etc")
```
```
Stix in: [file:hashes.sha256 = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d' AND file:parent_directory_ref.path = '/root']
```
```
(name of it | "n/a", "sha256", sha256 of it | "n/a", pathname of it | "n/a") of files whose (sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d" as lowercase) of folder ("/root")
```
```
Stix in :  [file:name = 'a' AND file:parent_directory_ref.path = '/root' AND file:hashes.sha256 = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d']
```
```
(name of it | "n/a", "sha256", sha256 of it | "n/a", pathname of it | "n/a") of files whose (name of it as lowercase contains "a" as lowercase AND sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d" as lowercase) of folder ("/root")
```
```
Stix in :  [file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.sha256 = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d']
```
```
(name of it | "n/a", "sha256", sha256 of it | "n/a", pathname of it | "n/a") of files whose (name of it as lowercase contains ".bash_logout" as lowercase OR sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d" as lowercase) of folder ("/root")
```

All Files in Folder:
```
Stix in :  [file:name = '*' AND file:parent_directory_ref.path = '/root']
```
```
(name of it | "n/a", "sha256", sha256 of it | "n/a", pathname of it | "n/a") of files of folder ("/root")
```
Bigfix out
```
.bash_logout, 2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d, /root/.bash_logout
```

Stix out:
```
Formatted JSON Data
{  
   "type":"bundle",
   "id":"bundle--01af7c1a-f2c3-4214-92af-d7b463b85c7f",
   "objects":[  
      {  
         "type":"identity",
         "id":"identity--8db05e60-7b1b-11e8-adc0-fa7ae01bbebc",
         "identity_class":"system",
         "name":"BigFix"
      },
      {  
         "type":"identity",
         "id":"identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebc",
         "identity_class":"system",
         "name":"14821900-DESKTOP-C30V1JF",
         "created_by_ref":"identity--8db05e60-7b1b-11e8-adc0-fa7ae01bbebc"
      },
      {  
         "id":"observed-data--bf045a61-b750-415d-9e4a-bdd1df0fbdfa",
         "type":"observed-data",
         "created_by_ref":"identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebcc",
         "objects":{  
            "0":{  
               "type":"file",
               "Name":". bash_logout",
               "hashes":{  
                  "SHA-256":"2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d"
               },
               "parent_directory_ref":"1"
            },
            "1":{  
               "type":"directory",
               "path":"/root"
            }
         }
      },
      {  
         "id":"observed-data--bf045a61-b750-415d-9e4a-bdd1df0fbdfa",
         "type":"observed-data",
         "created_by_ref":"identity--ddb05e60-7b1b-11e8-adc0-fa7ae01bbebcc",
         "objects":{  
            "0":{  
               "type":"file",
               "Name":". bash_logout",
               "hashes":{  
                  "SHA-256":"2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2291ad5eba06683d58c48570d"
               },
               "parent_directory_ref":"1"
            },
            "1":{  
               "type":"directory",
               "path":"/root"
            }
         }
      }
   ]
}
```