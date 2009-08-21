# -*- coding: utf-8 -*-
import urllib
import socket
import os
import re
import hashlib

class Rapidshare:
	"""
	API to upload and access information on Rapidshare.com
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
		self.enable_hashing = True

	def upload(self, filename):
		self.filename = filename
		self.hash = None
		if not os.path.exists(self.filename):
			return False
		self.length = os.path.getsize(self.filename)

		params = urllib.urlencode({'sub': 'nextuploadserver_v1'})
		f = urllib.urlopen("http://www.rapidshare.com/cgi-bin/rsapi.cgi?%s" % params)
		userver = re.search('\d+', f.read())
		userver = userver.group().lstrip()
		self.server = "rs%s.rapidshare.com" % (userver)

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.server, 80))

		D = []
		CRLF = '\r\n'
		BOUNDARY = '---------------------632865735RS4EVER5675865'
		D.append(BOUNDARY)
		D.append('Content-Disposition: form-data; name="rsapi_v1"')
		D.append('')
		D.append('1')

		if self.collector:
			D.append(BOUNDARY)
			D.append('Content-Disposition: form-data; name="freeaccountid"')
			D.append('')
			D.append(self.username)
			D.append(BOUNDARY)
			D.append('Content-Disposition: form-data; name="password"')
			D.append('')
			D.append(self.password)

		if self.premium:
			D.append(BOUNDARY)
			D.append('Content-Disposition: form-data; name="login"')
			D.append('')
			D.append(self.username)
			D.append(BOUNDARY)
			D.append('Content-Disposition: form-data; name="password"')
			D.append('')
			D.append(self.password)

		D.append(BOUNDARY)
		D.append('Content-Disposition: form-data; name="filecontent"; filename="%s"' % (self.filename))
		D.append('')
		D.append('')
		disposition_start = CRLF.join(D)
		
		E = []
		E.append('')
		E.append(BOUNDARY + "--")
		E.append('')
		disposition_end = CRLF.join(E)

		content_length = len(disposition_start) + self.length + len(disposition_end)

		H = []
		H.append('POST /cgi-bin/upload.cgi HTTP/1.0')
		H.append('Content-Type: multipart/form-data; boundary=%s' % (BOUNDARY))
		H.append('Content-Length: %s' % (str(content_length)))
		H.append('')
		H.append(disposition_start)
		headers = CRLF.join(H)

		s.send(headers)

		if self.enable_hashing:
			m = hashlib.md5()
		fd = open(self.filename, 'rb')
		
		d = fd.read(self.chunk)
		while d:
			if self.enable_hashing:
				m.update(d)
			s.send(d)

			d = fd.read(self.chunk)

		if self.enable_hashing:
			m.update(d)
		s.send(d)
		s.send(disposition_end)
		fd.close()

		if self.enable_hashing:
			self.hash = m.hexdigest().upper()

		result = s.recv(self.chunk)
		s.close()

		r = []
		for match in re.finditer('File1.(\d+)=(.+)', result):
			r.append(match.group(2))
		return r

	@staticmethod
	def cpu():
		params = urllib.urlencode({'sub': 'getapicpu_v1'})
		fd = urllib.urlopen("http://www.rapidshare.com/cgi-bin/rsapi.cgi?%s" % params)
		return fd.read()
