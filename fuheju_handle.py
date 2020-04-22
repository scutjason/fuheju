# !/usr/bin/python3
# encoding: utf-8
# Time    : 2020/4/17 9:52 下午 
# Author  : scutjason
# File    : fuheju_handle.py

import re
import json
import os


'''中文复句整理及模板'''
class Extraction:
    def __init__(self):
        file_path = os.path.abspath(os.path.dirname(__file__))
        fr = open(os.path.join(file_path, 'word_syn/data/daozhuang_dict.json'), 'r')
        self.all_dict = json.load(fr)
        fr.close()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做维护标识'''
    def split_sents(self, content):
        return [sentence.replace('　','') for sentence in re.split(r'[？?！!。：:\n\r]', content) if sentence]

    '''连词'''
    def lianci(self, sent):
        # 怎么找到 和 字 左右两边的词。
        return sent.replace('和', '与')

    '''模式匹配'''
    def pattern_match(self, sent):
        '''
            对于句子进行模版匹配复合句式
        :param sent:
        :return:
        '''
        datas = {}
        max = 0
        replace_jushi = ''

        for pre_word in self.all_dict:
            for post_word in self.all_dict[pre_word]:
                p = re.compile(r'({0})(.+?)({1})([^？?！!。；;：:\n\r，,]*)'.format(pre_word, post_word))
                # 遍历每一个匹配模版
                ress = p.findall(sent)
                if ress:
                    for res in ress:
                        # print(ress)
                        len_res = len(res[0] + res[2])
                        if len_res > max:
                            replace_jushi = self.all_dict[pre_word][post_word]
                            # match条件最长的那个，更准确。
                            datas = {'pre_wd': res[0], 'pre_part': res[1], 'post_wd': res[2], 'post_part': res[3]}
                            max = len_res
        return replace_jushi, datas

    '''替换函数，抽取完之后进行'''
    def exchange(self, content):
        sents = self.split_sents(content)
        ret_sent = ''
        for sent in sents:
            replace_word, juzi_tuples = self.pattern_match(sent)
            print(replace_word, juzi_tuples)
            if replace_word == '':
                ret_sent += sent + '。'
                continue
            # 1、找到第一个词
            pre_wd = juzi_tuples['pre_wd']
            # post_wd = juzi_tuples['post_wd']
            post_part = juzi_tuples['post_part']
            old_sent = sent
            replace_pair = replace_word.split(' ')

            # 2、开始替换
            new_sent = ''
            pre_wd_id = old_sent.index(pre_wd)
            # print(pre_wd_id)
            new_sent += old_sent[:pre_wd_id]

            ws = replace_pair[0].split('_')
            if ws[0] != post_part[0] and ws[0] != 'space':
                new_sent += ws[0]
            new_sent += post_part
            if len(ws) == 2:
                new_sent += ws[1]
            if new_sent[-1] not in ',，、':
                new_sent += '，'
            new_sent += replace_pair[1]
            new_sent += juzi_tuples['pre_part']

            post_part_idx = old_sent.index(post_part) + len(post_part)
            if post_part_idx < len(sent):
                if old_sent[post_part_idx] == new_sent[-1]:
                    # 可能有两个都好
                    post_part_idx += 1
                new_sent += old_sent[post_part_idx:]
            if new_sent[-1] in ',，':
                new_sent = new_sent[:-1]
            ret_sent += new_sent + '。'

        return ret_sent


'''基于给定语料与模板的事件抽取'''
if __name__ == '__main__':
    extract = Extraction()
    s = "只有现代化的驱动经济管理才能够符合社会经济的发展需求，因此，经济管理与现代化不能分开，现代化的经济管理体系是国民经济发展的必要因素。"
    s = '中国人在共产党的带领下，才有出路，才有发展。'
    s = '就如毛泽东说的那样：一切反动派都是纸老虎。'
    s = '一方有难，八方支援，这就是团结的力量，也是在延安时代，我们学习总结出来的。'
    s = '我们与其去玩游戏，还不如花时间去学习新知识。'
    # s = '不管做任何事都要一鼓作气，不要打退堂鼓。'
    # s = '用户首先需要根据项目功能划分任务和中断、然后创建任务和中断子程序，CPU同时只能运行一个任务，但由于操作系统内核的调度，可以几乎达到同时执行多任务的效果。'
    # s = '对于经常网购的人来说，网购其中有一大特点就是能够货到付款，但是迄今为止，很多自助快递柜还没有开发这项功能。而且仅存的快递服务过于单一，不利于盈利。自助快递柜如果要持续稳定发展，就一定要有大量的用户，就目前看来，线上购物的客户选择用快递柜占比十分低。用户使用快递柜一般使用其存储、收取快递的服务，这也就表示智能快递柜需要在其他领域开发一些实用性强的服务，如缴纳水电费、购票、取票、充话费等各种服务。让所研发出的技术可以满足客户的各种需求，在不同领域体现各种功能，从实际意义上满足用户需要，给生活带来不同体验。如此一来，除了能够吸引用户还可以获取收益。开发商还可以将大量的便民服务投放到快递柜功能中进行使用，能够极大程度上提高用户体验，改善客户的生活，以及对快递柜使用过程的满意度，确保了智能快递柜的使用率，减少空闲率，又可为快递柜带来非常好的收益。'
    # datas = extract.extract_main(s)
    s = '假如得到了精确的变换阶次和谱峰对应的分数阶域的变量将采样间隔和谱峰点的坐标代入公式（5.1）就得到了线性调频信号（LFM）的各个参数的估计值'
    s = '民心向背是决定历史因果律的显性力量，因而与其说是“易主的天下”，不如说是人民的天下。'

    s = '研究发现金融扶贫不是简简单单的政策扶贫，也不是无条件的给贫困人群发放金钱补助，而是以一种低息或者无息贷款的方式给贫困人群提供必要的本金'

    s = '不管外部环境或功能需求如何地变化'

    s = '不管独立的还是网络的，s7-200 都能发挥其作用。'
    s = '不管是在生活上还是精神上电子产品都愉悦着人们'

    s = '但无论电子商务怎么样发展，计算机网络和通信技术始终都是电子采购业务开展的主体支柱'

    s =  '倒立摆的研究无论是在工业、农业还是运输行业，都被多次运用到。'  # 无论 还是  都

    s = '即便是在商店销售的水果花茶，也仅仅是我们日常都能见到的普通的包装设计，没有更多的创新点来吸引消费者。'
    s = '即便在今天，北方某电视台还是能靠反复播放《甄嬛传》赚来一轮又一轮的广告费。'
    s = '即便已经开始接受动物保护的观念，但更多的可能仍旧在关注自身的权益'

    s = '即使这样改变还不够'

    s = '即使有些企业有这一环节，但是也只是以汇报或考试的形式进行，严重脱离实际工作，很难获取良好的培训效果。'  # 不行

    s = '即使在数字新媒体时代有限动画已经有了很大的应用价值，却依然有它的缺点存在。'

    s = '保证即使在手机或电脑关机的情况下，这些数据仍然不会丢失。'
    s = '即使是这样，封建地主统治阶级也不能忍受'

    s = '独立的小包装设计可以满足消费者一次性饮用的需求，又可以方便携带，在便捷的同时又不失创新的特点。'

    s = '一方面可以完美的展现本身水果全部的样貌形态，本身就可以作为一种包装设计，另一方面更加直观的进行视觉表现，加深了解品牌文化。'
    print('旧的句子：', s)
    print('新的句子：', extract.exchange(s))
