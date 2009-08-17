Python application for uploading to Rapidshare (other providers later on)
========================================================================

About
------------
Uploads files to Rapidshare.com, it runs quite fast as it hashes and reads at
the same time, example of 100MB test file `uploaded in [13.9677670002s] @ [7.16 Mb/s]`


Usage
------------

	Usage: uploader file

	Uploads files to rapidshare.com

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  --collector           sets the login type as collector
	  --premium             sets the login type as premium
	  -u USERNAME, --username=USERNAME
		                sets the username
	  -p PASSWORD, --password=PASSWORD
		                sets the password
	  --disable-hashing     disables hashing done while uploading
	  --chunk-size=CHUNK_SIZE
		                set the chunk size to read and upload at (bytes)
	  -c, --cpu             returns the API CPU value for your IP address


Examples
------------

Create a random 100MB file to test uploading with, `dd if=/dev/zero of=test.bin bs=100M count=1`.

To upload without an account, `uploader test.bin`.

To upload as a collector, `uploader --collector -u username -p password test.bin`.

To upload as a premium user, `uploader --premium -u username -p password test.bin`.

