import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# from streamlit_option_menu import option_menu
import os
os.chdir('..')
from src.dbconnection import get_dataFrame_from_database

# xdr_data = get_dataFrame_from_database()
# xdr_data_from_csv
xdr_data= pd.read_csv('docs/Week2_challenge_data_source(CSV).csv')
st.set_page_config(page_title="Dashboard")
# Set page title
st.title("Telecom Data Analysis")
st.markdown("##")


st.sidebar.header('Telecommunication')
st.sidebar.write("Telecom dataset analysized as follow:")
st.sidebar.success('Exploratory Data Analysis (EDA)')
st.sidebar.success('User Over view Analysis')
st.sidebar.success('User Engagement Analysis')
st.sidebar.success('User Experience Analysis')
st.sidebar.success('User Satisfaction Analysis')
# Show first few rows of the dataset
st.success("Initial Telecom Dataset")
st.write(xdr_data)

st.title("Exploratory Data Analysis")
st.success("Describe all telecom numerical values")
st.write(xdr_data.describe())
st.subheader("Check datatype of extracted dataset")
dataType_of_Dataset = st.selectbox("Choose a column to view its datatype", xdr_data.columns)

if st.button("View Datatype"):
    st.write(xdr_data[dataType_of_Dataset].dtypes)

st.write('...............................................................................................................................................................................................................................................................')

from scripts.tellcoAnalysis import find_missing_values,replace_missing_values,get_outlier_summary,remove_outliers_winsorization,aggregate_xdr_data,segment_users_and_calculate_total_data,compute_dispersion_parameters,correlationBetweenApplication,analyze_user_engagement,aggregate_average_xdr_data,find_top_bottom_frequent,assign_engagement_experience_scores,calculate_satisfaction_score,find_top_satisfied_customers,build_regression_model,segment_users_k_means,aggregate_cluster_scores,convertByteIntoMegaByte


st.subheader("List missing values")
missing_summary = find_missing_values(xdr_data)
st.write(missing_summary.head(missing_summary.size))

st.success("Replaced missing value (numerical value with mean and categorical with mode)")
xdr_data = replace_missing_values(xdr_data)
missing_summary = find_missing_values(xdr_data)
st.write(missing_summary.head(missing_summary.size))
        

st.subheader("List outlier values")
outlier_summary = get_outlier_summary(xdr_data)
st.write(outlier_summary.head(outlier_summary.size))  
st.subheader("Box-plot before removing outliers")
def boxPlotBeforeRemovingOutlier(applications):
    for application in applications:
        fig, ax = plt.subplots()
        st.success(application)
        st.write(sns.boxplot(x=xdr_data[application],orient='h'))
        st.pyplot(fig)
boxPlotBeforeRemovingOutlier(['Dur. (ms)','Avg RTT DL (ms)','Avg RTT UL (ms)','Nb of sec with 37500B < Vol UL','Nb of sec with 1250B < Vol UL < 6250B','Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)','TCP DL Retrans. Vol (Bytes)','TCP UL Retrans. Vol (Bytes)'])
st.subheader("Removed outlier values")
xdr_data = remove_outliers_winsorization(xdr_data)
outlier_summary = get_outlier_summary(xdr_data)
st.write(outlier_summary.head(outlier_summary.size)) 

st.subheader("Box-plot after outliers removed")

fig, ax = plt.subplots()
column_to_plot = st.selectbox("Select a column for the box-plot:",xdr_data.columns)
st.success(column_to_plot)
st.write(sns.boxplot(x=xdr_data[column_to_plot],orient='v'))
st.pyplot(fig)

xdr_data = convertByteIntoMegaByte(xdr_data)
st.subheader("Telecom dataset After Removing missing and outlier values")
st.success("Converted data(bytes) into Megabytes")
st.write(xdr_data)

st.title("User Over view analysis")
top_handsets = xdr_data['Handset Type'].value_counts().head(10)
top_manufacturers = xdr_data['Handset Manufacturer'].value_counts().head(3)
st.success('Top Ten handset types')
st.write(top_handsets)
st.bar_chart(top_handsets)
st.success('Top three handset manufacturers')
st.write(top_manufacturers)
st.bar_chart(top_manufacturers)

