import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler


def find_missing_values(df):
    """
    Finds missing values and returns a summary.

    Args:
        df: The DataFrame to check for missing values.

    Returns:
        A summary of missing values, including the number of missing values per column.
    """

    null_counts = df.isnull().sum()
    missing_value = null_counts
    percent_of_missing_value = 100 * null_counts / len(df)
    data_type=df.dtypes

    missing_data_summary = pd.concat([missing_value, percent_of_missing_value,data_type], axis=1)
    missing_data_summary_table = missing_data_summary.rename(columns={0:"Missing values", 1:"Percent of Total Values",2:"DataType" })
    missing_data_summary_table = missing_data_summary_table[missing_data_summary_table.iloc[:, 1] != 0].sort_values('Percent of Total Values', ascending=False).round(1)

    print(f"From {df.shape[1]} columns selected, there are {missing_data_summary_table.shape[0]} columns with missing values.")

    return missing_data_summary_table

def replace_missing_values(data):
  """
  Replaces missing values in a DataFrame with the mean for numeric columns and the mode for categorical columns.

  Args:
    data: The input DataFrame.

  Returns:
    The DataFrame with missing values replaced.
  """

  # Identify numeric and categorical columns
  numeric_columns = data.select_dtypes(include='number').columns
  categorical_columns = data.select_dtypes(include='object').columns

  # Replace missing values in numeric columns with the mean
  for column in numeric_columns:
    column_mean = data[column].mean()
    data[column] = data[column].fillna(column_mean)

  # Replace missing values in categorical columns with the mode
  for column in categorical_columns:
    column_mode = data[column].mode().iloc[0]
    data[column] = data[column].fillna(column_mode)

  return data

def convertByteIntoMegaByte(data):
    # We Have to convert some the data into MB or TB or GB
    megabyte=1*10e+5
    data['Bearer Id']=data['Bearer Id']/megabyte
    data['IMSI']=data['IMSI']/megabyte
    data['MSISDN/Number']=data['MSISDN/Number']/megabyte
    data['IMEI']=data['IMEI']/megabyte
    for column in data.columns:
        if 'Bytes' in column:
            data[column]=data[column]/megabyte
    return data


def get_outlier_summary(data):
    """
    Calculates outlier summary statistics for a DataFrame.

    Args:
        data : Input DataFrame.

    Returns:
        Outlier summary DataFrame.
    """

    outlier_summary = pd.DataFrame(columns=['Variable', 'Number of Outliers'])
    data = data.select_dtypes(include='number')

    for column_name in data.columns:
        q1 = data[column_name].quantile(0.25)
        q3 = data[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[column_name] < lower_bound) | (data[column_name] > upper_bound)]

        outlier_summary = pd.concat(
            [outlier_summary, pd.DataFrame({'Variable': [column_name], 'Number of Outliers': [outliers.shape[0]]})],
            ignore_index=True
        )
    non_zero_count = (outlier_summary['Number of Outliers'] > 0).sum()
    print(f"From {data.shape[1]} selected numerical columns, there are {non_zero_count} columns with outlier values.")

    return outlier_summary

def getBoxPlotToCheckOutlier(xdr_data,variables):
    for variable in variables:
        sns.boxplot(data=xdr_data[variable], orient='v')
        plt.title(f'Box Plot {variable}')
        plt.xlabel('Values')
        plt.ylabel(variable)
        plt.show()

