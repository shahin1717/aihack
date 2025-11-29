def apply_open_penalty(score: float) -> float:
    return max(0.0, score - 10)


def apply_click_penalty(score: float) -> float:
    return max(0.0, score - 30)


def apply_report_reward(score: float) -> float:
    return min(100.0, score + 20)

