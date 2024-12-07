# Import needed library
import matplotlib.pyplot as plt

# Sample data
x = [1, 5, 10, 15, 20]
y = [50, 20, 100, 30, 150]

# Create a plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', color='gold')

# Add title and labels
plt.title('Sample Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.show()