def remove_outliers_winsorization(xdr_data):
    """
    Removes outliers from specified columns of a DataFrame using winsorization.

    Args:
        data: The input DataFrame.
        column_names (list): A list of column names to process.

    Returns:
        The DataFrame with outliers removed.
    """
    # data = xdr_data.select_dtypes(include='number')
    for column_name in xdr_data.select_dtypes(include='number').columns:
        q1 = xdr_data[column_name].quantile(0.25)
        q3 = xdr_data[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        xdr_data[column_name] = xdr_data[column_name].clip(lower_bound, upper_bound)

    return xdr_data

def aggregate_xdr_data(data):
    """Aggregates xDR data per user and application.

    Args:
        The xDR data.

    Returns:
        The aggregated xDR data.

    """
    agg_xdr_data=pd.DataFrame(data)
    agg_xdr_data['Total_DL_and_UL_data'] = agg_xdr_data['Total DL (Bytes)'] + agg_xdr_data['Total UL (Bytes)']
    agg_xdr_data['Social Media Data'] = agg_xdr_data['Social Media DL (Bytes)']+agg_xdr_data['Social Media UL (Bytes)']
    agg_xdr_data['Google Data'] = agg_xdr_data['Google DL (Bytes)']+agg_xdr_data['Gaming UL (Bytes)']
    agg_xdr_data['Email Data']=agg_xdr_data['Email DL (Bytes)']+agg_xdr_data['Email UL (Bytes)']
    agg_xdr_data['YouTube Data']=agg_xdr_data['Email DL (Bytes)']+agg_xdr_data['Email UL (Bytes)']
    agg_xdr_data['Netflix Data']=agg_xdr_data['Netflix DL (Bytes)']+agg_xdr_data['Netflix UL (Bytes)']
    agg_xdr_data['Gaming Data']=agg_xdr_data['Gaming DL (Bytes)']+agg_xdr_data['Gaming UL (Bytes)']
    agg_xdr_data['Other Data'] = agg_xdr_data['Other DL (Bytes)']+agg_xdr_data['Other UL (Bytes)']

    columns = ['MSISDN/Number', 'Dur. (ms)','Bearer Id','Other Data','Gaming Data','Netflix Data','YouTube Data','Email Data', 'Google Data','Social Media Data', 'Total_DL_and_UL_data']

    df = agg_xdr_data[columns]

    # Aggregate data
    aggregated_df = df.groupby('MSISDN/Number').agg(
        Total_DL_And_UL=('Total_DL_and_UL_data', sum),
        Total_Social_Media_Data=('Social Media Data',sum),
        Total_Google_Data=('Google Data', sum),
        Total_Email_Data=('Email Data',sum),
        Total_YouTube_Data=('YouTube Data', sum),
        Total_Netflix_Data=('Netflix Data',sum),
        Total_Gaming_Data=('Gaming Data', sum),
        Total_Other_Data=('Other Data',sum),
        Total_Duration_Data=('Dur. (ms)',sum),
        Total_xDR_Sessions=('Bearer Id',sum)
    )

    return aggregated_df

def segment_users_and_calculate_total_data(data):
  """
  Segments users into the top five decile classes based on total session duration and calculates the total data (DL+UL) per decile class.

  Args:
    data: The input DataFrame containing user information data.

  Returns:
    A DataFrame with decile class and total data per decile class.
  """

  # Calculate total DL and UL data per user
  data['Total_DL_+_UL'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']

  # Segment users into top five decile classes based on total session duration
  decile_labels = ['Decile 1', 'Decile 2', 'Decile 3', 'Decile 4', 'Decile 5']
  data['decile_class'] = pd.qcut(data['Dur. (ms)'], 5, labels=decile_labels)

  # Calculate total data per decile class
  total_data_per_decile = data.groupby('decile_class')['Total_DL_+_UL'].sum()

  return total_data_per_decile

def compute_dispersion_parameters(data):
  """
  Computes various dispersion parameters for a DataFrame.

  Args:
    data : The input DataFrame.

  Returns:
    A DataFrame containing dispersion parameters for each numeric column.
  """

  numeric_columns = data.select_dtypes(include='number').columns

  dispersion_params = pd.DataFrame(index=['Range', 'Variance', 'Std Dev', 'IQR', 'Coef Var'], columns=numeric_columns)

  for column in numeric_columns:
    dispersion_params.loc['Range', column] = data[column].max() - data[column].min()
    dispersion_params.loc['Variance', column] = data[column].var()
    dispersion_params.loc['Std Dev', column] = data[column].std()
    dispersion_params.loc['IQR', column] = data[column].quantile(0.75) - data[column].quantile(0.25)
    dispersion_params.loc['Coef Var', column] = data[column].std() / data[column].mean()

  return dispersion_params

def plot_dispersion_parameters(dispersion_results,applications):
    for application in applications:
      sns.barplot(data=dispersion_results[application])
      plt.title('Dispersion Parameters')
      plt.xlabel(application)
      plt.ylabel('Value')
      plt.xticks(rotation=45)
      plt.show()

def correlationBetweenApplication(data):
        agg_xdr_data = pd.DataFrame(data)
        agg_xdr_data['Social Media Data'] = agg_xdr_data['Social Media DL (Bytes)']+agg_xdr_data['Social Media UL (Bytes)']
        agg_xdr_data['Google Data'] = agg_xdr_data['Google DL (Bytes)']+agg_xdr_data['Gaming UL (Bytes)']
        agg_xdr_data['Email Data']=agg_xdr_data['Email DL (Bytes)']+agg_xdr_data['Email UL (Bytes)']
        agg_xdr_data['YouTube Data']=agg_xdr_data['Email DL (Bytes)']+agg_xdr_data['Email UL (Bytes)']
        agg_xdr_data['Netflix Data']=agg_xdr_data['Netflix DL (Bytes)']+agg_xdr_data['Netflix UL (Bytes)']
        agg_xdr_data['Gaming Data']=agg_xdr_data['Gaming DL (Bytes)']+agg_xdr_data['Gaming UL (Bytes)']
        agg_xdr_data['Other Data'] = agg_xdr_data['Other DL (Bytes)']+agg_xdr_data['Other UL (Bytes)']
        return agg_xdr_data;

def analyze_user_engagement(data):
    """
    Analyzes user engagement based on session metrics and segments users into clusters.

    Args:
      data: The input DataFrame containing user data.

    Returns:
      A DataFrame with segmented users and engagement metrics.
    """

    # Aggregate metrics per customer ID
    aggregated_data = data.groupby('MSISDN/Number').agg({'Bearer Id': 'sum',
                                                        'Dur. (ms)': 'sum',
                                                        'Total_DL_+_UL': 'sum'})

  
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(aggregated_data)

    normalized_data = pd.DataFrame(normalized_data)

    # K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(normalized_data)
    aggregated_data['clusters'] = clusters

    # Compute minimum, maximum, average, and total metrics per cluster
    cluster_stats = aggregated_data.groupby('clusters').agg(['min', 'max', 'mean', 'sum'])

    # Aggregate user total traffic per application
    traffic_per_app = data.groupby(['MSISDN/Number','Google DL (Bytes)','Google UL (Bytes)','Email DL (Bytes)','Email UL (Bytes)','Youtube UL (Bytes)','Youtube DL (Bytes)', 'Netflix DL (Bytes)','Netflix UL (Bytes)','Gaming DL (Bytes)','Gaming UL (Bytes)','Other UL (Bytes)'])['Total_DL_+_UL'].sum().reset_index()
    top_10_most_engaged_users = traffic_per_app.groupby(['MSISDN/Number','Google DL (Bytes)','Google UL (Bytes)','Email DL (Bytes)','Email UL (Bytes)','Youtube UL (Bytes)','Youtube DL (Bytes)', 'Netflix DL (Bytes)','Netflix UL (Bytes)','Gaming DL (Bytes)','Gaming UL (Bytes)','Other UL (Bytes)'])['Total_DL_+_UL'].sum().nlargest(10)

    return aggregated_data, cluster_stats, top_10_most_engaged_users,normalized_data,clusters



def aggregate_average_xdr_data(data):
    # Aggregate data
    aggregated_average_df = data.groupby('MSISDN/Number').agg({
                                                            'TCP DL Retrans. Vol (Bytes)':'mean',
                                                            'TCP UL Retrans. Vol (Bytes)':'mean',
                                                            'Avg RTT DL (ms)':'mean',
                                                            'Avg RTT UL (ms)':'mean',
                                                            'Avg Bearer TP DL (kbps)':'mean',
                                                            'Avg Bearer TP UL (kbps)':'mean',
                                                            'Handset Type':'first'
                                                        })
    select_columns=aggregated_average_df[ ['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)','Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)']]
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(select_columns)

    normalized_data = pd.DataFrame(normalized_data)

    # K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(normalized_data)
    aggregated_average_df['clusters'] = clusters

    return aggregated_average_df,clusters


def find_top_bottom_frequent(data, column_name, n=10):
    """
    Finds the top n, bottom n, and most frequent values for a given column.

    Args:
        data: The input DataFrame.
        column_name: The name of the column to analyze.
        n: The number of values to find.

    Returns:
        A tuple containing the top n, bottom n, and most frequent values.
    """

    top_n = data[column_name].nlargest(n)
    bottom_n = data[column_name].nsmallest(n)
    most_frequent = data[column_name].value_counts().head(n)

    return top_n, bottom_n, most_frequent

def analyze_handset_throughput_metrics(data,avg_throughput):
  """
  Analyzes the distribution of average throughput  view per handset type.

  Args:
    data: The input DataFrame containing handset data.
  """

  # Calculate average throughput  count per handset type
  avg_throughput_DL_by_handset = data.groupby('Handset Type')[avg_throughput].mean()

  # Print the results
  print("Average Throughput per Handset Type:\n")
  print(avg_throughput_DL_by_handset.to_markdown())


def analyze_handset_retrasmission_metrics(data,tcp_retransmission):
  """
  Analyzes the distribution of average TCP retransmission view per handset type.

  Args:
    data The input DataFrame containing handset data.
  """

  avg_retransmission_by_handset = data.groupby('Handset Type')[tcp_retransmission].mean()


  print("\nAverage TCP Retransmission Count per Handset Type:\n")
  print(avg_retransmission_by_handset.to_markdown())


def assign_engagement_experience_scores(data, engagement_clusters,experience_clusters):
  """
  Assigns engagement and experience scores to users based on Euclidean distance.

  Args:
    data: The input DataFrame containing user data.
    engagement_clusters: The DataFrame with engagement clusters.
    experience_clusters: The DataFrame with experience clusters.

  Returns:
    A DataFrame with assigned engagement and experience scores.
  """
  engagement_clusters = engagement_clusters.drop('clusters', axis=1)
  experience_clusters = experience_clusters.drop(['clusters','Handset Type'], axis=1)

  engagement_distances = euclidean_distances(data[['Bearer Id','Dur. (ms)','Total_DL_+_UL']], engagement_clusters.iloc[0].values.reshape(1, -1))
  experience_distances = euclidean_distances(data[['TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)','Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)']], experience_clusters.iloc[2].values.reshape(1, -1))

  data['engagement_score'] = engagement_distances.min(axis=1)
  data['experience_score'] = experience_distances.min(axis=1)

  return data

def calculate_satisfaction_score(data):
    """
    Calculates a satisfaction score based on engagement and experience scores.

    Args:
        data: The input DataFrame containing user data.

    Returns:
        A Series with satisfaction scores for each user.
    """

    data['satisfaction_score'] = (data['engagement_score'] + data['experience_score']) / 2
    return data

def find_top_satisfied_customers(data, n=10):
    """
    Finds the top n satisfied customers based on their satisfaction score.

    Args:
        data : The input DataFrame containing user data.
        n: The number of top customers to find.

    Returns:
         A Series with the top n customer IDs.
    """

    top_satisfied = data.nlargest(n, 'satisfaction_score')['MSISDN/Number']
    return top_satisfied


def build_regression_model(data):
  """
  Builds a regression model to predict satisfaction score.

  Args:
    data : The input DataFrame containing user data.

  Returns:
  A tuple containing the trained model, R-squared score, and mean squared error.
  """

  # Split data into features and target variable
  X = data[['engagement_score', 'experience_score']]
  y = data['satisfaction_score']

  # Split data into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Create and train a linear regression model
  model = LinearRegression()
  model.fit(X_train, y_train)

  # Make predictions on the test set
  y_pred = model.predict(X_test)

  # Evaluate the model
  mse = mean_squared_error(y_test, y_pred)
  r2 = r2_score(y_test, y_pred)

  return model, r2, mse

def segment_users_k_means(data):
  """
  Segments users into two clusters based on engagement and experience scores.

  Args:
    data: The input DataFrame containing user data.

  Returns:
    A DataFrame with segmented users.
  """

  # Select relevant columns
  engagement_experience_metrics = data[['engagement_score', 'experience_score']]

  # Standardize the data
  scaler = StandardScaler()
  scaled_data = scaler.fit_transform(engagement_experience_metrics)

  # Perform k-means clustering
  kmeans = KMeans(n_clusters=2, random_state=42)
  clusters = kmeans.fit_predict(scaled_data)

  # Add cluster labels to the original DataFrame
  data['engagement_experience_segment'] = clusters

  return data

def aggregate_cluster_scores(data):
  """
  Aggregates the average satisfaction and experience scores per cluster.

  Args:
    data: The input DataFrame containing user data.

  Returns:
   A DataFrame with aggregated cluster scores.
  """

  cluster_stats = data.groupby('engagement_experience_segment')[['satisfaction_score', 'experience_score']].mean()
  return cluster_stats