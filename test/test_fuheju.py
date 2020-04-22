import unittest
from fuheju_handle import *

class TestSentenceHandle(unittest.TestCase):
    def setUp(self):
        self.extract = Extraction()

    def test_ruguo(self):
        '''
            假设、假如、假若、假使、如果
            那么、就、也、还、则、使
        :return:
        '''
        # 假如xxx，就yyy == yyy， 假如xxx
        s = '假如用户登录成功，就能够顺利运行App。'
        daozhuan_s = '能够顺利运行App，倘若用户登录成功。'
        # self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # A假如xxx，就yyy  == Ayyy，假如xxx
        s = '自助快递柜如果要持续稳定发展，就一定要有大量的用户，就目前看来，线上购物的客户选择用快递柜占比十分低。'
        daozhuan_s = '自助快递柜一定要有大量的用户，假若要持续稳定发展，就目前看来，线上购物的客户选择用快递柜占比十分低。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 假如xxx，A就yyy  == Ayyy，假如xxx
        s = '假如原始指标个数较多，综合评价就比较麻烦。'
        daozhuan_s = '综合评价比较麻烦，假如原始指标个数较多。'
        # self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 假如得到了精确的变换阶次和谱峰对应的分数阶域的变量将采样间隔和谱峰点的坐标代入公式（5.1）就得到了线性调频信号（LFM）的各个参数的估计值
        # 不做倒装，词替换。

        # 与其 - 不如
        s = '民心向背是决定历史因果律的显性力量，因而与其说是“易主的天下”，不如说是人民的天下。'
        daozhuan_s = '民心向背是决定历史因果律的显性力量，因而宁可说是人民的天下，也好过说是“易主的天下”。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 不是 - 也不是
        s = '研究发现金融扶贫不是简简单单的政策扶贫，也不是无条件的给贫困人群发放金钱补助，而是以一种低息或者无息贷款的方式给贫困人群提供必要的本金。'
        daozhuan_s = '研究发现金融扶贫既不是无条件的给贫困人群发放金钱补助，也不是简简单单的政策扶贫，而是以一种低息或者无息贷款的方式给贫困人群提供必要的本金。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 不是 - 而是
        s = '本毕设介绍了LTE无线网络的规划及优化方法、目的及流程，并不是简单的罗列LTE-TDD网络的优化流程和方法，而是以现网实际的优化数据和经验为基础，贯穿整个LTE-TDD无线网络建设的生命全周期，设计出LTE-TDD网络在优化阶段的重点工作和关键步骤，包括网络优化阶段的网络覆盖优化、网络结构和干扰优化、网络性能指标优化等内容。'
        daozhuan_s = '本毕设介绍了LTE无线网络的规划及优化方法、目的及流程，并是以现网实际的优化数据和经验为基础，而不是简单的罗列LTE-TDD网络的优化流程和方法，贯穿整个LTE-TDD无线网络建设的生命全周期，设计出LTE-TDD网络在优化阶段的重点工作和关键步骤，包括网络优化阶段的网络覆盖优化、网络结构和干扰优化、网络性能指标优化等内容。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

        s = '不是美国有多牛逼，而是小日子太菜了。'
        daozhuan_s = '是小日子太菜了，而不是美国有多牛逼。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 不管-始终
        s = '不管有多少任务，我们都始终让线程池中的线程轮番上阵，这样就避免了不必要的开销。'
        daozhuan_s = '要让线程池中的线程轮番上阵，无论有多少任务，我们都，这样就避免了不必要的开销。'
        # self.assertEqual(daozhuan_s, self.extract.exchange(s))

        # 不管-，还是
        s = '京津冀不管从它的开放程度上说，还是从城市的活跃程度和国家近年来提倡的创新方面，都是处于我国发展前列的。'
        daozhuan_s = '京津冀无论从城市的活跃程度和国家近年来提倡的创新方面，还是从它的开放程度上说，都是处于我国发展前列的。'
        self.assertEqual(daozhuan_s, self.extract.exchange(s))

if __name__ == '__main__':
    unittest.main()
