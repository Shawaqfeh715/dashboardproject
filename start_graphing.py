import matplotlib.pyplot as plt
import pandas as pd
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

hadestest = '/Users/anasshaw/Downloads/HADESTestData.csv'


# SOLUTION 1: Manual CSV reading with error handling
def read_problematic_csv(filepath):
    data = []
    max_columns = 0

    with open(filepath, 'r', encoding='latin-1', errors='ignore') as file:
        for line_num, line in enumerate(file, 1):
            try:
                # Clean the line and split by comma
                line = line.strip()
                if line:  # Only process non-empty lines
                    row = line.split(',')
                    # Clean each field
                    row = [field.strip('"\' ') for field in row]
                    data.append(row)
                    max_columns = max(max_columns, len(row))
            except Exception as e:
                print(f"Warning: Skipping line {line_num} due to error: {e}")
                continue

    # Normalize all rows to have the same number of columns
    for i, row in enumerate(data):
        if len(row) < max_columns:
            data[i] = row + [''] * (max_columns - len(row))
        elif len(row) > max_columns:
            data[i] = row[:max_columns]

    return data


# Read the problematic CSV
data = read_problematic_csv(hadestest)

if len(data) > 1:
    # Use first row as headers, rest as data
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)

    # Clean column names (remove extra spaces, etc.)
    df.columns = [col.strip() for col in df.columns]

    print("Columns found:", df.columns.tolist())
    print("Data shape:", df.shape)
    print("\nFirst 5 rows:")
    print(df.head())

    # Convert numeric columns to appropriate types
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            pass

else:
    print("Error: Not enough data in CSV file")
    df = pd.DataFrame()

# If we have data, proceed with plotting
if not df.empty and len(df) > 0:
    # Map possible column name variations
    column_mapping = {
        'altitude': ['altitude', 'Altitude', 'ALTITUDE', 'alt'],
        'x_position': ['X position', 'x position', 'X_position', 'x', 'X'],
        'y_position': ['Y position', 'y position', 'Y_position', 'y', 'Y'],
        'latitude': ['Latitude', 'latitude', 'LATITUDE', 'lat'],
        'longitude': ['Longitude', 'longitude', 'LONGITUDE', 'lon', 'long']
    }

    # Find actual column names
    actual_columns = {}
    for target_col, possible_names in column_mapping.items():
        for name in possible_names:
            if name in df.columns:
                actual_columns[target_col] = name
                break

    print("\nFound columns mapping:", actual_columns)

    # Extract data using actual column names
    if all(col in actual_columns for col in ['altitude', 'x_position', 'y_position']):
        altitude = pd.to_numeric(df[actual_columns['altitude']], errors='coerce').dropna().values
        x_position = pd.to_numeric(df[actual_columns['x_position']], errors='coerce').dropna().values
        y_position = pd.to_numeric(df[actual_columns['y_position']], errors='coerce').dropna().values

        min_length = min(len(altitude), len(x_position), len(y_position))
        altitude = altitude[:min_length]
        x_position = x_position[:min_length]
        y_position = y_position[:min_length]

        print(f"Plotting {min_length} data points")

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the entire trajectory
        ax.plot(x_position, y_position, altitude, 'b-', alpha=0.3, label="Rocket Path")
        ax.scatter(x_position[-1], y_position[-1], altitude[-1], c='red', s=100, label="Final Position")

        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Altitude')
        ax.set_title("Rocket Trajectory")
        ax.legend()

        plt.tight_layout()
        plt.show()

    else:
        print("Error: Missing required columns for 3D plot")
        print("Available columns:", df.columns.tolist())
else:
    print("No data available for plotting")
