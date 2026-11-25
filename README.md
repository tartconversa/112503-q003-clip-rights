# 衍生剪辑的权益敞口和月结冲回

衍生片段以半开毫秒区间表示。edge 的 source 在母版或衍生剪辑中定位，被引用区间长度与目标占用长度一致。聚合回款的净额单位为分，合约份额用千分比。 同层的权利人份额按该层涉及的秒数和合约份额计。layer_weights 的份额单位为万分比，不同层的权利收入口径不互换。授权状态缺行是尚未提供，另列拒绝记录明示禁止。

## 资料格式

样例均为合成记录。CSV 使用 UTF-8，首行为列名。日期或时间采用 ISO 表示，多值字段以竖线分隔，空单元格表示该来源未记录。保留多版记录和部分未匹配的业务事实可供复查。

- assets.csv 的字段为 asset、kind、duration、copyright_case。
- edges.csv 的字段为 parent、layer、source、source_from、source_to、target_from、target_to。
- rights.csv 的字段为 grant、case、market、channel、start、stop、segment_from、segment_to、parties、shares、rev。
- placements.csv 的字段为 placement、asset、channel、market、live_from、live_until、state。
- plays.csv 的字段为 event、placement、platform_key、start、end、valid_count。
- inflows.csv 的字段为 receipt、play_group、cents、date、refunds、market。
- paid.csv 的字段为 payment、month、receipt、party、cents、rights_rev。
- layer_weights.csv 的字段为 market、channel、layer、share_bp、from_day、to_day。

## 查验资料

使用 Python 3.11 及以上版本。资料检查只使用 Python 标准库。请在项目根目录运行。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
