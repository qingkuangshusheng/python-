#coding:utf-8
import url_manager, html_downLoader, html_parser, html_outputer
import robotparser

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.Url_Manager()
        self.downloader = html_downLoader.HtmlDownLoader()
        self.parser = html_parser.HtmlParser()
        self.outper = html_outputer.OutPuter()
    def craw_isrunning(self,new_url):
         html_cont = self.downloader.dowmload(new_url)
         new_urls, new_data = self.parser.parse(new_url, html_cont)
         # for seturl in new_urls:
         # print 'seturl:%s'%(seturl)
         self.urls.add_new_urls(new_urls)
         self.outper.collect_data(new_data)

    def craw(self, rool_url):
        count = 1
        self.urls.add_new_url(rool_url)
        throttle=self.downloader.Throttle(5)
        rp=robotparser.RobotFileParser()
        rp.set_url('https://baike.baidu.com/robots.txt')
        rp.read()
        user_agent='wswp'
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print u'第%d个页面%s'%(count,new_url)
                if rp.can_fetch(user_agent,new_url):
                    throttle.wait(new_url)
                    self.craw_isrunning(new_url)
                    if count == 100:
                        break
                    count = count + 1
                else:
                     print 'Blocked by robots.txt',new_url
            except:
                print 'craw failed'
        self.outper.output_html()
        # for oldurl in self.urls.old_urls:
        #     print 'oldurl%s:' % (oldurl)
        # for newurl in self.urls.new_urls:
        #     print 'newurl%s:' % (newurl)

if __name__ == '__main__':
    rool_url = 'http://baike.baidu.com/link?url=zPYR4ecR3IG55pGlXy1IRihmzanIwAxk6dzewkmpNUlVHOO-3k4G7MKrPhzasxjbBz07fHcCbciHjNeOFI_hq_'
    obj_spider = SpiderMain()
    obj_spider.craw(rool_url)
