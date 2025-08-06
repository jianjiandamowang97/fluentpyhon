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

# 我来详细解释`__repr__`方法的调用机制和`Sentence(%s)`的作用：
#
# ## `__repr__`方法何时被调用
#
# `__repr__`是Python的特殊方法（魔术方法），会在以下情况被**自动调用**：## `Sentence(%s)` 的作用详解
#
# `Sentence(%s)` 是一个**字符串格式化模板**，作用是创建对象的标准字符串表示：## 总结
#
# ### `__repr__`被调用的时机：
# 1. **交互式环境**：直接输入对象变量名
# 2. **repr()函数**：显式调用
# 3. **容器显示**：对象在列表、字典等容器中
# 4. **调试**：使用调试器或pprint时
# 5. **格式化**：使用`!r`格式符时
# 6. **str()函数**：当没有定义`__str__`时作为备选
#
# ### `Sentence(%s)`的设计意图：
#
# 1. **标准格式**：遵循Python对象表示的约定
#    ```python
#    ClassName(constructor_arguments)
#    ```
#
# 2. **可重现性**：理想情况下，repr的输出应该能重新创建对象
#    ```python
#    s = Sentence("Hello")
#    # repr(s) 返回 "Sentence('Hello')"
#    # eval("Sentence('Hello')") 应该能创建相同的对象
#    ```
#
# 3. **安全处理特殊字符**：
#    - `reprlib.repr()`会正确转义引号、换行符等
#    - 避免字符串注入问题
#    - 长文本自动截断
#
# 4. **调试友好**：
#    - 清晰显示对象类型和内容
#    - 在日志和错误信息中提供有用信息
#
# ### 为什么使用`reprlib.repr()`而不是直接用字符串？
#
# ```python
# # ❌ 不安全的方式
# def __repr__(self):
#     return f'Sentence({self.text})'
#
# # ✅ 安全的方式
# def __repr__(self):
#     return 'Sentence(%s)' % reprlib.repr(self.text)
# ```
#
# `reprlib.repr()`的优势：
# - **转义特殊字符**：正确处理引号、换行符等
# - **长度限制**：防止输出过长的字符串
# - **类型安全**：确保输出是有效的Python字符串字面量
#
# 这种设计使得对象在调试、日志记录和交互式开发中都有清晰、安全的字符串表示。