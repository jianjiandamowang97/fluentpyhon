import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # 提取所有单词

    def __getitem__(self, index):
        return self.words[index]  # 支持索引访问

    def __len__(self):
        return len(self.words)  # 返回单词数量

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


# 运行示例
if __name__ == "__main__":
    # 创建Sentence对象
    s = Sentence("The quick brown fox jumps over the lazy dog!")

    print("=== 初始化后的状态 ===")
    print(f"原文本: {s.text}")
    print(f"提取的单词: {s.words}")
    print(f"单词数量: {len(s)}")
    print(f"对象表示: {repr(s)}")

    print("\n=== 索引访问 ===")
    print(f"第一个单词 s[0]: {s[0]}")
    print(f"第二个单词 s[1]: {s[1]}")
    print(f"最后一个单词 s[-1]: {s[-1]}")

    print("\n=== 切片操作 ===")
    print(f"前三个单词 s[0:3]: {s[0:3]}")
    print(f"后三个单词 s[-3:]: {s[-3:]}")

    print("\n=== 遍历操作 ===")
    print("遍历所有单词:")
    for i, word in enumerate(s):
        print(f"  {i}: {word}")

    print("\n=== 特殊情况 ===")
    # 包含标点符号和数字的文本
    s2 = Sentence("Hello, world! I have 123 apples & 456 oranges.")
    print(f"复杂文本: {s2.text}")
    print(f"提取的单词: {s2.words}")

    # 很长的文本（展示reprlib的截断功能）
    long_text = "word " * 30 + "end"
    s3 = Sentence(long_text)
    print(f"\n长文本的repr: {repr(s3)}")

    print("\n=== 序列协议测试 ===")
    print(f"是否支持 'in' 操作: {'quick' in s.words}")
    print(f"单词 'fox' 的索引: {s.words.index('fox')}")
    print(f"是否为空: {len(s) == 0}")
# 我来详细分析这段Python代码的运行过程。这是一个实现了序列协议的
# `Sentence`
# 类：
#
# ## 代码结构分析
#
# ### 1. 导入模块和正则表达式定义
# ```python
# import re
# import reprlib
#
# RE_WORD = re.compile(r'\w+')
# ```
#
# - `re`：正则表达式模块
# - `reprlib`：用于创建对象的简化字符串表示
# - `RE_WORD`：编译的正则表达式模式，`\w + `匹配一个或多个单词字符（字母、数字、下划线）
#
# ### 2. 类的初始化方法
# ```python
#
#
# def __init__(self, text):
#     self.text = text
#     self.words = RE_WORD.findall(text)  # <1>
#
#
# ```
#
# ** 运行过程： **
# - 接收文本参数并保存到
# `self.text`
# - 使用
# `RE_WORD.findall(text)`
# 提取文本中的所有单词
# - 将单词列表保存到
# `self.words`
#
# ** 示例： **
# ```python
# s = Sentence("Hello world! How are you?")
# # s.text = "Hello world! How are you?"
# # s.words = ['Hello', 'world', 'How', 'are', 'you']
# ```
#
# ### 3. 索引访问方法
# ```python
#
#
# def __getitem__(self, index):
#     return self.words[index]  # <2>
#
#
# ```
#
# ** 功能： ** 实现索引和切片操作，使对象可以像列表一样访问
# ** 示例： **
# ```python
# s = Sentence("Hello world!")
# print(s[0])  # 输出: "Hello"
# print(s[1])  # 输出: "world"
# print(s[0:2])  # 输出: ['Hello', 'world']
# ```
#
# ### 4. 长度方法
# ```python
#
#
# def __len__(self):  # <3>
#     return len(self.words)
#
#
# ```
#
# ** 功能： ** 返回句子中单词的数量
# ** 示例： **
# ```python
# s = Sentence("Hello world!")
# print(len(s))  # 输出: 2
# ```
#
# ### 5. 字符串表示方法
# ```python
#
#
# def __repr__(self):
#     return 'Sentence(%s)' % reprlib.repr(self.text)
#
#
# ```
#
# ** 功能： ** 提供对象的字符串表示，`reprlib.repr()`
# 会在文本过长时进行截断
# ** 示例： **
# ```python
# s = Sentence("Hello world!")
# print(repr(s))  # 输出: Sentence('Hello world!')
#
# # 对于很长的文本，reprlib.repr会截断
# long_text = "word " * 50
# s_long = Sentence(long_text)
# print(repr(s_long))  # 输出类似: Sentence('word word word word word word...')
# ```
#
# ## 完整运行示例## 核心设计特点
#
# ### 1. **序列协议实现**
# 通过实现
# `__getitem__`
# 和
# `__len__`
# 方法，这个类遵循了Python的序列协议，使得：
# - 对象可以被索引访问：`s[0]`
# - 支持切片操作：`s[1:3]`
# - 可以使用
# `len()`
# 函数
# - 支持迭代：`
# for word in s`
# - 支持
# ` in `操作符等
#
# ### 2. **正则表达式的使用**
# - `\w + `模式只匹配单词字符，会自动过滤掉标点符号和空格
# - `findall()`
# 方法一次性提取所有匹配的单词
#
# ### 3. **内存效率**
# - 在初始化时一次性提取所有单词并存储
# - 后续的索引访问都是直接从预处理的列表中获取
#
# ### 4. **用户友好的表示**
# - `reprlib.repr()`
# 在文本过长时会自动截断，避免输出过长的字符串
#
# 这个设计模式常用于需要将文本按单词处理的场景，如文本分析、自然语言处理等应用中。