#2.1

import pandas as pd

def calculate_distance_matrix(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Create a pivot table with 'id_from', 'id_to', and 'distance' columns
    pivot_df = df.pivot_table(index='id_from', columns='id_to', values='distance', aggfunc='sum', fill_value=0)

    # Ensure the matrix is symmetric
    distance_matrix = pivot_df.add(pivot_df.T, fill_value=0)

    # Set diagonal values to 0
    for i in distance_matrix.index:
        distance_matrix.at[i, i] = 0

    return distance_matrix

# Example usage:
dataset_path = 'path/to/dataset-3.csv'
result = calculate_distance_matrix(dataset_path)
print(result)

#2.2


def unroll_distance_matrix(distance_matrix):
    # Reset the index to convert index values to columns
    distance_matrix = distance_matrix.reset_index()

    # Melt the DataFrame to unroll the distance matrix
    unrolled_df = pd.melt(distance_matrix, id_vars='id_from', var_name='id_to', value_name='distance')

    # Rename the columns to match the desired output
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Filter out rows where id_start is equal to id_end
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    # Reset the index for the final DataFrame
    unrolled_df.reset_index(drop=True, inplace=True)

    return unrolled_df

# Example usage:
# Assuming 'result' is the DataFrame from calculate_distance_matrix function
unrolled_result = unroll_distance_matrix(result)
print(unrolled_result)

#2.3


def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    # Filter the DataFrame based on the reference value in 'id_start' column
    reference_df = distance_df[distance_df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    average_distance = reference_df['distance'].mean()

    # Calculate the threshold values
    lower_threshold = 0.9 * average_distance
    upper_threshold = 1.1 * average_distance

    # Filter out values within 10% threshold (including ceiling and floor)
    filtered_ids = distance_df[
        (distance_df['distance'] >= lower_threshold) &
        (distance_df['distance'] <= upper_threshold)
    ]['id_start'].unique()

    # Sort the list of values
    filtered_ids_sorted = sorted(filtered_ids)

    return filtered_ids_sorted

# Example usage:
# Assuming 'unrolled_result' is the DataFrame from unroll_distance_matrix function
reference_value = 1  # Replace with the desired reference value
result = find_ids_within_ten_percentage_threshold(unrolled_result, reference_value)
print(result)



#2.4

import pandas as pd

def calculate_toll_rate(distance_matrix):
    # Create a copy of the input DataFrame to avoid modifying the original
    toll_df = distance_matrix.copy()

    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        toll_df[vehicle_type] = distance_matrix['distance'] * rate_coefficient

    return toll_df

# Example usage:
# Assuming 'result' is the DataFrame from calculate_distance_matrix function
result_with_toll = calculate_toll_rate(result)
print(result_with_toll)

#2.5

def generate_car_matrix(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Create a pivot table using id_1, id_2, and car columns
    pivot_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0 and set the diagonal values to 0
    car_matrix = pivot_df.fillna(0).values
    for i in range(min(car_matrix.shape)):
        car_matrix[i, i] = 0

    # Create a new DataFrame with the modified car_matrix
    result_df = pd.DataFrame(car_matrix, index=pivot_df.index, columns=pivot_df.columns)

    return result_df

# Example usage:
dataset_path = 'path/to/dataset-1.csv'
result = generate_car_matrix(dataset_path)
print(result)