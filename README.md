# NodeCreator
支持通过优选IP批量创建节点的本地工具

## 更新说明
### v0.6.0：
- 增加缓存机制
- 三击空格间隔须在2s内

### v0.5.0：
- 增加cfno1优选IP
- 支持优选IP+端口
- 支持从URL解析到IP列表
- 支持三击空格显示URL解析结果
- 支持ctrl+z撤回
- 提高响应速度
- 自动去除IP中的注释

### v0.4.0：
- 可以通过优选之后的节点生成优选节点

### v0.3.0：
- 版本内置CF官方、CF反代、CF官方优选以及CF反代优选IP

## 使用方法

1. 点击右侧Releases，下载NodeCreator.exe
2. 双击运行

&nbsp;&nbsp;&nbsp; ![90526e98365fbfe1ef04c.png](https://img.checo.cc/file/90526e98365fbfe1ef04c.png)

3. 输入原始节点（必须已经套了CDN）

&nbsp;&nbsp;&nbsp; ![9628e4dd2284a7ef171c9.png](https://img.checo.cc/file/9628e4dd2284a7ef171c9.png)

4. 输入优选IP或反代优选IP优选域名（支持`IP+端口`以及`域名+端口`）

   4.1 手动输入优选IP或优选域名

   ![a31a041c2647af103c984.png](https://img.checo.cc/file/a31a041c2647af103c984.png)

   4.2 在下拉框中选择优选IP

   ![58f56f6bcea4ffb270513.png](https://img.checo.cc/file/58f56f6bcea4ffb270513.png)

   4.3 输入URL自动获取优选IP

   ![24dd920cf59edbeca8aec.png](https://img.checo.cc/file/24dd920cf59edbeca8aec.png)

5. 选择随机或顺序并输入生成节点数量

&nbsp;&nbsp;&nbsp; ![image.png](https://cdn.nlark.com/yuque/0/2024/png/35591949/1710678807420-28cfa073-38e7-4273-9770-3403ce03d5e2.png#averageHue=%23eedfde&clientId=u651cf9be-a887-4&from=paste&height=52&id=u2a2e3bcd&originHeight=65&originWidth=699&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=9786&status=done&style=none&taskId=u715de2f4-afdc-41bf-ac5c-f48d96d8cb2&title=&width=559.2)

6. 点击生成节点

7. 点击复制按钮即可一键复制

8. 将节点导入代理工具即可使用

&nbsp;&nbsp;&nbsp; ![image.png](https://cdn.nlark.com/yuque/0/2024/png/35591949/1710679025271-e59bfd90-03ca-4c0c-a606-2f0105dc0872.png#averageHue=%23f6f5f5&clientId=u651cf9be-a887-4&from=paste&height=498&id=ub431f39d&originHeight=622&originWidth=2560&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=58553&status=done&style=none&taskId=u5da51605-482d-4a4a-acf6-78c44a41709&title=&width=2048)

## 编译方法(Windows)
```
python -m PyInstaller --onefile --windowed --icon=C:\Users\Administrator\Desktop\1\logo.ico --add-data C:\Users\Administrator\Desktop\1\logo.ico;. C:\Users\Administrator\Desktop\1\NodeCreator.py
```

## 更新计划

- [x] 增加预置优选IP
- [x] 增加vless节点
- [ ] 增加web版
- [x] 解决复制1条的问题
- [ ] 结果可保存
- [ ] 支持mac
- [x] 支持通过优选节点生成优选节点
- [x] 支持优选IP+端口
- [x] 支持Ctrl+Z撤回
- [x] 支持在IP列表直接输入URL
- [x] 支持连击空格将URL转换为IP列表
- [x] 自动去除IP列表中的#以及#之后的内容
- [x] 提高加载速度
- [x] 增加缓存，缓存已加载数据
- [ ] 增加缓存更新机制
- [ ] 增加启动之后自动预加载
- [ ] 优化UI
- [ ] 增加滚动条

## 致谢
感谢https://github.com/ymyuuu/IPDB 这一项目提供的IP数据
感谢[CF NO.1频道](https://t.me/cf_no1) 提供的优选反代IP





