from dataclasses import dataclass


@dataclass
class AppState:
    quiz_level: str = "Easy"
    quiz_count: int = 10  # default number of questions


APP_STATE = AppState()
