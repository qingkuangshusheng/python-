#coding:utf-8
import urllib2
import urlparse
import time
import datetime

class HtmlDownLoader(object):
    #增强版下载功能，增加了网络代理，错误重试功能
    def downLoad(self,url,user_agent='wswp',proxy=None,num=5):
        if url is None:
            return None
        print 'DownLoading',url
        headers={'User-agent':user_agent}
        request=urllib2.Request(url,headers=headers)
        opener=urllib2.build_opener()
        if proxy:
            proxy_params={urlparse.urlparse(url).scheme:proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            html=opener.open(request).read()
        except urllib2.URLError,e:
            print 'DownLoading error:',e.reason
            html=None
            if num>0:
                if hasattr(e,'code') and 500<=e.code<600:
                    return self.downLoad(url,user_agent,num-1)
        return html
    #添加延时下载功能
    class Throttle:
        def __init__(self,delay):
            self.delay=delay
            self.domains={}
        def wait(self,url):
            domain=urlparse.urlparse(url).netloc
            last_accessed=self.domains.get(domain)
            if self.delay>0 and last_accessed is not None:
                sleep_secs=self.delay-(datetime.datetime.now()-last_accessed).seconds
                if sleep_secs>0:
                    time.sleep(sleep_secs)
            self.domains[domain]=datetime.datetime.now()