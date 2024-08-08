#1.1

import pandas as pd

def generate_car_matrix(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Create a pivot table using id_1, id_2, and car columns
    pivot_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0 and set the diagonal values to 0
    car_matrix = pivot_df.fillna(0).values

    # Create a new DataFrame with the modified car_matrix
    result_df = pd.DataFrame(car_matrix, index=pivot_df.index, columns=pivot_df.columns)

    return result_df

dataset_path = 'dataset-1.csv'
result = generate_car_matrix(dataset_path)
print(result)




#1.2

def get_type_count(dataset):
    df = pd.read_csv(dataset)

    # Add a new categorical column 'car_type' based on the 'car' column values
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default=np.nan), dtype="category")

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count_sorted = dict(sorted(type_count.items()))

    return type_count_sorted

dataset_path = 'dataset-1.csv'
result = get_type_count(dataset_path)
print(result)


#1.3


def get_bus_indexes(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Calculate the mean value of the 'bus' column
    mean_bus = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean value
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    # Sort the indices in ascending order
    bus_indexes_sorted = sorted(bus_indexes)

    return bus_indexes_sorted

# Example usage:
dataset_path = 'dataset-1.csv'
result = get_bus_indexes(dataset_path)
print(result)


#1.4


def filter_routes(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Calculate the average of values in the 'truck' column for each 'route'
    avg_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    selected_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes_sorted = sorted(selected_routes)

    return selected_routes_sorted

# Example usage:
dataset_path = 'path/to/dataset-1.csv'
result = filter_routes(dataset_path)
print(result)



#1.5

def multiply_matrix(car_matrix):
    # Create a copy of the input DataFrame to avoid modifying the original
    modified_matrix = car_matrix.copy()

    # Apply the modification logic
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    return modified_matrix

# Example usage:
# Assuming 'result' is the DataFrame from generate_car_matrix function
modified_result = multiply_matrix(result)
print(modified_result)

#1.6

def check_timestamps_completeness(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Combine date and time columns to create a single timestamp column
    df['startTimestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['endTimestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Check if each pair covers a full 24-hour period and spans all 7 days of the week
    completeness_check = (
        (df['endTimestamp'] - df['startTimestamp'] == pd.Timedelta(days=1)) &
        (df['startTimestamp'].dt.floor('D') == df['endTimestamp'].dt.floor('D')) &
        (df['startTimestamp'].dt.day_name() == df['endTimestamp'].dt.day_name())
    )

    # Create a multi-index boolean series with ('id', 'id_2')
    completeness_series = completeness_check.groupby(['id', 'id_2']).all()

    return completeness_series

# Example usage:
dataset_path = 'path/to/dataset-2.csv'
result = check_timestamps_completeness(dataset_path)
print(result)
