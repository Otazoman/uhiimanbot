"""
 テスト用データ(全体)
"""
testdata = [
    {"ID": 1, "name": "山田太郎", "salary": 400000},
    {"ID": 2, "name": "田中一郎", "salary": 500000},
    {"ID": 3, "name": "田中花子", "salary": 300000},
    {"ID": 4, "name": "山下一郎", "salary": 250000},
    {"ID": 5, "name": "谷口次郎", "salary": 190000},
    {"ID": 6, "name": "坂本龍馬", "salary": 600000},
]

"""
テストのタイトル(検索、削除用)
"""
testtitles = [
    "\nall",
    "uniqueIDspecification",
    "string",
    "ngsign",
    "regexp(multi)",
    "regexp(single)",
    "number equal",
    "greater than",
    "more than",
    "less",
    "less than",
    "multiple",
    "none",
]

""" 
検索条件(検索、削除用)
"""
conditions = [
    # 全件
    {},
    # ユニークID指定
    {"ID": 3},
    # 文字列指定条件
    {"name": "坂本龍馬"},
    # 否定
    {"name": {"$ne": "坂本龍馬"}},
    # 正規表現
    {"name": {"$regex": "^田中"}},
    {"name": {"$regex": "^.*馬$"}},
    # 数値
    {"salary": 500000},
    # より大きい
    {"salary": {"$gt": 500000}},
    # 以上
    {"salary": {"$gte": 300000}},
    # 未満
    {"salary": {"$lt": 200000}},
    # 以下
    {"salary": {"$lte": 300000}},
    # 複合条件
    {"$and": [{"salary": {"$gte": 300000}}, {"name": {"$regex": "^.*郎$"}}]},
    # 条件に合致しない
    {"salary": 0},
]

""" カウント結果 """
countsdata = [6, 1, 1, 5, 2, 1, 1, 1, 4, 1, 3, 2, 0]