st.subheader('The top 5 handset type per top 3 handset manufacturer')
filtered_data = xdr_data[xdr_data['Handset Manufacturer'].isin(top_manufacturers.index)]
for h_manufacturer in top_manufacturers.index:
    fig, ax = plt.subplots(figsize=(18,6))
    top_5_handsets_per_manufacturer = filtered_data[filtered_data['Handset Manufacturer']==h_manufacturer]['Handset Type'].value_counts().head(5)
    st.success(h_manufacturer)
    st.write(top_5_handsets_per_manufacturer)
    st.write(sns.barplot(top_5_handsets_per_manufacturer))
    st.pyplot(fig)
    
st.subheader('Aggregate Each Application per User')
aggregated_xdr_data=aggregate_xdr_data(xdr_data)
st.dataframe(aggregated_xdr_data)

st.subheader('Exploratory Data Analysis (EDA) on Aggregated Application per User Data')
st.dataframe(aggregated_xdr_data.describe())

st.subheader('Variable transformations')
st.success('Segment the users into the top five decile classes and Calculate Total Data per Decile Class')    
total_data_per_decile = segment_users_and_calculate_total_data(xdr_data)
st.bar_chart(total_data_per_decile)
st.subheader("Univariate Analysis: Dispersion Parameters")
dispersion_results = compute_dispersion_parameters(xdr_data)
st.write(dispersion_results)
st.subheader('Univariate Analysis: Graphical Dispersion Parameters Analysis')
def graphicalDispersionParametersAnalysis(applications):
    for application in applications:
        st.success(application)
        st.bar_chart(dispersion_results[application])
graphicalDispersionParametersAnalysis(['Avg RTT DL (ms)','Avg RTT UL (ms)','HTTP DL (Bytes)','HTTP UL (Bytes)','Social Media DL (Bytes)','Social Media UL (Bytes)','Youtube DL (Bytes)','Youtube UL (Bytes)','Netflix DL (Bytes)','Netflix UL (Bytes)','Google DL (Bytes)', 'Google UL (Bytes)','Email DL (Bytes)', 'Email UL (Bytes)', 'Gaming DL (Bytes)', 'Gaming UL (Bytes)', 'Other UL (Bytes)', 'Other DL (Bytes)'])

st.subheader('Bivariate Analysis:')
st.success('Using correlation between applications and Total DL and UL')
def bivariateAnalysisbetweenApplicationAndTotalDL_UL():
    fig, ax = plt.subplots(figsize=(20,8))
    correlation_matrix = xdr_data[['Total_DL_+_UL','Social Media DL (Bytes)','Social Media UL (Bytes)','Youtube DL (Bytes)','Youtube UL (Bytes)','Netflix DL (Bytes)','Netflix UL (Bytes)','Google DL (Bytes)', 'Google UL (Bytes)','Email DL (Bytes)', 'Email UL (Bytes)', 'Gaming DL (Bytes)', 'Gaming UL (Bytes)', 'Other UL (Bytes)', 'Other DL (Bytes)']].corr()
    st.write(sns.heatmap(correlation_matrix,annot=True,cmap='viridis'))
    st.pyplot(fig)
bivariateAnalysisbetweenApplicationAndTotalDL_UL()

st.subheader('Correlation Analysis:')
st.success('Computing a Correlation Matrix for Each Applications')
applicationData=correlationBetweenApplication(xdr_data)
def correlationBetweenEachApplications():
    fig, ax = plt.subplots()
    correlation_matrix_app = applicationData[['Social Media Data', 'Google Data', 'Email Data', 'YouTube Data', 'Netflix Data', 'Gaming Data', 'Other Data']].corr()
    st.write(sns.heatmap(correlation_matrix_app,annot=True,cmap='viridis',))
    st.pyplot(fig)
correlationBetweenEachApplications()


from sklearn.decomposition import PCA

st.subheader('Principal Component Analysis (PCA):')
st.success('For Dimensionality Reduction')
# Select only the desired columns
data_selected = applicationData[['Social Media Data', 'Google Data', 'Email Data', 'YouTube Data', 'Netflix Data', 'Gaming Data', 'Other Data']]

data_standardized = (data_selected - data_selected.mean()) / data_selected.std()

# Perform PCA
pca = PCA(n_components=2) 
principal_components = pca.fit_transform(data_standardized)

principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

final_df = pd.concat([principal_df, xdr_data], axis=1)

st.dataframe(final_df)

