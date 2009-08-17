# -*- coding: utf-8 -*-
import urllib, socket
import os, sys, re, hashlib

class rapidshare:
	def __init__(self):
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
		f = open(self.filename, 'rb')
		
		d = f.read(self.chunk)
		while d:
			if self.enable_hashing:
				m.update(d)
			s.send(d)

			d = f.read(self.chunk)

		if self.enable_hashing:
			m.update(d)
		s.send(d)
		s.send(disposition_end)
		f.close()

		if self.enable_hashing:
			self.hash = m.hexdigest().upper()

		result = s.recv(self.chunk)
		s.close()

		serverhash = re.search('File1.4=(\w+)', result)
		if (not self.enable_hashing) or (serverhash.group(1) == self.hash):
			print "md5 hash [%s] [valid]" % (self.hash)
			upload = re.search('File1.1=(\S+)', result)
			delete = re.search('File1.2=(\S+)', result)
			print "url [%s]" % (upload.group(1))
			print "del [%s]" % (delete.group(1))

	@staticmethod
	def cpu():
		params = urllib.urlencode({'sub': 'getapicpu_v1'})
		f = urllib.urlopen("http://www.rapidshare.com/cgi-bin/rsapi.cgi?%s" % params)
		return f.read()
