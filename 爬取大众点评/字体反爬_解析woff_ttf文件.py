from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr
from fontTools.ttLib import TTFont


class parse_woff_ttf(object):
    def __init__(self,*filename_list):
        self.filename_list=filename_list
    def font_to_img(self,txt, filename):
        """
        将字体画成图片
        :param txt:
        :param filename:字体文件
        :return:
        """
        img_size = 1024
        img = Image.new('1', (img_size, img_size), 255)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(filename, int(img_size * 0.7))
        txt = chr(txt)
        x, y = draw.textsize(txt, font=font)
        draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
        return img
    def font_analysis(self,filename):
        """
        传入字体文件名称就能直接出来映射对照
        :param filename:字体文件名称
        :return:返回识别结果
        """
        # 存储识别结果的字典
        analysis_res = {}
        # 加载字体文件
        font_file = TTFont(filename)
        ocr = ddddocr.DdddOcr()
        for i, Glyph_name in font_file.getBestCmap().items():
            # 将字体文件转成图片
            pil = self.font_to_img(i, filename)
            bytes_io = BytesIO()
            pil.save(bytes_io, format="PNG")
            # 使用ddddocr进行识别
            res = ocr.classification(bytes_io.getvalue())
            # print(res)
            # analysis_res的key位置是放Glyph_name还是i 需要测试一下
            # 比如 闪职用的是i
            # 汽车之家用的是Glyph_name
            # analysis_res[i] = res
            analysis_res[Glyph_name] = res
        return analysis_res
    # 合并得到的替换字典
    def merge(self,dic1, dic2):
        return dic2.update(dic1)

    def main(self):
        rep_list=[]
        #print(self.filename_list)
        for filename in self.filename_list:
            #print(filename)
            rep_dic=self.font_analysis(filename)
            rep_list.append(rep_dic)
        for i in range(len(rep_list)):
            if i == len(rep_list)-1:
                break
            self.merge(rep_list[i],rep_list[i+1])
        return rep_list[-1]

if __name__=="__main__":
    a=parse_woff_ttf('字体1.woff','字体2.woff','字体3.woff')
    print(a.main())


