# CryptoArb

brief introduction:
This is the code for cryptocurrency arbtriage, included exchanges: huobi, okex, binance, polenix, kakren

main idea:
when highest_bid > lowest_ask, there is a no-risk oppounity(logically): buy in lowest_ask and sell in highest_bid.
sloving sell short problem: use withdraw function (transfer coin from A->B), withdraw can be quite time-costly, in
the waiting period, the program will get into frozen state to wait the withdraw finished, once finished, the program
will go on.

system:
both windows and linux are fine, since it's a python project.
python2.7
notice: these exchanges's server address are blocked in china.

run command:
python main_handler.py

config:
two config needed, 1 for account 2 for strategy

risk control:
to aviod one exchange failed, it will check total position, to ensure it is in a reasonable number.
for example:
i set sell_out_count =  0 buy_back_count = 3 for btc in huobi and okex, if okex had problem that day, huobi alway gets filled and okex
failed, the total num of btc will keep increasing or decreasing, if it >3 or <0, the programe will stop, since it's not in [sell_out_count, buy_back_count]

for more:
you can check this to know the market data and see the visual ui for the oppounity. https://github.com/nickhuangxinyu/CryptoUI

Author:
XinYu Huang

any questions or suggestions are welcome, please contract me with:huangxy17@fudan.edu.cn, i will list your name here to thanks for
your contribution.

Thanks list:
