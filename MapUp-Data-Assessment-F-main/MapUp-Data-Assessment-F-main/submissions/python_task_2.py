#2.1

import pandas as pd

def calculate_distance_matrix(dataset):
    # Read the dataset CSV file into a DataFrame
    df = pd.read_csv(dataset)

    # Create a pivot table with 'id_from', 'id_to', and 'distance' columns
    pivot_df = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='sum', fill_value=0)

    # Ensure the matrix is symmetric
    distance_matrix = pivot_df.add(pivot_df.T, fill_value=0)

    # Set diagonal values to 0
    for i in distance_matrix.index:
        distance_matrix.at[i, i] = 0

    return distance_matrix

# Example usage:
dataset_path = 'dataset-3.csv'
result = calculate_distance_matrix(dataset_path)
print(result)

#2.2


import pandas as pd

def unroll_distance_matrix(distance_matrix):
    # Stack the distance matrix to create a Series with multi-index
    stacked_series = distance_matrix.stack()

    # Reset the index to convert index values to columns
    unrolled_df = stacked_series.reset_index()

    # Rename the columns to match the desired output
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Filter out rows where id_start is equal to id_end
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    # Reset the index for the final DataFrame
    unrolled_df.reset_index(drop=True, inplace=True)

    return unrolled_df

# Example usage:
# Assuming 'result' is the DataFrame from calculate_distance_matrix function
result_unrolled = unroll_distance_matrix(result)
print(result_unrolled)


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
# Assuming 'result_unrolled' is the DataFrame from unroll_distance_matrix function
reference_value = 1  # Replace with the desired reference value
result = find_ids_within_ten_percentage_threshold(result_unrolled, reference_value)
print(result)



#2.4

import pandas as pd

def calculate_toll_rate(distance_df):
    # Create a copy of the input DataFrame to avoid modifying the original
    toll_df = distance_df.copy()

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
        toll_df[vehicle_type] = distance_df['distance'] * rate_coefficient

    return toll_df

# Example usage:
# Assuming 'result_unrolled' is the DataFrame from unroll_distance_matrix function
result_with_toll = calculate_toll_rate(result_unrolled)
print(result_with_toll)


#2.5

import pandas as pd

def calculate_time_based_toll_rates(distance_df):
    # Create a copy of the input DataFrame to avoid modifying the original
    time_based_toll_df = distance_df.copy()

    # Extract day and time information
    time_based_toll_df['start_day'] = time_based_toll_df['start_timestamp'].dt.day_name()
    time_based_toll_df['start_time'] = time_based_toll_df['start_timestamp'].dt.time
    time_based_toll_df['end_day'] = time_based_toll_df['end_timestamp'].dt.day_name()
    time_based_toll_df['end_time'] = time_based_toll_df['end_timestamp'].dt.time

    # Define time ranges and discount factors for weekdays and weekends
    weekdays_time_ranges = [
        ('00:00:00', '10:00:00', 0.8),
        ('10:00:00', '18:00:00', 1.2),
        ('18:00:00', '23:59:59', 0.8)
    ]
    weekends_time_ranges = [('00:00:00', '23:59:59', 0.7)]

    # Apply time-based discount factors for weekdays and weekends
    for start_range, end_range, discount_factor in weekdays_time_ranges:
        mask = (time_based_toll_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])) & \
               (time_based_toll_df['start_time'] >= pd.to_datetime(start_range).time()) & \
               (time_based_toll_df['start_time'] <= pd.to_datetime(end_range).time())
        time_based_toll_df.loc[mask, time_based_toll_df.columns[5:]] *= discount_factor

    for start_range, end_range, discount_factor in weekends_time_ranges:
        mask = (time_based_toll_df['start_day'].isin(['Saturday', 'Sunday'])) & \
               (time_based_toll_df['start_time'] >= pd.to_datetime(start_range).time()) & \
               (time_based_toll_df['start_time'] <= pd.to_datetime(end_range).time())
        time_based_toll_df.loc[mask, time_based_toll_df.columns[5:]] *= discount_factor

    return time_based_toll_df

# Example usage:
# Assuming 'result' is the DataFrame from check_timestamp_completeness function
result_with_time_based_toll = calculate_time_based_toll_rates(result)
print(result_with_time_based_toll)