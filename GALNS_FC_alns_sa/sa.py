initial_temperature = 1000
end_temperature = 0.1  # 0으로 설정할 수 없으므로, 아주 작은 값으로 설정합니다.
num_iterations = 10000

# 지수 감소율 계산 (고정된 값으로 계산됨)
step = (end_temperature / initial_temperature) ** (1 / num_iterations)

# 온도 갱신 루프
temperature = initial_temperature
for i in range(num_iterations):
    temperature = max(end_temperature, temperature * step)
    print(f"Iteration {i + 1}: Temperature = {temperature}")