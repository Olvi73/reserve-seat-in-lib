# reserve-seat-in-lib
我去图书馆 自动抢座助手

[reserve_seat_today.py](https://github.com/Olvi73/reserve-seat-in-lib/blob/main/reserve_seat_today.py)：当日预约

[reserve_seat_tomorrow.py](https://github.com/Olvi73/reserve-seat-in-lib/blob/main/reserve_seat_tomorrow.py)：次日预约（开发中）



## 使用

1. 修改`reserve_seat_today.py`中的教室编号以及座位编号
2. 抓包获取cookie，确保含有四个参数`wechatSESS_ID`、`SERVERID`、`Hm_lpvt_7ecd21a13263a714793f376c18038a87`、`Hm_lvt_7ecd21a13263a714793f376c18038a87`，可多不可少，后续通过正则自动匹配
3. 运行`reserve_seat_today.py`
4. 点一下右上角的`star`及便时获取最新版本

![](https://gitee.com/Olvi73/img/raw/master/seat%201.png?_sasdk=fE%3F%40C%3FA%3D)
