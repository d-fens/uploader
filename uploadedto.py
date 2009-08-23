# -*- coding: utf-8 -*-
"""
Nodule for uploaded.to API
"""
import urllib
import socket
import os
import re
import random
import time

class Uploadedto:
	"""
	API to upload and access information on uploaded.to
	"""

	def __init__(self):
		self.filename = None
		self.username = None
		self.password = None
		self.collector = False
		self.premium = False
		self.length = 0
		self.chunk = (1024 * 64)
		self.server = None
		self.hash = None
		self.enable_hashing = False

	def upload(self, filename):
		"""
		This is different to the rapidshare.com code as the server 
		returned is in the format http://hostname

		Also the boundary for some reason is more specific for the
		uploaded.to server (eg RFC) than rapidshare is.
		"""
		self.filename = filename
		self.hash = None
		if not os.path.exists(self.filename):
			return False
		self.length = os.path.getsize(self.filename)

		f = urllib.urlopen("http://www.uploaded.to/api/uploadserver")
		self.server = f.read()[7:-1]

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.server, 80))

		D = []
		CRLF = '\r\n'
		BOUNDARY = '----------------------------be8d82fc9b3b'

		D.append("--" + BOUNDARY)
		D.append('Content-Disposition: form-data; name="file1x"; filename="%s"' % (self.filename))
		D.append('Content-Type: application/octet-stream')
		D.append('')
		D.append('')
		disposition_start = CRLF.join(D)
		
		E = []
		E.append('')
		E.append("--" + BOUNDARY + "--")
		E.append('')
		disposition_end = CRLF.join(E)

		content_length = len(disposition_start) + self.length + len(disposition_end)

		# From their javascript UID
		uid = "%s0%s" % (int(10000*random.random()), int(10000*random.random()))

		H = []
		H.append('POST /up?upload_id=%s&output=csv HTTP/1.1' % (uid))
		H.append('Host: %s' % (self.server))
		H.append('Accept: */*')
		H.append('Content-Length: %s' % (str(content_length)))
		H.append('Expect: 100-continue')
		H.append('Content-Type: multipart/form-data; boundary=%s' % (BOUNDARY))
		H.append('')
		H.append('')

		# continue 100
		headers = CRLF.join(H)
		s.send(headers)
		# just to wait for the server to send a response
		time.sleep(0.25)

		if s.recv(self.chunk) != ("HTTP/1.1 100 Continue" + CRLF + CRLF):
			return

		H = []
		H.append(disposition_start)
		headers = CRLF.join(H)

		s.send(headers)

		fd = open(self.filename, 'rb')
		
		d = fd.read(self.chunk)
		while d:
			s.send(d)
			d = fd.read(self.chunk)

		s.send(d)
		s.send(disposition_end)

		fd.close()

		result = s.recv(self.chunk)
		s.close()
		
		# (id, size, delete, name)
		match = re.search('(?P<id>.+),(?P<size>.+),(?P<delete>.+),(?P<name>.+)', result)
		if match:
			url = "http://ul.to/%s" % (match.group('id').strip())
			size = int(match.group('size').strip())
			delete = "http://uploaded.to/?id=%s" % (match.group('delete').strip())
			name = match.group('name').strip()
			return (url, delete, size, name)
		else:
			return False
