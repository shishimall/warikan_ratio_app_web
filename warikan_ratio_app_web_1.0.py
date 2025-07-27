# warikan_ratio_app_web

import streamlit as st
import pandas as pd

st.set_page_config(page_title="割り勘アプリ", layout="centered")
st.title("\U0001f4b8 割り勘計算アプリ（%指定）")

st.write("""
### 💡 アプリの使い方：
1. 合計金額を入力します
2. 割り勘する人数を入力します
3. 入力方式を選択します（ユーザー指定 or 等倍）
4. 各人の名前と支払割合（%）を入力します（※等倍なら自動計算）
5. [計算する] を押すと、支払金額が表示されます
※ 割合の合計が100%になるようにしてください
""")

# 入力：合計金額
total_amount = st.number_input("合計金額（円）を入力してください", min_value=0, step=1000)

# 入力：人数
num_people = st.number_input("人数を入力してください", min_value=1, step=1)

# 入力方式の選択
mode = st.radio("入力方式を選択", ["ユーザー指定", "等倍（自動）"])

st.subheader("参加者の名前と割合（%）を入力してください")

names = []
percents = []

# 割合のデフォルト
for i in range(int(num_people)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"名前{i+1}", value=f"参加者{i+1}", key=f"name_{i}")
    with col2:
        if mode == "等倍（自動）":
            percent = round(100 / num_people, 2)
            st.number_input(f"割合{i+1} (%)", value=percent, key=f"percent_{i}", disabled=True)
        else:
            percent = st.number_input(f"割合{i+1} (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key=f"percent_{i}")
        percents.append(percent)
    names.append(name)

# 合計割合の確認
total_percent = round(sum(percents), 2)
if mode == "ユーザー指定":
    if total_percent > 100:
        st.error(f"割合の合計が {total_percent}% です。100% 以下にしてください。")
    else:
        st.info(f"現在の合計割合：{total_percent}% / 残り {100 - total_percent}%")

if st.button("計算する"):
    if total_percent == 0:
        st.error("割合の合計が0%です。1人以上に割合を設定してください。")
    elif total_percent != 100:
        st.warning(f"割合の合計が {total_percent}% です。100% に調整してください。")
    else:
        result = []
        for name, percent in zip(names, percents):
            amount = round(total_amount * (percent / 100))
            result.append((name, f"{percent:.2f}%", amount))

        df = pd.DataFrame(result, columns=["名前", "割合", "支払金額（円）"])
        st.success("\U0001f4b0 割り勘結果")
        st.dataframe(df, use_container_width=True)

        # 合計確認
        st.markdown(f"**計算チェック：{sum([r[2] for r in result])} 円 / 合計 {total_amount} 円**")
