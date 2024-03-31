# educhain

A Python package for generating educational content using Generative AI. Educhain makes it easy to apply Generative AI in various educational use cases to create engaging and personalized learning experiences 

## Installation

```shell
pip install educhain
```

## Usage

### Use it to Generate MCQs

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1bseC2F00l42JPVN2-35fwMupeTnyYGME?usp=sharing)

##### With given no. of ques, no csv generated

```shell
from educhain import qna_engine

topic = "Theory of Relativity"
level = "Intermediate"
num = 5

mcq = qna_engine.generate_mcq(topic, level, num)
print(mcq)
```
##### With given no. of ques. & csv generated with given file_name

```shell
from educhain import qna_engine

topic = "Quantum Entanglement"
level = "Intermediate"
num = 5
file_name="my_mcqs.csv"

mcq = qna_engine.generate_mcq(topic, level, num=num, file_name=file_name)
print(mcq)
```

### Effortlessly create Lesson Plans


```shell
from educhain import content_engine

topic = "Medieval History"
level = "Beginner"

lesson_plan = content_engine.generate_lesson_plan(topic, level)
print(lesson_plan)
```


## Next Steps

Will be releasing more features for MCQ Generation
- [x] Bulk Generation
- [x] Outputs in JSON format
- [x] Export questions to CSV
- [ ] Support for other LLM models
- [ ] Generate questions from text/pdf file
- [ ] Finetuned Model for question generation



