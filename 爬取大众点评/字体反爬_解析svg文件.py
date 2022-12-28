from lxml import etree
import re
class parse_svg:
    def __init__(self,svg_file,css_file):
        self.svg_file=svg_file
        self.css_file=css_file
    #解析svg文件
    def process_svg(self):
        tree = etree.ElementTree(file=self.svg_file)  # 保证每次操作均为原始model文件
        root = tree.getroot()  # 获取根元素
        elems = root.findall('{http://www.w3.org/2000/svg}text')
        dic={}
        for elem in elems:
            #print(elem.text)
            address = -int(elem.attrib['y']) + 23
            #print(address)
            for i in range(len(elem.text)):
                dic[(i,address)]=elem.text[i]
        return dic


    #结息css文件
    def process_css(self):
        with open(self.css_file, 'r', encoding='utf-8') as f:
            file_data = f.read()
            # print(file_data)
            data_list = re.findall('(\w{5})({background:)(.*?)(;})', file_data, re.S)
            dic = {}
            for data in data_list:
                data = list(data)
                data[2] = data[2].replace('px', '').replace('.0', '')
                dic[data[0]] = tuple(map(int, data[2].split(' ')))
        return dic
    #转换字典
    def process_css1(self,dic_rep1):
        dic={}
        for k,v in dic_rep1.items():
            v=list(v)
            v[0]=int(-v[0]/14+1)
            dic[k]=tuple(v)
        return dic

    #得到替换的字典
    def final_result(self,dic_rep,dic_rep1):
        #dic_rep = a.process_svg()
        # print(dic_rep)
        # print(len(dic_rep))
        # print(dic_rep1)
        dic_rep11 = self.process_css1(dic_rep1)
        # print(dic_rep11)
        # print(len(dic_rep11))
        final_dic = {}
        for k, v in dic_rep11.items():
            try:
                final_dic[k] = dic_rep[v]
            except:
                pass

        return final_dic

    def main(self):
        dic_rep=self.process_svg()
        dic_rep1=self.process_css()
        final_dic=self.final_result(dic_rep,dic_rep1)
        return final_dic

if __name__=="__main__":
    a = parse_svg('tupian.svg', 'replace.css')
    final_dic = a.main()
    print(final_dic)