""" 検索結果 """
find_expected_results = [
    # 全件
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # ユニークID指定
    [
        {"ID": 3, "name": "田中花子", "salary": 300000},
    ],
    # 文字列指定条件
    [
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 否定
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 正規表現
    [
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
    ],
    [
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 数値
    [
        {"ID": 2, "name": "田中一郎", "salary": 500000},
    ],
    # より大きい
    [
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 以上
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 未満
    [
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 以下
    [
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 複合条件
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
    ],
    # なし
    [],
]

""" 削除後期待結果 """
delete_expected_results = [
    # 全件
    [],
    # ユニークID指定
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 文字列指定条件
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 否定
    [
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 正規表現
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 数値
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # より大きい
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 以上
    [
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
    ],
    # 未満
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 以下
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 複合条件
    [
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
    # 条件に合致しない
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000},
        {"ID": 2, "name": "田中一郎", "salary": 500000},
        {"ID": 3, "name": "田中花子", "salary": 300000},
        {"ID": 4, "name": "山下一郎", "salary": 250000},
        {"ID": 5, "name": "谷口次郎", "salary": 190000},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000},
    ],
]


"""
更新テスト用
"""
""" テストタイトル """
update_test_titles = [
    "\nUpdate specific key",
    "Update All",
    "Update regexp",
    "Update equal",
    "Update ngsign",
    "Update greater than",
    "Update More than",
    "Update Or Less",
    "Update less than",
    "Update Multipule condition",
    "unmatch condition",
    "Update Multipule values",
    "Update Multipule conditions and values",
]

""" 更新用条件と設定値 """
update_conditions = [
    # 特定のキーを指定
    {"ID": 1},
    # 全件
    {},
    # 正規表現に合致したもの
    {"name": {"$regex": "^田中"}},
    # 数値に合致したもの
    {"salary": 500000},
    # 条件に合致しないもの
    {"name": {"$ne": "坂本龍馬"}},
    # 特定数値より大きいもの
    {"salary": {"$gt": 500000}},
    # 特定数値以上のもの
    {"salary": {"$gte": 300000}},
    # 特定数値未満のもの
    {"salary": {"$lt": 200000}},
    # 特定数値以下のもの
    {"salary": {"$lte": 300000}},
    # 複合条件に合致するもの
    {
        "$and": [
            {"salary": {"$gte": 300000}},
            {"name": {"$regex": "^.*郎$"}},
        ]
    },
    # 条件に合致しないケース
    {"ID": 100},
    # 複数要素
    {"ID": 1},
    # 複合条件に合致するものの複数要素
    {
        "$and": [
            {"salary": {"$gte": 300000}},
            {"name": {"$regex": "^.*郎$"}},
        ]
    },
]

replacements_values = [
    {"$set": {"salary": 300000}},
    {"$set": {"salary": 1000000}},
    {"$set": {"salary": 950000}},
    {"$set": {"name": "山岡鉄舟"}},
    {"$set": {"salary": 550000}},
    {"$set": {"name": "高木ブー"}},
    {"$set": {"salary": 2000000}},
    {"$set": {"name": "大西太郎"}},
    {"$set": {"name": "ダミー"}},
    {"$set": {"name": "猫ひろし"}},
    {"$set": {"salary": 300000}},
    {"$set": {"name": "山本一郎", "salary": 300000}},
    {"$set": {"name": "猫ひろし", "salary": 600000}},
]


""" 更新後の期待結果 """
update_expected_results = [
    # 指定IDの要素が更新される
    [{"ID": 1, "name": "山田太郎", "salary": 300000}],
    # 全件の要素が更新される
    [
        {"ID": 1, "name": "山田太郎", "salary": 1000000},
        {"ID": 2, "name": "田中一郎", "salary": 1000000},
        {"ID": 3, "name": "田中花子", "salary": 1000000},
        {"ID": 4, "name": "山下一郎", "salary": 1000000},
        {"ID": 5, "name": "谷口次郎", "salary": 1000000},
        {"ID": 6, "name": "坂本龍馬", "salary": 1000000},
    ],
    # 正規表現に合致した場合に要素が更新される
    [
        {"ID": 2, "name": "田中一郎", "salary": 950000},
        {"ID": 3, "name": "田中花子", "salary": 950000},
    ],
    # 数値に合致した場合に要素が更新される
    [
        {"ID": 2, "name": "山岡鉄舟", "salary": 500000},
    ],
    # 条件に合致しない場合に要素が更新される
    [
        {"ID": 1, "name": "山田太郎", "salary": 550000},
        {"ID": 2, "name": "田中一郎", "salary": 550000},
        {"ID": 3, "name": "田中花子", "salary": 550000},
        {"ID": 4, "name": "山下一郎", "salary": 550000},
        {"ID": 5, "name": "谷口次郎", "salary": 550000},
    ],
    # 指定された値より大きな場合に要素が更新される
    [{"ID": 6, "name": "高木ブー", "salary": 600000}],
    # 指定された値以上の場合に要素が更新される
    [
        {"ID": 1, "name": "山田太郎", "salary": 2000000},
        {"ID": 2, "name": "田中一郎", "salary": 2000000},
        {"ID": 3, "name": "田中花子", "salary": 2000000},
        {"ID": 6, "name": "坂本龍馬", "salary": 2000000},
    ],
    # 指定された値未満の場合に要素が更新される
    [
        {"ID": 5, "name": "大西太郎", "salary": 190000},
    ],
    # 指定された値以下の場合に要素が更新される
    [
        {"ID": 3, "name": "ダミー", "salary": 300000},
        {"ID": 4, "name": "ダミー", "salary": 250000},
        {"ID": 5, "name": "ダミー", "salary": 190000},
    ],
    # 複合条件に合致した場合に要素が更新される
    [
        {"ID": 1, "name": "猫ひろし", "salary": 400000},
        {"ID": 2, "name": "猫ひろし", "salary": 500000},
    ],
    # 条件に合致しない場合は更新されない
    [],
    # 複数要素が更新される
    [{"ID": 1, "name": "山本一郎", "salary": 300000}],
    # 複合条件に合致すると複数項目が更新される
    [
        {"ID": 1, "name": "猫ひろし", "salary": 600000},
        {"ID": 2, "name": "猫ひろし", "salary": 600000},
    ],
]

""" テストタイトル(要素追加の場合) """
add_test_titles = [
    "Add specific key",
    "Add All",
    "Add regexp",
    "Add equal",
    "Add ngsign",
    "Add greater than",
    "Add More than",
    "Add Or Less",
    "Add less than",
    "Add Multipule condition",
    "Add Multipule values",
    "Add Multipule conditions and values",
]

""" 更新用条件の設定値 """
add_values = [
    {"$set": {"pgskill": "Java"}},
    {"$set": {"memo": "日本人です"}},
    {"$set": {"memo": "たなか"}},
    {"$set": {"memo": "給料やすすぎ"}},
    {"$set": {"memo": "凡人"}},
    {"$set": {"pgskill": "javascript"}},
    {"$set": {"pgskill": "Rust"}},
    {"$set": {"memo": "貧乏です"}},
    {"$set": {"pgskill": "Ruby"}},
    {"$set": {"memo": "実はアメリカ生まれ"}},
    {"$set": {"salary": 300000}},
    {"$set": {"pgskill": "Java", "phone": "080-999-8888"}},
    {"$set": {"memo": "実はアメリカ生まれ", "size": 22}},
]


""" 更新後(要素追加)の期待結果 """
add_expected_results = [
    # 指定IDに要素が追加される
    [{"ID": 1, "name": "山田太郎", "salary": 400000, "pgskill": "Java"}],
    # 全件に要素が追加される
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000, "memo": "日本人です"},
        {"ID": 2, "name": "田中一郎", "salary": 500000, "memo": "日本人です"},
        {"ID": 3, "name": "田中花子", "salary": 300000, "memo": "日本人です"},
        {"ID": 4, "name": "山下一郎", "salary": 250000, "memo": "日本人です"},
        {"ID": 5, "name": "谷口次郎", "salary": 190000, "memo": "日本人です"},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000, "memo": "日本人です"},
    ],
    # 正規表現に合致した場合に要素が追加される
    [
        {"ID": 2, "name": "田中一郎", "salary": 500000, "memo": "たなか"},
        {"ID": 3, "name": "田中花子", "salary": 300000, "memo": "たなか"},
    ],
    # 数値に合致した場合に要素が追加される
    [{"ID": 2, "name": "田中一郎", "salary": 500000, "memo": "給料やすすぎ"}],
    # 条件に合致しない場合に要素が追加される
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000, "memo": "凡人"},
        {"ID": 2, "name": "田中一郎", "salary": 500000, "memo": "凡人"},
        {"ID": 3, "name": "田中花子", "salary": 300000, "memo": "凡人"},
        {"ID": 4, "name": "山下一郎", "salary": 250000, "memo": "凡人"},
        {"ID": 5, "name": "谷口次郎", "salary": 190000, "memo": "凡人"},
    ],
    # 指定された値より大きな場合に要素が追加される
    [{"ID": 6, "name": "坂本龍馬", "salary": 600000, "pgskill": "javascript"}],
    # 指定された値以上の場合に要素が追加される
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000, "pgskill": "Rust"},
        {"ID": 2, "name": "田中一郎", "salary": 500000, "pgskill": "Rust"},
        {"ID": 3, "name": "田中花子", "salary": 300000, "pgskill": "Rust"},
        {"ID": 6, "name": "坂本龍馬", "salary": 600000, "pgskill": "Rust"},
    ],
    # 指定された値未満の場合に要素が追加される
    [
        {"ID": 5, "name": "谷口次郎", "salary": 190000, "memo": "貧乏です"},
    ],
    # 指定された値以下の場合に要素が追加される
    [
        {"ID": 3, "name": "田中花子", "salary": 300000, "pgskill": "Ruby"},
        {"ID": 4, "name": "山下一郎", "salary": 250000, "pgskill": "Ruby"},
        {"ID": 5, "name": "谷口次郎", "salary": 190000, "pgskill": "Ruby"},
    ],
    # 複合条件に合致した場合に要素が追加される
    [
        {"ID": 1, "name": "山田太郎", "salary": 400000, "memo": "実はアメリカ生まれ"},
        {"ID": 2, "name": "田中一郎", "salary": 500000, "memo": "実はアメリカ生まれ"},
    ],
    # 条件に合致しない場合は追加されない
    [],
    # 複数要素が追加される
    [
        {
            "ID": 1,
            "name": "山田太郎",
            "salary": 400000,
            "pgskill": "Java",
            "phone": "080-999-8888",
        }
    ],
    # 複合条件に合致すると複数項目が追加される
    [
        {
            "ID": 1,
            "name": "山田太郎",
            "salary": 400000,
            "memo": "実はアメリカ生まれ",
            "size": 22,
        },
        {
            "ID": 2,
            "name": "田中一郎",
            "salary": 500000,
            "memo": "実はアメリカ生まれ",
            "size": 22,
        },
    ],
]
