# About
一个用于不同环境下自动实现工程化prompt的Python包，用prompt替换参数化声明模块，并把结果存在example中。

# Install
`$ pip3 install -U resounds`

# Director 
+ resounds 

# Description
我们现在遇到一个简单的问题，就是想判断两个字符串是不是一致，我应该怎么实现这个问题？
在这里就可以想到对字符串一致的定义，那如果以匹配方式来理解的话，那就是整体内容的一一对应，把这种情况写成代码是这个样子：
```python3
from typing import Annotated

def answer_correctness(
    predicted_answer: Annotated[str, "predicted answer"],
    gold_answer: Annotated[str, "gold answer"]
) -> bool:
    """Verify that the predicted answer matches the gold answer."""
    return predicted_answer == gold_answer

if __name__ == '__main__':
    print(answer_correctness('Hello', 'Hello'))   # True
    print(answer_correctness('Hi', 'Hello'))      # False
```
如果是判断是否完全一致，上面的这种描述是可以很好完成工作任务的。但是就像上面举例的情况，放在LLM的对话过程中，我们从语义上进行理解，"hello"和"hi"，这两个词从含义上是没有什么区别的。
对于这种情况，用机械匹配肯定是不可以的，这时候就提出了语义函数的情况，下面这个例子就可以明显进行对比：
```python3
# 一个比较函数
from typing import Annotated

def answer_correctness(
    predicted_answer: Annotated[str, "predicted answer"],
    gold_answer: Annotated[str, "gold answer"]
) -> bool:
    """Verify that the predicted answer matches the gold answer."""
    return predicted_answer == gold_answer

if __name__ == '__main__':
    print(answer_correctness('Hello', 'Hello'))   # True
    print(answer_correctness('How have you been?', 'How’s it going?'))      # False
    print(answer_correctness('How’s it going?', '最近怎么样？'))      # False

# 改写成语义函数
from resounds import predictor, GPT
from typing import Annotated

@predictor(GPT())
def answer_correctness(
    predicted_answer: Annotated[str, "predicted answer"],
    gold_answer: Annotated[str, "gold answer"]
) -> bool:
    """Verify that predicted answer and gold answer are expressing the same meaning."""
    if predicted_answer == gold_answer:
        return True
    return ...

if __name__ == '__main__':
    print(answer_correctness('Hello', 'Hello'))   # True
    print(answer_correctness('How have you been?', 'How’s it going?'))      # True
    print(answer_correctness('How’s it going?', '最近怎么样？'))      # True
# return ... 就会把下面的工作交给GPT进行完成。
```

# Contact us
<may.xiaoya.zhang@gmail.com>
