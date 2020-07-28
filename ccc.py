import requests
from bs4 import BeautifulSoup
import bs4
import os
import datetime
import sys
#---------------------------------------------------------------------
kv = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    # 伪造设备信息，必须的
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  # 接收类型
    'DNT': '1',  # 防追踪
    'referer': "http://archive.nyafuu.org/e/gallery/"}

#---------------------------------------------------------------------

def save_file(rod, url):  # 保存文件函数(文件夹路径，封面图片路径)
    try:
        path = rod + '//' + url.split('/')[-1]  # 文件保存路径,获取文件名 -- XXX.png
        if not os.path.exists(rod):  # 判断该路径文件是否存在
            os.makedirs(rod)  # 不存在就创建该文件夹
        if not os.path.exists(path):  # 判断文件是否已经下载过
            r = requests.get(url, headers=kv, timeout=30)  # 爬取网上内容
            with open(path, 'wb') as f:
                f.write(r.content)
                print('文件下载成功')
                inputfile('文件下载成功')
        else:
            print('该文件已存在')
            inputfile('该文件已存在')
    except:
        print('爬取失败')
        inputfile('爬取失败')
# ---------------------------------------------------------------------

def getHMTlText(url):  # 将URL信息从网络上爬取下来
    try:
        r = requests.get(url, headers=kv, timeout=30)  # timeout 链接超时时间我设定是30 你们可以自己改
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''
#---------------------------------------------------------------------

def gir_deef_supe(path, urls):  #图片组路径下的所有图片，有个bug,但我们不进行save_file操作时，会出现循环找重复img的情况，
    try:
        html=getHMTlText(urls)
        soup = BeautifulSoup(html, 'html.parser')  # 熬一锅汤,解析从网上爬取的内容
        count=0  #要下载的图片数量
        for tr in soup.find(id='main').descendants:  # 把解析内容里的 ID = 'pins'的内容遍历出来,descendants是找了子标签，然后再一步步探入别人的家中，把一个个后代，按辈分由大往小找着。
            if isinstance(tr, bs4.element.Tag):  # 判断tr  = Tag标签，根据id元素来找时，应该这样判断
                for retn_a in tr.find_all('a'):
                    for retn_img in retn_a.find_all('img'):  # 找到 'A' 标签里的'img'标签
                        top_img_the_link = retn_a.get('href')  # 找到 'A' 的href，即高清图片的url，注意这里不是从img中找到的
                        newpath = path + '//' + top_img_the_link.split('/')[-1]  # 文件保存路径,获取文件名 -- XXX.png
                        if not os.path.exists(newpath):  # 判断文件是否已经下载过
                            count = count + 1
                            print("该图片组中的高清图片路径 " + str(count) + ":" + top_img_the_link)
                            inputfile("该图片组中的高清图片路径 " + str(count) + ":" + top_img_the_link)
                            save_file(path, top_img_the_link)
                        else:  #已存在，跳出循环，为了浪费资源
                            break
        print("下载总量;"+str(count))
        print('\n')
        inputfile("下载总量;"+str(count)+"\n")
    except:
        inputfile('未知错误！')
        return '未知错误！'
#---------------------------------------------------------------------
def fillUniucList(html,pagenum,thistitlenum,startDowGroup):  # 取出组
    try:
        soup = BeautifulSoup(html, 'html.parser')  # html.parser：html解析器
        for tr in soup.find(id='thread_o_matic').descendants:  # 把解析内容里的 ID = 'pins'的内容遍历出来,descendants是找了子标签，然后再一步步探入别人的家中，把一个个后代，按辈分由大往小找着。
            if isinstance(tr, bs4.element.Tag):  # 判断tr  = Tag标签，根据id元素来找时，应该这样判断
                for td in tr.find_all('a'):  # 找到'A'标签
                    for thx in tr.find_all('h2'):  # 找到'h2'标签
                        break
                    for tds in td.find_all('img'):  # 找到 'A' 标签里的'img'标签
                        if(thistitlenum<startDowGroup):  #现在下载的小于我要求开始下载的,不下载
                            thistitlenum=thistitlenum+1
                            break
                        else:
                            newgrouptitle = title_rename(thx.get_text())  # 获取标题中的文本，然后对文本中的特殊字符进行替换
                            if len(newgrouptitle) > 0:
                                path = 'd://图片//' + "页面" + str(
                                    pagenum) + "-标题[" + newgrouptitle + "]"  # 创建文件夹路径,这样只要修改下载的页面就可以实现下载新的图片，不会漏掉
                            else:
                                path = 'd://图片//' + "页面" + str(pagenum) + "-标题[" + str(thistitlenum) + "]"

                            print("当前下载标题[" + str(thistitlenum) + "]：" + newgrouptitle)
                            inputfile("当前下载标题[" + str(thistitlenum) + "]：" + newgrouptitle)

                            urls = td.get('href')  # 找到 'A' 的href
                            print("下载图组网络路径[" + str(thistitlenum) + "]：" + urls)
                            print("下载图组本地路径[" + str(thistitlenum) + "]：" + path)
                            inputfile("下载图组网络路径[" + str(thistitlenum) + "]：" + urls
                                      +"\n"+
                                      "下载图组本地路径[" + str(thistitlenum) + "]：" + path)

                            thistitlenum = thistitlenum + 1
                            urlimg = tds.get('src')  # 获取显示的封面路径

                            print("模糊封面图片网络路径：" + urlimg)
                            inputfile("模糊封面图片网络路径：" + urlimg)

                            gir_deef_supe(path, urls)
                    break;

    except:
        inputfile('未知错误！')
        return
#---------------------------------------------------------------------
def title_rename(title):  #为了使文件夹命名规范
    newtitle=title.replace('\\',' ').replace('/', ' ').replace(':', ' ').replace('*', ' ').replace('?', ' ').replace('"', ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ');
    return newtitle.strip()
#---------------------------------------------------------------------
def inputfile(thestr):  #写入文件日志数据
    if os.path.exists("D:\\图片\\1.txt"):  # 文件7存在
        f = open("D:\\图片\\1.txt", "a+")
        f.write("\n"+thestr)
        f.close()
    else:
        f = open("D:\\图片\\1.txt", "w+")
        f.write("\n"+thestr)
        f.close()
#---------------------------------------------------------------------
def main():  # 主函数，这个可以实现动态更新后的下载，避免重复下载，但是难去确认下载到了那一个图片组,但可以对开始下载的地方进行指定,同时也添加了写入日志文件的功能
    pagenum = 1
    while 1 > 0:
        num = input("请输入开始的位置 1~n :")
        if num.replace(".", '').isdigit():
            if num == '0':
                print("输入数值要>=1")
            elif num.count(".") == 1:
                print("输入数值要为int类型")
            elif num.count(".") == 0:
                break
        else:
            print("请输入int类型：")

    print("即将从图组【" + num + "】开始下载...")
    inputfile("即将从图组【" + num + "】开始下载...")

    startDowGroup = int(num)
    while pagenum <= 240:   #页面分页管理，分240页,实现240页的跳转
        url = 'http://archive.nyafuu.org/e/gallery/'+str(pagenum)
        html = getHMTlText(url)
        thistitlenum = 1  # 标题号变回初值
        fillUniucList(html,pagenum,thistitlenum,startDowGroup)
        startDowGroup = 1
        pagenum += 1
#---------------------------------------------------------------------
main()
