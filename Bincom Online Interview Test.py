import re
import random
import psycopg2
from collections import Counter
from statistics import mean, median, variance


data = {
    "MONDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "TUESDAY": "ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "WEDNESDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "THURSDAY": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "FRIDAY": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
}

# Extract all colors
colors = []
for day in data.values():
    colors.extend(re.findall(r'\b[A-Z]+\b', day))

# Count occurrences
color_counts = Counter(colors)

# Mean color (not mathematically accurate because you can only calculate mean of numeric data, choosing color with mean frequency index)
avg_freq = mean(color_counts.values())
mean_color = min(color_counts, key=lambda k: abs(color_counts[k] - avg_freq))

# Get most worn color
most_worn_color = color_counts.most_common(1)[0][0]

# Median color 
sorted_colors = sorted(color_counts.items(), key=lambda x: x[1])
median_color = median([v for k, v in sorted_colors])

# Variance (I love bonus questions)
color_variance = variance(color_counts.values())

# Probability of Red (Thankss)
prob_red = color_counts["RED"] / sum(color_counts.values())

# Store in PostgreSQL
def save_to_db():
    conn = psycopg2.connect("dbname=staffcolor user=Admin password=1234 host=localhost")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS color_frequencies (
            color TEXT PRIMARY KEY,
            frequency INT
        )
    """)
    for color, freq in color_counts.items():
        cur.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s) ON CONFLICT (color) DO NOTHING", (color, freq))
    conn.commit()
    conn.close()

#Recursive Function

def recursive_search(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return recursive_search(arr, target, mid + 1, high)
    else:
        return recursive_search(arr, target, low, mid - 1)
    
# Test recursive search
num_list = sorted(random.sample(range(1, 100), 10))
target_num = random.choice(num_list)
search_result = recursive_search(num_list, target_num)
print("Recursive Search - Target:", target_num, "Found at Index:", search_result)

# Generate 4-digit binary number and convert to base 10
binary_num = "".join(random.choices("01", k=4))
base10_num = int(binary_num, 2)

# Fibonacci sum
fib = [0, 1]
for _ in range(48):
    fib.append(fib[-1] + fib[-2])
fib_sum = sum(fib)

# Print results
print("Mean Color:", mean_color)
print("Most Worn Color:", most_worn_color)
print("Median Color:", median_color)
print("Color Variance:", color_variance)
print("Probability of Red:", prob_red)
print("Random Binary Number:", binary_num, "-> Base 10:", base10_num)
print("Sum of first 50 Fibonacci numbers:", fib_sum)

# Thank you for considering my applicaion to your company.