aggregated_data_user_engagement, cluster_stats_user_engagement, top_10_most_engaged_users,normalized_data,engagement_clusters = analyze_user_engagement(xdr_data)

st.title('User Engagement Analysis ')

st.subheader('Aggregate session metrics (session freq, session duration and total session) per customer')
st.dataframe(aggregated_data_user_engagement.head())

st.success('Top 10 most engaged users per application')
st.dataframe(top_10_most_engaged_users.head())

st.subheader('After Aggregated, Segment users into three clusters')
cluster_one = aggregated_data_user_engagement[aggregated_data_user_engagement['clusters']==0]
cluster_two = aggregated_data_user_engagement[aggregated_data_user_engagement['clusters']==1]
cluster_three = aggregated_data_user_engagement[aggregated_data_user_engagement['clusters']==2]
st.success('User Engagement First Cluster')
st.write(cluster_one)
st.success('User Engagement Second Cluster')

st.write(cluster_two)
st.success('User Engagement Third Cluster')
st.write(cluster_three)

st.subheader('Segmented user into clusters:')
st.success('Cluster metrics')
st.dataframe(cluster_stats_user_engagement.head())

top_frequency = aggregated_data_user_engagement['Bearer Id'].nlargest(10)
top_duration = aggregated_data_user_engagement['Dur. (ms)'].nlargest(10)
top_traffic = aggregated_data_user_engagement['Total_DL_+_UL'].nlargest(10)

st.success('Top Ten sessions frequencies')
st.write(top_frequency)
st.bar_chart(top_frequency)
st.success('Top Ten sessions durations')
st.write(top_duration)
st.success('Top Ten sessions traffics')
st.write(top_traffic)
st.bar_chart(top_traffic)

st.success('Top Three most used Applications')
top_three_apps = xdr_data[['Google DL (Bytes)','Google UL (Bytes)','Email DL (Bytes)','Email UL (Bytes)','Youtube UL (Bytes)','Youtube DL (Bytes)', 'Netflix DL (Bytes)','Netflix UL (Bytes)','Gaming DL (Bytes)','Gaming UL (Bytes)','Other UL (Bytes)']].sum().nlargest(3)
st.write(top_three_apps)
st.bar_chart(top_three_apps)

st.title('Experience Analytics')
st.success('Aggregate average TCP,RTT,TP and Handset type per user')
aggregated_average_experience_analysis,experience_clusters = aggregate_average_xdr_data(xdr_data)

st.dataframe(aggregated_average_experience_analysis)


# Handset Type Distribution
st.success("Handset Type Distribution")
handset_counts = aggregated_average_experience_analysis['Handset Type'].value_counts()
st.bar_chart(handset_counts)

st.success('Top, Bottom, and Most frequent values for TCP, RTT, and throughput')


# Find top, bottom, and most frequent values for TCP, RTT, and throughput
top_tcp_DL, bottom_tcp_DL, frequent_tcp_DL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'TCP DL Retrans. Vol (Bytes)')
top_tcp_UL, bottom_tcp_UL, frequent_tcp_UL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'TCP UL Retrans. Vol (Bytes)')
top_rtt_DL, bottom_rtt_DL, frequent_rtt_DL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'Avg RTT DL (ms)')
top_rtt_UL, bottom_rtt_UL, frequent_rtt_UL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'Avg RTT UL (ms)')
top_throughput_DL, bottom_throughput_DL, frequent_throughput_DL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'Avg Bearer TP DL (kbps)')
top_throughput_UL, bottom_throughput_UL, frequent_throughput_UL = find_top_bottom_frequent(aggregated_average_experience_analysis, 'Avg Bearer TP UL (kbps)')
st.success('Top TCP')
st.write(top_tcp_DL,top_tcp_UL)
st.success('Bottom TCP')
st.write(bottom_tcp_DL,bottom_tcp_UL)
st.success('Frequent TCP')
st.write(frequent_tcp_DL,frequent_tcp_UL)
st.success('Top RTT')
st.write(top_rtt_DL,top_rtt_UL)
st.success('Bottom RTT')
st.write(bottom_rtt_DL,bottom_rtt_UL)
st.success('Frequent RTT')
st.write(frequent_rtt_DL,frequent_rtt_UL)
st.success('Top Throughput')
st.write(top_throughput_DL,top_throughput_UL)
st.success('Bottom Throughput')
st.write(bottom_throughput_DL,bottom_throughput_UL)
st.success('Frequent Throughput')
st.write(frequent_throughput_DL,frequent_throughput_UL)

