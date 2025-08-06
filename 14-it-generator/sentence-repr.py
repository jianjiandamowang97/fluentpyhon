import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        print("🔥 __repr__方法被调用了！")  # 添加这行来观察调用时机
        return 'Sentence(%s)' % reprlib.repr(self.text)


# 演示__repr__的各种调用时机
print("=== 创建对象 ===")
s = Sentence("Hello world!")

print("\n=== 1. 在交互式环境中直接输入对象名 ===")
# 在Python交互式环境中，直接输入变量名会调用__repr__
# s  # 这在脚本中不会显示，但在交互式环境中会调用__repr__

print("\n=== 2. 使用repr()函数 ===")
result = repr(s)
print(f"repr()返回: {result}")

print("\n=== 3. 使用str()函数（当没有__str__时） ===")
result = str(s)
print(f"str()返回: {result}")

print("\n=== 4. 在容器中显示对象 ===")
sentence_list = [s, Sentence("Another sentence")]
print(f"列表中的对象: {sentence_list}")

print("\n=== 5. 在字典中显示对象 ===")
sentence_dict = {"first": s}
print(f"字典中的对象: {sentence_dict}")

print("\n=== 6. 使用format或f-string（特定情况） ===")
print(f"使用!r格式: {s!r}")

print("\n=== 7. 调试信息 ===")
import pprint

pprint.pprint({"sentences": [s]})


# 对比：添加__str__方法的情况
class SentenceWithStr:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        print("🔥 __repr__被调用")
        return f'Sentence({reprlib.repr(self.text)})'

    def __str__(self):
        print("✨ __str__被调用")
        return f'句子包含{len(self.words)}个单词: {" ".join(self.words)}'


print("\n" + "=" * 50)
print("=== 有__str__方法的对比 ===")
s2 = SentenceWithStr("Hello world!")

print("\nstr()调用:")
print(str(s2))

print("\nrepr()调用:")
print(repr(s2))

print("\nprint()调用:")
print(s2)  # 优先调用__str__

print("\n在容器中:")
print([s2])  # 容器中仍然调用__repr__

# 解释sentence和repr函数