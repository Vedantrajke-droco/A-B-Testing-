
# Import libraries
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, norm
import matplotlib.pyplot as plt

df = pd.read_csv("ab_test_data.csv")
print("\nDataset Loaded Successfully\n")
print(df.head())

control = df[df["group"] == "control"]["converted"]
test = df[df["group"] == "test"]["converted"]

print("\nHYPOTHESIS:")
print("H0: No difference between control and test conversion rates")
print("H1: There is a significant difference between control and test conversion rates")

alpha = 0.05
print("Alpha =", alpha)


control_rate = control.mean()
test_rate = test.mean()

print("\nConversion Rates:")
print("Control Group:", control_rate)
print("Test Group:", test_rate)

t_stat, p_value = ttest_ind(test, control)
print("\nT-Statistic:", t_stat)
print("P-Value:", p_value)


print("\nDECISION:")
if p_value < alpha:
    print("Reject Null Hypothesis (H0)")
    decision = "Test group is significantly better."
else:
    print("Fail to Reject Null Hypothesis (H0)")
    decision = "No significant difference found."

diff = test.mean() - control.mean()
se = np.sqrt(test.var()/len(test) + control.var()/len(control))

ci_low = diff - 1.96 * se
ci_high = diff + 1.96 * se

print("\n95% Confidence Interval for Difference:")
print("Lower Bound:", ci_low)
print("Upper Bound:", ci_high)


group_means = df.groupby("group")["converted"].mean()

plt.figure()
group_means.plot(kind="bar")
plt.title("Conversion Rate: Control vs Test Group")
plt.xlabel("Group")
plt.ylabel("Conversion Rate")
plt.show()

summary = pd.DataFrame({
    "Group": ["Control", "Test"],
    "Conversion Rate": [control_rate, test_rate]
})

summary.to_csv("ab_test_summary.csv", index=False)
print("\nab_test_summary.csv saved successfully")


with open("final_recommendation.txt", "w") as f:
    f.write("A/B Testing Result\n")
    f.write("-------------------\n")
    f.write(f"Control Conversion Rate: {control_rate}\n")
    f.write(f"Test Conversion Rate: {test_rate}\n")
    f.write(f"P-Value: {p_value}\n")
    f.write(f"Decision: {decision}\n")
    f.write(f"95% Confidence Interval: ({ci_low}, {ci_high})\n")

print("final_recommendation.txt saved successfully")

