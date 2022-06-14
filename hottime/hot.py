import requests
from lxml import etree
from urllib.parse import urljoin
import re, csv


class Crawl_WeiBo_SINA:

    def __init__(self) -> None:
        self.header = {
            'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding':
            'gzip, deflate, br',
            'accept-language':
            'zh-CN,zh;q=0.9',
            'cache-control':
            'max-age=0',
            'cookie':
            'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Wh8Na4iaYJB.OpTXovmMSy7; _s_tentry=passport.weibo.com; Apache=6567708276034.916.1655124708234; SINAGLOBAL=6567708276034.916.1655124708234; ULV=1655124708253:1:1:1:6567708276034.916.1655124708234:; SUB=_2AkMV-7u0f8NxqwJRmP0Sym_qaox0zA_EieKjp0pvJRMxHRl-yj8XqmAntRB6PnuVWwOefnC4aSsxEkxNccDie6o_ysLc',
            'referer':
            'https://s.weibo.com/top/summary?cate=total&key=friends',
            'sec-ch-ua-mobile':
            '?0',
            'sec-ch-ua-platform':
            "Windows",
            'sec-fetch-dest':
            'document',
            'sec-fetch-mode':
            'navigate',
            'sec-fetch-site':
            'same-origin',
            'sec-fetch-user':
            '?1',
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        }

    def qingqiu(self, hot_url):
        response = requests.get(hot_url, headers=self.header)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
        else:
            print(response.status_code)
            return None

    def html_parse(self, html, hot_url):
        selector = etree.HTML(html)
        tbody_trs = selector.xpath(
            '//div[@id="pl_top_realtimehot"]/table/tbody/tr')
        if len(tbody_trs) > 0:
            titles = tbody_trs[0].xpath('//td[2]/a/text()')
            urls = tbody_trs[0].xpath('//td[2]/a/@href')
            urls = [urljoin(hot_url, url) for url in urls]
            return urls

    def new_parse(self, html):
        selector = etree.HTML(html)
        pl_feedlist_index = selector.xpath('//div[@id="pl_feedlist_index"]')
        if pl_feedlist_index:
            topic_header = pl_feedlist_index[0].xpath(
                '//div[@class="title"]/h1[@class="short"]/a//text()')
            summary = selector.xpath(
                '//*[@id="pl_feedlist_index"]/div[2]/div//text()')
            huati_zhuchiren = selector.xpath(
                '//*[@id="pl_right_side"]/div[1]/div/div[2]/div/div[2]/div/a//text()'
            )
            read_numbers = selector.xpath(
                '//*[@id="pl_topic_header"]/div[1]/div[2]/div/div[2]/span[1]//text()'
            )
            task_numbers = selector.xpath(
                '//*[@id="pl_topic_header"]/div[1]/div[2]/div/div[2]/span[2]//text()'
            )
            desc_url = selector.xpath(
                '//*[@id="pl_topic_header"]/div[1]/div[2]/div/div[2]/a/@href')
            if summary:
                summary = ''.join(summary).replace(' ', '').replace('\n', '')
            else:
                summary = ""
            if huati_zhuchiren:
                huati_zhuchiren = ''.join(huati_zhuchiren).strip()
            else:
                huati_zhuchiren = ""
            if read_numbers:
                read_numbers = ''.join(read_numbers)
                num = re.findall("\d+\.\d+", read_numbers)
                if num:
                    num = float(''.join(num))
                else:
                    num = 0
                if "万" in read_numbers:
                    read_numbers = num * 10000
                elif "亿" in read_numbers:
                    read_numbers = num * 100000000
            if task_numbers:
                task_numbers = ''.join(task_numbers)
                num = re.findall("\d+\.?\d+", task_numbers)
                if num:
                    num = float(''.join(num))
                else:
                    num = 0
                if "万" in task_numbers:
                    task_numbers = num * 10000
                elif "亿" in task_numbers:
                    task_numbers = num * 100000000
                else:
                    task_numbers = num
            if desc_url:
                desc_url = ''.join(desc_url)

            hot_info = {
                "title": topic_header[0] if topic_header else "",
                "summary": summary,
                "huati_zhuchiren": huati_zhuchiren,
                "read_numbers": int(read_numbers),
                "task_numbers": int(task_numbers),
                "desc_url": desc_url
            }
            return hot_info
            


def write_csv(datas, filename):

    with open(filename, 'a', encoding='utf-8', newline='') as csv_hander:
        fields = [
            "title", "summary", "huati_zhuchiren", "read_numbers",
            "task_numbers", "desc_url"
        ]
        writer = csv.DictWriter(csv_hander, fieldnames=fields)
        writer.writeheader()
       
        writer.writerows(datas)



def main():
    hot_url = "https://s.weibo.com/top/summary?cate=realtimehot"
    sina = Crawl_WeiBo_SINA()
    htmlobj = sina.qingqiu(hot_url)
    new_urls = sina.html_parse(htmlobj, hot_url)
    datas = []
    for new in new_urls:
        try:
            new_html = sina.qingqiu(new)
            data = sina.new_parse(new_html)
            datas.append(data)
        except Exception as e:
            print('new', e, new)
            continue
    write_csv(datas, './sina_hot.csv')
    print("==== Done ====")


if __name__ == "__main__":
    main()
