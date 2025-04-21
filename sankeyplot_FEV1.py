
import plotly.graph_objects as go
import pandas as pd

# コードの最初の部分で、pipのインストールチェックとkaleidoのインストールを行う
import importlib.util
import subprocess
import sys

# kaleidoのインストール確認
kaleido_spec = importlib.util.find_spec("kaleido")
kaleido_installed = kaleido_spec is not None

# kaleidoがインストールされていない場合、pythonモジュールとしてインストール
if not kaleido_installed:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'kaleido'], check=True)


# データの作成
data = {
    'From': ['>80%', '>80%', '>80%', '50-80%', '50-80%', '50-80%', '<50%', '<50%', '<50%'],
    'To': ['>80%', '50-80%', '<50%', '>80%', '50-80%', '<50%', '>80%', '50-80%', '<50%'],
    'Value': [23, 7, 0, 9, 2, 1, 1, 3, 6],
    'Percentage': [44.2, 13.5, 0.0, 17.3, 3.8, 1.9, 1.9, 5.8, 11.5]
}

df = pd.DataFrame(data)

# pre-biologicsとpost-biologicsのラベルを設定
labels = ['pre-biologics: >80%', 'pre-biologics: 50-80%', 'pre-biologics: <50%', 
         'post-biologics: >80%', 'post-biologics: 50-80%', 'post-biologics: <50%']

# インデックスのマッピング
label_to_index = {label: idx for idx, label in enumerate(labels)}

# ソースとターゲットの準備
sources = [label_to_index[f'pre-biologics: {label}'] for label in df['From']]
targets = [label_to_index[f'post-biologics: {label}'] for label in df['To']]
values = df['Value'].tolist()

# ノードの色を設定
node_colors = ["rgba(0,0,255,0.7)", "rgba(0,255,0,0.7)", "rgba(255,0,0,0.7)"] * 2

# リンクの色を設定（Pre-biologicsの状態に基づく）
link_colors = []
for source in sources:
    if source == 0:  # >80%からの遷移
        link_colors.append("rgba(0,0,255,0.3)")
    elif source == 1:  # 50-80%からの遷移
        link_colors.append("rgba(0,255,0,0.3)")
    else:  # <50%からの遷移
        link_colors.append("rgba(255,0,0,0.3)")

# 図の作成
fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = [""] * 6,  # 空のラベルを6つ設定
        color = node_colors
    ),
    link = dict(
        source = sources,
        target = targets,
        value = values,
        color = link_colors,
        label = [f"{val}% ({num})" for val, num in zip(df['Percentage'], df['Value'])]
    )
)])

# レイアウトの設定
fig.update_layout(
    title_text="FEV1 Changes before and after biologic therapy (n=52)",
    font_size=12,
    height=500
)

# 保存先のパスを指定して保存
save_path = "/Users/nfujino/Desktop/"  # 例：デスクトップに保存

fig.write_image(save_path + "sankey_diagram_high_res.png", width=500, height=800, scale=4)
fig.write_html(save_path + "sankey_diagram.html")



