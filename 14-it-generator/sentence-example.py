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