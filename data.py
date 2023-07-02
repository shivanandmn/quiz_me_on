from dataclasses import dataclass


@dataclass
class Quiz():
    question_text: str
    options: list
    correct_option_idx: int
    hint: str = ""
    explanation: str = ""

    def __post_init__(self):
        self.options = [str(x) for x in self.options]


if __name__ == '__main__':
    q = Quiz("question", [1, 3], 1)
    print(q)
    print()
