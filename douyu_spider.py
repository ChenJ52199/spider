from selenium import webdriver
import time


class DouyuSpider(object):
    '''斗鱼房间信息'''

    def __init__(self):
        self.start_url = 'https://www.douyu.com/directory/all'
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        # self.driver.implicitly_wait(20)

    def get_content_list(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@class='layout-Cover-list']/li")
        content_list = list()
        for li in li_list:
            item = dict()
            item['room_title'] = li.find_element_by_xpath(".//h3[@class='DyListCover-intro']").get_attribute("title")
            item['room_author'] = li.find_element_by_xpath('.//div[@class="DyListCover-userName"]').text
            item['room_hot'] = li.find_element_by_xpath('./div/a//span[@class="DyListCover-hot"]').text
            print('room_title:%s\troom_author:%s\troom_hot:%s' % (
            item['room_title'], item['room_author'], item['room_hot']))
            content_list.append(item)
        next_url = self.driver.find_elements_by_xpath("//div[@class='ListFooter']/ul/li[last()]")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content_list(self, content_list):
        with open('douyu_data.txt', 'a') as f:
            for item in content_list:
                f.write('room_title:%s\troom_author:%s\troom_hot:%s\n' % (
                item['room_title'], item['room_author'], item['room_hot']))

    def run(self):  # 实现主要逻辑
        # 1.获取start_url
        # 2.发送请求获取响应
        self.driver.get(self.start_url)
        time.sleep(10)
        # 3.提取网页数据, 获取next_url
        content_list, next_url = self.get_content_list()
        # 4.保存数据
        self.save_content_list(content_list)
        while next_url:
            next_url.click()
            # time.sleep(10)
            # 提取网页数据, 获取next_url
            content_list, next_url = self.get_content_list()
            # 保存数据
            self.save_content_list(content_list)


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()
