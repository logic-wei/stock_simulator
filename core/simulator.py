import math
import abc
from matplotlib import pyplot as plt


class PriceSeries(metaclass=abc.ABCMeta):
    """
    行情抽象接口
    """
    @abc.abstractmethod
    def get_price(self, time):
        """
        获取当前价格
        :param time:时间坐标（只是一个示意，用序号1,2，3代替即可）
        :return: 当前时间对应的价格
        """
        return 0

    @abc.abstractmethod
    def get_duration(self):
        """
        行情包含的时间段
        :return:时间长度（序号长度）
        """
        return 0


class TradeSeries(metaclass=abc.ABCMeta):
    """
    交易抽象接口
    """
    @abc.abstractmethod
    def get_trade(self, time):
        """
        获取当前时间对应的买卖操作
        :param time:当前时间
        :return:Trade
        """
        return 0


class TestPriceSeries(PriceSeries):
    def get_price(self, time):
        return math.sin(time / 6) * 5

    def get_duration(self):
        return 40


class TestTradeSeries(TradeSeries):
    def get_trade(self, time):
        if time % 2 == 0:
            return -200
        else:
            return 200


class Simulator:
    """
    根据给定的行情和操作手法，计算资产的盈亏变化
    """
    def __init__(self, price_series=TestPriceSeries(), trade_series=TestTradeSeries(), account=0):
        """
        构造一个新的模拟器
        :param price_series: 预设的行情数据
        :param trade_series: 预设的操作手法
        :param account: 初始资产
        """
        self.price_series = price_series
        self.trade_series = trade_series
        self.account = account

    def simulate(self):
        """
        开始模拟
        :return:None
        """
        time = range(self.price_series.get_duration())
        price = []              # 实时股价
        trade = []              # 实时交易
        account = []            # 账户余额
        hold_worth = []         # 持仓总价值
        hold_amount = []        # 持股总数
        total_property = []     # 总资产
        cost_average = []       # 筹码平均成本
        cost_total = []         # 筹码总成本
        earning = []            # 盈亏
        for i in time:
            price.append(self.price_series.get_price(i))
            if i == 0:
                # 0时刻初始化
                trade.append(0)
                account.append(self.account)
                hold_amount.append(0)
                hold_worth.append(hold_amount[i] * price[i])
                total_property.append(account[i] + hold_worth[i])
                cost_total.append(0)
                cost_average.append(0)
                earning.append(0)
            else:
                # 1时刻开始交易
                trade.append(self.trade_series.get_trade(i))
                hold_amount.append(hold_amount[i - 1] + trade[i])  # 买入
                hold_worth.append(hold_amount[i] * price[i])  # 持有价值
                cost_total.append(cost_total[i - 1] + price[i] * trade[i])  # 持仓总成本
                if hold_amount[i] == 0:  # 持仓平均成本
                    cost_average.append(0)
                else:
                    cost_average.append(cost_total[i] / hold_amount[i])
                account.append(account[i - 1] - price[i] * trade[i])  # 计算余额
                total_property.append(hold_worth[i] + account[i])  # 计算总资产
                earning.append(total_property[i] - self.account)
        # show you all the data
        subplot_size = 5
        subplot_index = 0
        fig, axs = plt.subplots(subplot_size, 1, sharex=True)
        # subplot 0
        lines = axs[subplot_index].plot(time, price, time, cost_average)  # 股价和成本价对比
        axs[subplot_index].legend(lines, ("price", "cost_average"), loc="upper right")
        axs[subplot_index].set_ylabel("yuan")
        subplot_index += 1
        # subplot 1
        lines = axs[subplot_index].bar(time, trade)  # 柱状图显示交易量
        axs[subplot_index].legend(lines, ("trade", ), loc="upper right")
        axs[subplot_index].set_ylabel("volume")
        subplot_index += 1
        # subplot 2
        lines = axs[subplot_index].bar(time, hold_amount)  # 柱状图显示持有量
        axs[subplot_index].legend(lines, ("hold_amount",), loc="upper right")
        axs[subplot_index].set_ylabel("volume")
        subplot_index += 1
        # subplot 3
        lines = axs[subplot_index].plot(time, hold_worth, "r--",
                                        time, account, "r-",
                                        time, total_property, "b--",
                                        time, earning, "b*")
        axs[subplot_index].legend(lines, ("hold_worth", "account", "total_property", "earning"), loc="upper right")
        axs[subplot_index].set_ylabel("yuan")
        subplot_index += 1
        # subplot 4
        lines = axs[subplot_index].plot(time, cost_total)
        axs[subplot_index].legend(lines, ("cost_total",), loc="upper right")
        axs[subplot_index].set_ylabel("yuan")

        fig.subplots_adjust(hspace=0)
        plt.show()


def main():
    sim = Simulator(account=10000)
    sim.simulate()


if __name__ == "__main__":
    main()
