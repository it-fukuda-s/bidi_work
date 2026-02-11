"""Fortune telling tool for Mysty agent."""

import random


def get_fortune() -> dict:
    """今日の運勢を占います。ユーザーが占いや運勢を聞いてきたときに使用してください。

    Returns:
        dict: 運勢、ラッキーアイテム、ラッキー方角、今日のアドバイスを含む辞書。
    """

    fortunes = ["大吉", "中吉", "小吉", "吉", "末吉"]
    lucky_items = [
        "赤いもの",
        "丸いもの",
        "甘いお菓子",
        "青い傘",
        "古い本",
        "新しい靴",
        "黄色い花",
        "銀のアクセサリー",
    ]
    lucky_directions = ["東", "西", "南", "北", "北東", "南西"]
    advice = [
        "今日は新しいことを始めるのに最適な日です",
        "慎重に行動すれば良い結果が得られるでしょう",
        "人との出会いを大切にしてください",
        "直感を信じて行動しましょう",
        "リラックスする時間を作ると運気がアップします",
        "笑顔を忘れずに過ごしましょう",
    ]

    return {
        "運勢": random.choice(fortunes),
        "ラッキーアイテム": random.choice(lucky_items),
        "ラッキー方角": random.choice(lucky_directions),
        "今日のアドバイス": random.choice(advice),
    }
