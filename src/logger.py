import pandas as pd

# Save motion detection log data to a CSV file
def save_log(data, filename="motion_log.csv"):
    if data:
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            print(f"[LOG]: Motion log saved with {len(data)} entries.")
        except Exception as e:
            print(f"[Error]: Failed to write log: {e}")
