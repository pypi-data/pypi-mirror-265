#! /usr/bin/env python

import os
import re
import html
from html.parser import HTMLParser
import sys
import argparse
import datetime
import subprocess
import urllib.request
from functools import partial

class EDGARLatest10K():

    def __init__(self, odir=None):
        self.sprefix = 'https://www.sec.gov/Archives/edgar/full-index'
        self.rprefix = 'https://www.sec.gov/Archives'
        if 'EQEMAIL' in os.environ:
            self.hdr     = {'User-Agent' : os.environ['EQEMAIL'] }
        else:
            print('EQEMAIL environmental variable must be set to a valid \
                   HTTP User-Agent value such as an email address')
        self.now     = datetime.datetime.now()
        self.cik     = None
        self.link    = True
        if odir: self.odir = odir
        elif os.environ['EQODIR']: self.odir = os.environ['EQODIR']
        else: self.odir = '/tmp'
        self.odir = os.path.abspath(self.odir)
        self.chunksize =4294967296

    def query(self, url=None):
        """query - query an EDGAR URL
         url  - EDGAR URL to query - required 
         not yet implemented
        """
        try:
            req = urllib.request.Request(url, headers=self.hdr)
            resp = urllib.request.urlopen(req)
            return resp
        except urllib.error.URLError as e:
            print("Error %s(%s): %s" % ('query', url, e.reason),
            file=sys.stderr )
            sys.exit(1)

    def storequery(self, qresp, tf):
        """storequery - store the query response in a file \
        resp - the query response \
        tf   - filename that will hold the query response
        """
        if not qresp:
            print('storequery: no content', file=sys.stderr)
            sys.exit(1)
        if not tf:
            print('storequery: no output filename', file=sys.stderr)
            sys.exit(1)
        of = os.path.abspath(tf)
        # some downloads can be somewhat large
        with open(of, 'wb') as f:
            parts = iter(partial(qresp.read, self.chunksize), b'')
            for c in parts:
                f.write(c)
            #if c: f.write(c)
            f.flush()
            os.fsync(f.fileno() )
            return

    def pgrep(self, pat=None, fn=None):
        """ pgrep - simulate grap when command does not exist
        """
        if not fn and not pat:
            print('pgrep pat and fn required')
            sys.exit(1)
        rc = re.compile(pat)
        with open(fn, 'r') as f:
            for line in f:
                if rc.search(line):
                    return line

    def dogrep(self, cik=None, fn=None):
        """ dpgrep - desparately try to grep for something
        """
        if not fn and not cik:
            print('dogrep: fn and cik required')
            sys.exit(1)
        cmd=None
        pat = '10-K.* %s ' % cik
        if os.path.exists(os.path.join('/', 'bin', 'grep') ):
            cmd = os.path.join('bin', 'grep')
        elif os.path.exists(os.path.join('/', 'usr', 'bin', 'grep') ):
            cmd = os.path.join('/', 'usr', 'bin', 'grep')

        if cmd:
            try:
                sp = subprocess.Popen([cmd, pat, fn],
                       bufsize=-1, stdout=subprocess.PIPE)
                so, se = sp.communicate()
                if so:
                    out = so.decode('utf-8')
                    htm = '%s/%s-index.htm' % (self.rprefix,
                           out.split()[-1].split('.')[0] )
                    # print(htm)
                    return htm
                if se:
                    err = se.decode('utf-8')
                    print(err)
                    sys.exit(1)
                os.unlink(fn)
            except Exception as e:
                print('grep url: %s' % (e), file=sys.stderr)
                sys.exit(1)
        else:
            res = self.pgrep(pat, fn)
            return res

    def get10kfromhtml(self, url, link):
        """parse the html table to find relative link to 10-K html file
           complete the url and either return it or
           store the 10-k html file
        """
        resp = self.query(url)
        rstr    = resp.read().decode('utf-8')
        # print(rstr)
        class MyHTMLParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'a':
                    if 'ix?doc' in attrs[0][1]:
                        tkurl =  '%s%s' % ('https://www.sec.gov',
                             attrs[0][1].split('=')[1])
                        self.data = tkurl
                        print(tkurl)
            def handle_endtag(self, tag):
                pass
            def handle_data(self, data):
                pass
        parser = MyHTMLParser()
        parser.feed(rstr)
        tkurl = parser.data
        if not link:
            tkresp = self.query(tkurl)
            ofn = os.path.join(self.odir, 'CIK%s.10-K.htm' % (self.cik.zfill(10) ) )
            self.storequery(tkresp, ofn)

    def gensearchurls(self):
        """ gensearchurls - 10-k files are published once a year or so
            and can be published on a schedule controlled by the company
            return a set of links to form files where the 10-K link
            may reside
        """
        surla = []
        yr = self.now.year
        mo = self.now.month
        if mo <=3:
            surla.append('%s/%d/QTR1/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR2/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR3/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR4/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR1/form.idx' % (self.sprefix, yr) )
        elif mo <=6:
            surla.append('%s/%d/QTR2/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR3/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR4/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR1/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR2/form.idx' % (self.sprefix, yr) )
        elif mo <=9:
            surla.append('%s/%d/QTR3/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR4/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR1/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR2/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR3/form.idx' % (self.sprefix, yr) )
        else:
            surla.append('%s/%d/QTR4/form.idx' % (self.sprefix, yr-1) )
            surla.append('%s/%d/QTR1/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR2/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR3/form.idx' % (self.sprefix, yr) )
            surla.append('%s/%d/QTR4/form.idx' % (self.sprefix, yr) )
        return surla

    def search10K(self, cik, link):
        """ search10K - search in the form.idx files for a page that
            contains a link to the 10-k for a cik
            cik - central index key, required
            link - if true, just return a url link to the 10-K html page
                   if false, store the html page
        """
        surla = self.gensearchurls()
        ofn   = os.path.join(self.odir, 'form.idx')
        tktbl = None
        for url in surla:
            resp = self.query(url)
            self.storequery(resp, tf=ofn)
            res = self.dogrep(cik, ofn)
            if res:
                tktbl = res
        if tktbl:
            self.get10kfromhtml(tktbl, link)

def main():
    LT = EDGARLatest10K()

    argp = argparse.ArgumentParser(
              description='find the most recent 10-K for cik')
    argp.add_argument("--cik", required=True,
        help="10-digit Central Index Key")
    argp.add_argument("--link",
          action='store_true', default=False,
          help="return the url for the latest 10-K")

    args = argp.parse_args()

    LT.cik = args.cik
    LT.search10K(args.cik, link=args.link)

main()
