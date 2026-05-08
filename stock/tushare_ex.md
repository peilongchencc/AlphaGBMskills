```bash
# 安装
pip install tushare
```

```python
# 使用示例
import tushare as ts
ts.set_token('你的token')  # 注册 tushare.pro 获取
pro = ts.pro_api()

# 获取日线数据
df = pro.daily(ts_code='000001.SZ', start_date='20200101')

# 获取期权日线（需要积分够）
df = pro.opt_daily(exchange='SSE', trade_date='20260507')
```