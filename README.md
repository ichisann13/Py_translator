# py_translator
## 简述
实时翻译屏幕上的指定区域

使用前需要安装paddleOCR, 并在百度翻译中申请API填入key.txt文件内. 百度翻译api申请地址: https://api.fanyi.baidu.com/api/trans/product/prodinfo

选定区域截图, 然后对图片进行文字识别, 使用百度翻译后展示在屏幕上

使用了paddleOCR进行文字识别, 调用百度翻译API翻译后展示在一个窗口内

焦点在窗口上时Ctrl+Q可以退出程序, Ctrl+B可以将窗口移动到鼠标位置, 同样, 拖拽也可以移动窗口, 但是会十分卡顿。