st.subheader('The distribution of average Throughput per Handset type')
def analyze_handset_throughput_metrics(data,avg_throughput):
    avg_retransmission_by_handset = data.groupby('Handset Type')[avg_throughput].mean()
    st.success("Average Throughput per Handset Type")
    st.write(avg_retransmission_by_handset)
analyze_handset_throughput_metrics(xdr_data,'Avg Bearer TP DL (kbps)')
analyze_handset_throughput_metrics(xdr_data,'Avg Bearer TP UL (kbps)')

st.subheader('Average TCP retransmission view per handset type')
def analyze_handset_retrasmission_metrics(data,tcp_retrans):
    avg_retransmission_by_handset = data.groupby('Handset Type')[tcp_retrans].mean()
    st.success("Average TCP Retransmission per Handset Type")
    st.write(avg_retransmission_by_handset)

analyze_handset_retrasmission_metrics(xdr_data,'TCP DL Retrans. Vol (Bytes)')
analyze_handset_retrasmission_metrics(xdr_data,'TCP UL Retrans. Vol (Bytes)')

st.subheader('Aggregated experience Cluster analysis')
cluster_1 = aggregated_average_experience_analysis[aggregated_average_experience_analysis['clusters'] == 0]
cluster_2 = aggregated_average_experience_analysis[aggregated_average_experience_analysis['clusters'] == 1]
cluster_3 = aggregated_average_experience_analysis[aggregated_average_experience_analysis['clusters'] == 2]
st.success("First cluster of Aggregated experience")
st.write(cluster_1)
st.success("Second cluster of Aggregated experience")
st.write(cluster_2)
st.success("Third cluster of Aggregated experience")
st.write(cluster_3)

st.title("Satisfaction Analysis")
st.success("Assign engagement and experience scores to users to calculate user satisfaction")
data_with_scores = assign_engagement_experience_scores(xdr_data, aggregated_data_user_engagement,aggregated_average_experience_analysis)

st.write(data_with_scores)

st.subheader('Calculated satisfaction score based on the average of engagement and experience scores')
st.write('Data with satisfaction score')
data_with_satisfaction = calculate_satisfaction_score(xdr_data)
st.write(data_with_satisfaction)
st.success('Top 10 satisfied customers')
top_satisfied_customers = find_top_satisfied_customers(data_with_satisfaction, 10)
st.write(top_satisfied_customers)
st.subheader('Build a regression model to predict customer satisfaction scores based on engagement and experience')
model, r2, mse = build_regression_model(xdr_data)
st.write("R-squarea and MSE of Regression Model")
st.write("R-squared:", r2)
st.write("Mean Squared Error:", mse)

st.subheader("Make predictions")
def getEngagementAndExperienceScore(engagement_score,experience_score):
    new_user_data = pd.DataFrame({'engagement_score': [engagement_score],
                             'experience_score': [experience_score]})
    return new_user_data
engagement_score=st.number_input('engagement_score')
experience_score=st.number_input('experience_score')
# Make predictions using the trained model
# st.write("The predicted satisfaction score of engagement_score = 0.8 and experience_score = 0.5")
if st.button("Predict satisfaction score"):
    new_user_data=getEngagementAndExperienceScore(engagement_score,experience_score)
    predicted_satisfaction_score = model.predict(new_user_data)
    st.success(f"The Predicted satisfaction score of {engagement_score} and {experience_score} is {predicted_satisfaction_score}")
    # st.write("Predicted satisfaction score:", predicted_satisfaction_score)

st.subheader("Segment users into two clusters based on engagement and experience scores using k-means clustering")
segmented_data = segment_users_k_means(xdr_data)
cluster_segmented_1=segmented_data[segmented_data['engagement_experience_segment']==0]
cluster_segmented_2=segmented_data[segmented_data['engagement_experience_segment']==1]
st.success("First cluster based on engagement and experience scores")
st.write(cluster_segmented_1)
st.success("Second cluster based on engagement and experience scores")
st.write(cluster_segmented_2)

st.subheader("The average satisfaction and experience scores for each of the two clusters")
cluster_scores = aggregate_cluster_scores(segmented_data)
st.write(cluster_scores)
