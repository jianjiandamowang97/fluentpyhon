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

# 很好的观察！让我用代码精确演示为什么`__repr__`会被调用两次：你观察到的现象是正确的！**`__repr__`确实会被调用两次**，这是因为：
#
# ## 第4步中发生的两次调用：
#
# ```python
# sentence_list = [s, Sentence("Another sentence")]
# print(f"列表中的对象: {sentence_list}")
# ```
#
# ### 第一次调用：
# - **创建新对象**：`Sentence("Another sentence")` 创建时
# - 虽然看起来只是创建对象，但**实际上这个对象会立即被加入到列表中，然后在print时显示**
#
# ### 第二次调用：
# - **显示列表**：当`print(sentence_list)`执行时
# - Python需要显示列表中的每个对象，所以会调用每个对象的`__repr__`
#
# ## 更准确的说明：
#
# 实际上是这样的：
# 1. `s` 已经存在，不会再调用`__repr__`
# 2. `Sentence("Another sentence")` 创建新对象
# 3. `print(sentence_list)` 时，为了显示列表内容：
#    - 调用 `s` 的 `__repr__` → 第一次输出
#    - 调用新创建对象的 `__repr__` → 第二次输出
#
# ## 验证：
#
# 如果你想避免这个"混淆"，可以分步骤：
#
# ```python
# print("=== 分步骤演示 ===")
# s = Sentence("Hello world!")
#
# print("\n步骤1：创建第二个对象")
# s2 = Sentence("Another sentence")  # 这里可能调用__repr__
#
# print("\n步骤2：创建列表（不会调用__repr__）")
# sentence_list = [s, s2]
#
# print("\n步骤3：打印列表（这里调用__repr__）")
# print(sentence_list)
# ```
#
# ## 总结：
#
# 在你的原始代码中，`"🔥 __repr__方法被调用了!"` 输出两次是因为：
# 1. **列表中有两个Sentence对象**
# 2. **打印列表时，每个对象都需要调用`__repr__`来生成字符串表示**
# 3. **所以有几个对象就会调用几次`__repr__`**
#
# 这是完全正常的行为！每个对象都需要"自我介绍"才能在列表中被正确显示。

# print("=== 分步骤演示 ===")
# s = Sentence("Hello world!")
#
# print("\n步骤1：创建第二个对象")
# s2 = Sentence("Another sentence")  # 这里可能调用__repr__
#
# print("\n步骤2：创建列表（不会调用__repr__）")
# sentence_list = [s, s2]
#
# print("\n步骤3：打印列表（这里调用__repr__）")
# print(sentence_list)
#
# 你问得非常好！这里说"可能调用`__repr__`"而不是确定性的，是因为**这取决于你的运行环境**。让我详细解释：
#
# ## 为什么是"可能"而不是"确定"？## 核心答案
#
# **在Python脚本中（.py文件），`s2 = Sentence("Another sentence")` 这行代码本身【确定不会】调用`__repr__`。**
#
# 说"可能"是因为考虑了不同的运行环境：
#
# ### 🔴 在脚本中（确定不调用）
# ```python
# # script.py 文件中
# s2 = Sentence("Another sentence")  # ❌ 不调用__repr__
# ```
#
# ### 🟡 在交互式环境中（可能调用）
# ```python
# # Python REPL
# >>> s2 = Sentence("Another sentence")  # ❌ 赋值本身不调用
# >>> Sentence("Another sentence")  # ✅ 未赋值的表达式会调用
# ```
#
# ### 🟡 在Jupyter中（取决于位置）
# ```python
# # Jupyter cell
# s2 = Sentence("Another sentence")  # 如果是最后一行可能调用
# print("done")  # 如果有这行，上面就不会调用
# ```
#
# ## 为什么会有这种差异？
#
# 1. **Python脚本**：执行语句，不自动显示结果
# 2. **交互式环境**：为了方便，自动显示表达式的值
# 3. **Jupyter**：显示单元格最后一个表达式的值
#
# ## 实践建议
#
# 如果你想精确控制`__repr__`的调用：
#
# ```python
# # 明确分离创建和显示
# s2 = Sentence("Another sentence")  # 创建（不调用__repr__）
# print(s2)  # 显示（调用__repr__）
#
# # 或者用计数器追踪
# class Sentence:
#     def __repr__(self):
#         print(f"__repr__调用：{id(self)}")
#         return f"Sentence(...)"
# ```
#
# 所以说"可能"是为了涵盖所有运行环境，但在你的具体场景（Python脚本）中，单纯的赋值语句是**确定不会**调用`__repr__`的！