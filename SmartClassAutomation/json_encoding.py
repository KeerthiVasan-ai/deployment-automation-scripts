import base64

# Read the file as bytes
with open("D:\\deployment-automation-scripts\\SmartClassAutomation\\smartreserve.json", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

# Print the single-line base64 string
print(encoded)
