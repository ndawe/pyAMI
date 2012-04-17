import os, socket
from urlparse import urlparse
from httplib import HTTPConnection, HTTPSConnection


class AMIHTTPConnection(HTTPConnection):

    def __init__(self, host, port=None, strict=None, **kwargs):

        self.proxy_host = None
        self.proxy_port = None
        if os.environ.has_key('http_proxy'):
            o = urlparse(os.environ['http_proxy'])
            try:
                self.proxy_host, self.proxy_port = o[1].split(':')
            except:
                pass
        HTTPConnection.__init__(self, host=host,
                                      port=port,
                                      strict=strict,
                                      **kwargs)

    def connect(self):

        if not (self.proxy_host and self.proxy_port):
            HTTPConnection.connect(self)
        else:
            msg = "getaddrinfo returns an empty list"
            for res in socket.getaddrinfo(self.proxy_host, self.proxy_port, 0,
                                        socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self.sock = socket.socket(af, socktype, proto)
                    if self.debuglevel > 0:
                        print "connect: (%s, %s)" % (self.proxy_host, self.proxy_port)
                    self.sock.connect(sa)
                except socket.error, msg:
                    if self.debuglevel > 0:
                        print 'connect fail:', (self.proxy_host, self.proxy_port)
                    if self.sock:
                        self.sock.close()
                    self.sock = None
                    continue
                break
            if not self.sock:
                raise socket.error, msg

    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        """
        Recover the full URL path together with host
        """
        full_url = url
        urlPref = "http://"
        if not url.startswith(urlPref):
            full_url = '%s%s:%s%s' % (urlPref, self.host, self.port, url)
        HTTPConnection.putrequest(self, method, full_url, skip_host, skip_accept_encoding)


class AMIHTTPSConnection(HTTPSConnection):

    def __init__(self, host, port=None, strict=None, **kwargs):

        self.proxy_host = None
        self.proxy_port = None
        if os.environ.has_key('https_proxy'):
            o = urlparse(os.environ['https_proxy'])
            try:
                self.proxy_host, self.proxy_port = o[1].split(':')
            except:
                pass
        HTTPSConnection.__init__(self, host=host,
                                       port=port,
                                       strict=strict,
                                       **kwargs)

    def connect(self):

        if not (self.proxy_host and self.proxy_port):
            HTTPSConnection.connect(self)
        else:
            msg = "getaddrinfo returns an empty list"
            for res in socket.getaddrinfo(self.proxy_host, self.proxy_port, 0,
                                    socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self.sock = socket.socket(af, socktype, proto)
                    if self.debuglevel > 0:
                        print "connect: (%s, %s)" % (self.proxy_host, self.proxy_port)
                    self.sock.connect(sa)
                except socket.error, msg:
                    if self.debuglevel > 0:
                        print 'connect fail:', (self.proxy_host, self.proxy_port)
                    if self.sock:
                        self.sock.close()
                    self.sock = None
                    continue
                break
            if not self.sock:
                raise socket.error, msg

    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        """
        Recover the full URL path together with host
        """
        full_url = url
        urlPref = "https://"
        if not url.startswith(urlPref):
            full_url = '%s%s:%s%s' % (urlPref, self.host, self.port, url)
        HTTPSConnection.putrequest(self, method, full_url, skip_host, skip_accept_encoding)
