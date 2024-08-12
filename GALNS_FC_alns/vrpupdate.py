import numpy as np
import matplotlib.pyplot as plt

# 시뮬레이션 총 시간과 최대 고도 설정
total_time = 16  # 총 시간(분)
max_altitude = 100  # 최대 고도(m)

# 각 단계별 지속 시간 설정
vertical_duration = 1  # 수직 이륙/착륙 지속 시간(분)
horizontal_durations = [3, 3, 3, 3]  # 각 수평 비행 지속 시간(분)

# 고도 배열 초기화
altitude = np.zeros(total_time + 1)

# 현재 시간 설정
current_time = 0

# 비행 경로 시뮬레이션
for flight_time in horizontal_durations:
    # 이륙 (수직 상승)
    if current_time + vertical_duration <= total_time:
        end_time = current_time + vertical_duration
        altitude[current_time:end_time+1] = np.linspace(0, max_altitude, vertical_duration + 1)
        current_time = end_time

    # 수평 비행
    if current_time + flight_time <= total_time:
        end_time = current_time + flight_time
        altitude[current_time:end_time] = max_altitude
        current_time = end_time

    # 착륙 (수직 하강)
    if current_time + vertical_duration <= total_time:
        end_time = current_time + vertical_duration
        altitude[current_time:end_time+1] = np.linspace(max_altitude, 0, vertical_duration + 1)
        current_time = end_time

# 그래프 플로팅을 위해 부드러운 연결
times = np.arange(0, total_time + 1)
smooth_altitudes = np.interp(times, times[altitude != 0], altitude[altitude != 0])

# 고도 변화 그래프 생성
plt.figure(figsize=(15, 7))
plt.plot(times, smooth_altitudes, drawstyle='steps-post', linewidth=2, color='red')
plt.title('Drone Flight Path: Altitude Changes Over Time')
plt.xlabel('Time (min)')
plt.ylabel('Altitude (m)')
plt.grid(True)
plt.show()
