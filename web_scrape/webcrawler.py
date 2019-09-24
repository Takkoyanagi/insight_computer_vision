from icrawler.builtin import BingImageCrawler, BaiduImageCrawler #0.6.2

# load the list of categories to download
labels = [labels.rstrip('\n') for labels in open('key_words_updated.txt')]

# download images from Bing
for i in labels:
    bing_crawler = BingImageCrawler(downloader_threads=4,
                               storage={'root_dir':i})
    bing_crawler.crawl(keyword=i, max_num=1000)

# download images from baidu
for i in labels:
    baidu_crawler = BaiduImageCrawler(storage={'root_dir':i+str(1)})
    baidu_crawler.crawl(keyword=i, max_num=1000)