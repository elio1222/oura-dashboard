import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

# Generate 100 consecutive days
start_date = dt.date(2024, 1, 1)
dates = [start_date + dt.timedelta(days=i) for i in range(100)]  # 100 days

# Dummy Y-values
y_data = np.random.rand(len(dates))

# Create a wide figure to fit all dates
fig, ax = plt.subplots(figsize=(40, 6))  # Wider = more space for each date label

# Plot dates vs values
ax.plot(dates, y_data, marker='o')

# Format X-axis to show every date
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Show every day

# Rotate date labels
plt.xticks(rotation=90)

# Optional: reduce padding between ticks
plt.tight_layout(pad=1.5)

# Labels and title
plt.title("Daily Values Over Time")
plt.xlabel("Date")
plt.ylabel("Value")

plt.show()
