import pandas as pd
import matplotlib.pyplot as plt

# load data from file
df = pd.read_csv("graph.csv",sep=";")
print("Loaded data from graph.csv")

# plot the dependance of y on x
plt.plot(df["x"], df["y"], label="y = sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.savefig("graph.png") # save the plot as a file
print("Saved plot as graph.png")
