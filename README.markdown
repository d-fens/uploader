Python application for uploading to file hosting services
========================================================================

About
------------
Uploads files to file hosting services.

Rapidshare.com for example, runs quite fast as it hashes and reads at
the same time, with a 100MB test file:

	URL: http://rapidshare.com/files/XXXXXXXXX/test.bin.html
	Delete: http://rapidshare.com/files/XXXXXXXXX/test.bin?killcode=YYYYY
	Checksum: OK
	Uploaded in [14.27s] @ [7.01 MB/s]
	Scores [0,60000]

uploaded.to

	URL: http://ul.to/xxxxx
	Delete: http://uploaded.to/?id=yyyyyyy
	Checksum: DISABLED
	Uploaded in [16.81s] @ [5.95 MB/s]

Usage
------------

	Usage: uploader file

	Uploads files to file hosting services

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -P PROVIDER, --provider=PROVIDER
	                        sets the hosting provider
	  --collector           sets the login type as collector
	  --premium             sets the login type as premium
	  -u USERNAME, --username=USERNAME
	                        sets the username
	  -p PASSWORD, --password=PASSWORD
	                        sets the password
	  --disable-hashing     disables hashing done while uploading
	  --chunk-size=CHUNK_SIZE
	                        set the chunk size to read and upload at (bytes)


Examples
------------

Create a random 100MB file to test uploading with, `dd if=/dev/zero of=test.bin bs=100M count=1`

To upload without an account, `uploader test.bin`

To upload as a collector, `uploader --collector -u username -p password test.bin`

To upload as a premium user, `uploader --premium -u username -p password test.bin`

To upload to uploaded.to, `uploader -P uploadedto test.bin`
