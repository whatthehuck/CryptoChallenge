31.py为服务器程序
31attack.py为攻击者程序
foo为服务器本机存在的测试文件

31.py 使用需要使用命令行 输入：python 31.py "http://localhost:9000/test?file=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51"

31attack.py 直接运行即可

31attack.py调用31.py通过返回时间来判断输入的MAC是否正确
同时会产生服务器返回结果
每当某一个字节正确，就输出当前已匹配的MAC
有问题找我。！！！！！