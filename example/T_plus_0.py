import core.simulator as sim
import math


class MyPriceSeries(sim.PriceSeries):

    def get_price(self, time):
        shock = 0
        if time % 2 == 0:
            shock = -1
        else:
            shock = 1
        return 10 + 10 * math.sin(time / 6) + shock

    def get_duration(self):
        return 50


class MyTradeSeries(sim.TradeSeries):

    def get_trade(self, time):
        if time <= 1:  # 建仓
            return 500
        else:  # 频繁交易
            if time % 2 == 0:  # 高抛低吸
                return 200
            else:
                return -200


s = sim.Simulator(MyPriceSeries(), MyTradeSeries(), account=10000)
s.simulate()
