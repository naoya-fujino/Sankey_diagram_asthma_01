import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

# データの作成
data = {
    'From': ['>80%', '>80%', '>80%', '50-80%', '50-80%', '50-80%', '<50%', '<50%', '<50%'],
    'To': ['>80%', '50-80%', '<50%', '>80%', '50-80%', '<50%', '>80%', '50-80%', '<50%'],
    'Value': [23, 7, 0, 9, 2, 1, 1, 3, 6]
}

df = pd.DataFrame(data)

# ユニークな状態を取得
states = list(set(df['From']).union(set(df['To'])))
states.sort()

# 遷移行列を作成
transition_matrix = np.zeros((len(states), len(states)))

# 遷移データを行列に反映
for _, row in df.iterrows():
    from_idx = states.index(row['From'])
    to_idx = states.index(row['To'])
    transition_matrix[from_idx, to_idx] += row['Value']

# カイ二乗検定を実施
chi2, p_value, dof, expected = chi2_contingency(transition_matrix)

# 結果の表示
print(f"カイ二乗値: {chi2:.4f}")
print(f"p値: {p_value:.4e}")
print(f"自由度: {dof}")
