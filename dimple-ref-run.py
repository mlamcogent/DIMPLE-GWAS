### Dimple reference run 
### Python notebook script conversion 

## Load notebook dependencies 
## Dependecies will generally support this notebook however 
## Some of the code blocks are going to be exported as standalone scripts 
## in those code blocks the depedencies are imported accordingly

from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

import os

OUTDIR = os.environ.get("DIMPLE_REF_OUTDIR", "ref_outputs")
os.makedirs(OUTDIR, exist_ok=True)

def outpath(name: str) -> str:
    return os.path.join(OUTDIR, name)

# Dimension reduction and clustering libraries
import umap
import hdbscan
import sklearn.cluster as cluster
#from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score

# Jibin's scripts 
#import numpy as np
import pandas as pd
#import umap
#from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
#import matplotlib.pyplot as plt

# to compute Trustworthiness and Continuity

from sklearn.neighbors import NearestNeighbors

# GRID search
import numpy as np
import hdbscan
from sklearn.metrics import silhouette_samples
from sklearn.datasets import make_blobs
import pandas as pd  # Import pandas for easy CSV writing

# for 3d plotting
from mpl_toolkits.mplot3d import Axes3D

## Dependencies for interactive plots
import plotly.graph_objects as go

print("General Dependencies for IDP Neuroimaging Clustering Pipeline Loaded")

### Define objects for pipeline 
print("Defining input and output objectives for pipeline")

## read in data
datainput = "test_dat.csv"
## Initial umap plot
prelim_umap = outpath("Stage_00_preliminary_umap_scatterplot.html")
## hdbscan input
hdbscan_input = outpath("Stage_01_hdbscan_input.csv")
## input file for scree plot
screeinput = outpath("Stage_02_scree_plot_input.csv")
# optimized cluster solutations 
optimized_out = outpath("Stage_03_optimized_cluster_solutions.csv")
## scree plot
screeplot1 = outpath("Stage_04_plotly_2d_silhouette_vs_clusters.html")
screeplot2 = outpath("Stage_05_plotly_2d_noise_vs_clusters.html")
screeplot3 = outpath("Stage_06_plotly_2d_silhouette_vs_noise.html")
## sil plot 
silplot = outpath("Stage_07_silhouette_analysis.png")
##log file 
logfile = outpath("Stage_08_cluster_metrics.txt")
## umapdataframe
umapdataframe = outpath("Stage_09_UMAP_vizdata_cluster_solutions.csv")
## clusterplot1
clusterplot1 = outpath("Stage_10_plotly_3d_cluster_solutions.html")
## clusterplot2
clusterplot2 = outpath("Stage_11_plotly_3d_modalities.html")

## read in data 
## note that 'datainput' is defined in the earlier step 
## please check if this code block is not running correctly
print("reading in input data")

try:
    df = pd.read_csv(datainput, engine="pyarrow", sep=",")
except Exception as e:
    print(f"pyarrow CSV read failed ({e}); falling back to default pandas CSV reader")
    df = pd.read_csv(datainput, sep=",")

df2=df.iloc[:,4:]
X=df2.T

### check matrix 
print("checking data matrix...")
X

## Generate UMAP for visualization purposes
# Note matrix for umap reducer is X from above
print("generating umap dimensions for visualization...")
n_components = 3

clusterable_embedding_viz = umap.UMAP(
    densmap=True, 
    n_neighbors=30,
    min_dist=0.0,
    n_components=n_components,
    random_state=42,
).fit_transform(X)

# check UMAP data set
# This dataset is for plottin and visualization thereafter 
# this is the standard random state = 42 
print("umap dimensions:")
clusterable_embedding_viz

### Generate preliminary UMAP plot

import plotly.graph_objects as go
import pandas as pd

# Assuming clusterable_embedding is the 3D UMAP embedding from your UMAP transformation
# clusterable_embedding is an (n_samples, 3) array where each row is a 3D UMAP coordinate.

# Create a DataFrame for easy manipulation
df_umap = pd.DataFrame(clusterable_embedding_viz, columns=['UMAP1', 'UMAP2', 'UMAP3'])

# Create a 3D scatter plot
fig = go.Figure()

# Add all points in the UMAP embedding as a single trace (no labels or clusters)
fig.add_trace(go.Scatter3d(
    x=df_umap['UMAP1'],
    y=df_umap['UMAP2'],
    z=df_umap['UMAP3'],
    mode='markers',
    marker=dict(
        size=5,
        color='blue',  # Choose a uniform color for all points
        opacity=0.8,
    ),
    name='UMAP Points'
))

# Update layout
fig.update_layout(
    title='3D UMAP Embedding',
    scene=dict(
        xaxis_title='UMAP1',
        yaxis_title='UMAP2',
        zaxis_title='UMAP3'
    ),
    legend_title='UMAP'
)

# Show the plot
# fig.show()  # disabled for non-notebook execution

import plotly.express as px
import plotly.io as pio


# Save the plot as an HTML file
pio.write_html(fig, file=prelim_umap, auto_open=False)
print("write preliminary umap plot...")

#### Parallelized UMAP implementation 
#### Note that this code block is going to run UMAP for 1000 random states 
#### starting with random state = 1 through to random state 1000
#### Note random state 42 is usually used as the default for any stochastic algorithms
#### The rationale of carrying out umap in this manner to capture the nuanced pleiotropic architecture 
#### that might be embedding in the neuroimaging IDP features 
#### The code here is going to parallelize umap over all available CPU cores
#### ending up with 3000 umap dimensions for cluster analysis 

print("initiating parallelized umap with 1000 random states....")

import umap
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

# Assuming X is your input data matrix (n_samples, n_features)
n_components = 3  # 3 UMAP dimensions per run
n_random_states = 1000  # Number of UMAP runs

# Define a function to run UMAP with a specific random state
def run_umap(random_state):
    print(f"Running UMAP with random_state={random_state}")
    reducer = umap.UMAP(
        densmap=True, 
        n_neighbors=30,
        min_dist=0.0,
        n_components=n_components,
        random_state=random_state
    )
    return reducer.fit_transform(X)

# Use joblib's Parallel to run UMAP in parallel (adjust n_jobs based on your CPU)
results = Parallel(n_jobs=-1)(delayed(run_umap)(rs) for rs in range(1, n_random_states + 1))

# Concatenate the results into a single array
consolidated_umap_array = np.hstack(results)

# Create a DataFrame for easier manipulation and save it to a CSV
umap_df = pd.DataFrame(consolidated_umap_array, columns=[f'UMAP_{i+1}' for i in range(consolidated_umap_array.shape[1])])

# Save the DataFrame to a CSV file
umap_df.to_csv(hdbscan_input, index=False)

print("UMAP embeddings saved to hdbscan input file....")

### Parallelized grid search 

print("parallelized grid search for best fitting cluster....")

import hdbscan
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_samples
from joblib import Parallel, delayed

try:
    clusterable_embedding = pd.read_csv(hdbscan_input, engine="pyarrow")
except Exception as e:
    print(f"pyarrow CSV read failed ({e}); falling back to default pandas CSV reader")
    clusterable_embedding = pd.read_csv(hdbscan_input)

# Grid search ranges
min_samples_range = range(2, 20)
min_cluster_size_range = range(5, 50)
epsilon_range = np.arange(0, 3)  # Epsilon from 0 to 3


# Define a function to perform clustering and calculate silhouette scores
def evaluate_config(epsilon, min_samples, min_cluster_size, clusterable_embedding):
    clusterer = hdbscan.HDBSCAN(
        min_samples=min_samples,
        min_cluster_size=min_cluster_size,
        cluster_selection_epsilon=epsilon,
        cluster_selection_method='eom'
    ).fit(clusterable_embedding)

    labels = clusterer.labels_
    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    
    # Count the number of noise points
    noise_count = (labels == -1).sum()  # Count how many points are labeled as -1 (noise)
    
    if num_clusters > 1:
        # Calculate silhouette scores only for non-noise samples
        non_noise_indices = labels != -1
        filtered_labels = labels[non_noise_indices]
        filtered_embedding = clusterable_embedding[non_noise_indices]

        silhouette_values = silhouette_samples(filtered_embedding, filtered_labels)
        silhouette_avg = np.mean(silhouette_values)

        # Return configuration, silhouette score, and noise point count
        return {
            'Silhouette_avg': silhouette_avg,
            'Epsilon': epsilon,
            'Min_samples': min_samples,
            'Min_cluster_size': min_cluster_size,
            'Clusters': num_clusters,
            'Noise_points': noise_count  # Add noise point count to the output
        }
    return None  # Return None if no valid clusters

# Parallelize the grid search across all configurations
suitable_configurations = Parallel(n_jobs=-1)(
    delayed(evaluate_config)(epsilon, min_samples, min_cluster_size, clusterable_embedding)
    for epsilon in epsilon_range
    for min_samples in min_samples_range
    for min_cluster_size in min_cluster_size_range
)

# Filter out None values (if any)
suitable_configurations = [config for config in suitable_configurations if config is not None]

# Create a DataFrame from the list of configurations
df = pd.DataFrame(suitable_configurations)

# Output the suitable configurations
print("All configurations regardless of silhouette criteria:")
print(df)

# Save to CSV file
print("saving cluster properties to file....")
df.to_csv(screeinput, index=False)

### Generate the three scree plots
print("generating screeplots....")

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load the CSV into a DataFrame ** UPDATE FILE NAME **
dfsc = pd.read_csv(screeinput)

# Sort the DataFrame by 'Clusters' and 'Silhouette_avg' (adjust the column names if needed)
sorted_dfsc = dfsc.sort_values(by=['Clusters', 'Silhouette_avg'], ascending=[False, False])

# Display the sorted DataFrame (for checking)
print(sorted_dfsc.head())

### 1. Silhouette Average vs Clusters
# Create an interactive scatter plot for Silhouette Average vs Clusters
fig1 = px.scatter(sorted_dfsc, x='Silhouette_avg', y='Clusters',
                  title='Silhouette Average vs. Clusters',
                  labels={'Silhouette_avg': 'Silhouette Average', 'Clusters': 'Number of Clusters'}, 
                  hover_data=sorted_dfsc.columns)  # Display all columns as hover data
# Show the plot
# fig1.show()  # disabled for non-notebook execution

# Save the plot as an HTML file
pio.write_html(fig1, file=screeplot1, auto_open=False)


### 2. Noise Points vs Clusters
# Create an interactive scatter plot for Noise Points vs Clusters
fig2 = px.scatter(sorted_dfsc, x='Noise_points', y='Clusters',
                  title='Noise Points vs. Clusters',
                  labels={'Noise_points': 'Number of Noise Points', 'Clusters': 'Number of Clusters'}, 
                  hover_data=sorted_dfsc.columns)  # Display all columns as hover data
# Show the plot
# fig2.show()  # disabled for non-notebook execution

# Save the plot as an HTML file (name it appropriately)
pio.write_html(fig2, file=screeplot2, auto_open=False)


### 3. Silhouette Averages vs Noise Points
# Create an interactive scatter plot for Silhouette Averages vs Noise Points
fig3 = px.scatter(sorted_dfsc, x='Silhouette_avg', y='Noise_points',
                  title='Silhouette Averages vs. Noise Points',
                  labels={'Silhouette_avg': 'Silhouette Average', 'Noise_points': 'Number of Noise Points'}, 
                  hover_data=sorted_dfsc.columns)  # Display all columns as hover data
# Show the plot
# fig3.show()  # disabled for non-notebook execution

# Save the plot as an HTML file (name it appropriately)
pio.write_html(fig3, file=screeplot3, auto_open=False)

### Optimization code to select best solution 
print("carrying out optimization for cluster selection....")

import pandas as pd

# Load the CSV file containing the grid search results
df = pd.read_csv(screeinput)

# Normalize the metrics to a 0-1 scale
df['Silhouette_avg_normalized'] = df['Silhouette_avg'] / df['Silhouette_avg'].max()
df['Clusters_normalized'] = df['Clusters'] / df['Clusters'].max()
df['Noise_points_normalized'] = df['Noise_points'] / df['Noise_points'].max()

# Calculate the range of each metric
range_silhouette = df['Silhouette_avg'].max() - df['Silhouette_avg'].min()
range_clusters = df['Clusters'].max() - df['Clusters'].min()
range_noise = df['Noise_points'].max() - df['Noise_points'].min()

# Assign weights based on the range of each metric
total_range = range_silhouette + range_clusters + range_noise
weight_silhouette = range_silhouette / total_range
weight_clusters = range_clusters / total_range
weight_noise = range_noise / total_range

print(f"Assigned Weights: Silhouette = {weight_silhouette}, Clusters = {weight_clusters}, Noise = {weight_noise}")

# Calculate the weighted score
df['Score'] = (
    weight_silhouette * df['Silhouette_avg_normalized'] +
    weight_clusters * df['Clusters_normalized'] -
    weight_noise * df['Noise_points_normalized']
)

# Sort the DataFrame by the score in descending order
df_sorted = df.sort_values(by='Score', ascending=False)

# Display the top configuration
top_config = df_sorted.iloc[0]
print("Top configuration based on weighted score:")
print(top_config)

# Calculate the median index
median_index = len(df_sorted) // 2  # Use integer division to get the middle index

# Display the median configuration
median_config = df_sorted.iloc[median_index]
print("Median configuration based on weighted score:")
print(median_config)

## SUBSTITUTE TOP CONFIG with CUSTOM CONFIG 
## Use only after top config has been generated 
#top_config = df_sorted.iloc[15]
#print("Customized configuration based on weighted score:")
#print(top_config)

# Extract the top configuration parameters into variables for downstream clustering
best_epsilon = top_config['Epsilon']
best_min_samples = top_config['Min_samples']
best_min_cluster_size = top_config['Min_cluster_size']
best_avg_silhouette = top_config['Silhouette_avg']

# Print the extracted values for downstream use
print(f"Best Epsilon: {best_epsilon}")
print(f"Best Min Samples: {best_min_samples}")
print(f"Best Min Cluster Size: {best_min_cluster_size}")
print(f"Best Average Silhouette: {best_avg_silhouette}")

# Save the sorted results for further analysis if needed
print("saving optimized cluster outputs....")
df_sorted.to_csv(optimized_out, index=False)

### Plot score by cluster 
# Create an interactive scatter plot for Silhouette Averages vs Noise Points
fig4 = px.scatter(df_sorted, x='Score', y='Clusters',
                  title='Score vs. Clusters',
                  labels={'Silhouette_avg': 'Silhouette Average', 'Noise_points': 'Number of Noise Points'}, 
                  hover_data=df_sorted.columns)  # Display all columns as hover data
# Show the plot
# fig4.show()  # disabled for non-notebook execution

## HDBscan + DBscan 
## To be informed by optimal cluster solutioning 
## See plot above Number of clusters - Silhouette Average
print("conducting DBscan procedures based on optimized cluster solution...")

epsilon = int(best_epsilon)
min_samples = int(best_min_samples)
min_cluster_size= int(best_min_cluster_size)
avgsil = best_avg_silhouette

labels = hdbscan.HDBSCAN(
    min_samples=min_samples,
    min_cluster_size=min_cluster_size,
    cluster_selection_epsilon=epsilon,
    cluster_selection_method='eom'
).fit_predict(clusterable_embedding)

## count clusters 
from collections import Counter
hdb_counter = Counter(labels)
hdb_n_clusters = len([label for label in hdb_counter.keys() if label != -1])

    # Calculate silhouette score, handling case where all points are considered noise
if len(set(labels)) > 1:  # Ensure there's more than one cluster
    silhouette_avg = silhouette_score(clusterable_embedding, labels)
else:
    silhouette_avg = -1  # Assign a low score if HDBSCAN found 0 or 1 clusters
print(f"n_components: {n_components}")
print(f"silhouette_avg: {silhouette_avg}")
print(f"Clusters: {hdb_n_clusters}")

## Silhouette analysis 
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt
import numpy as np

silhouette_vals = silhouette_samples(clusterable_embedding, labels)
cluster_labels = np.unique(labels)
y_lower, y_upper = 0, 0
yticks = []

for i, c in enumerate(cluster_labels):
    c_silhouette_vals = silhouette_vals[labels == c]
    c_silhouette_vals.sort()
    y_upper += len(c_silhouette_vals)
    plt.barh(range(y_lower, y_upper), c_silhouette_vals, edgecolor='none', height=1)
    yticks.append((y_lower + y_upper) / 2)
    y_lower += len(c_silhouette_vals)

plt.axvline(np.mean(silhouette_vals), color="red", linestyle="--")
plt.axvline(avgsil, color="blue", linestyle="--")
plt.yticks(yticks, cluster_labels + 1)
plt.ylabel('Cluster')
plt.xlabel('Silhouette coefficient')
plt.title('Silhouette Analysis')  # Optional: Adds a title to the plot

# Saving the figure to a file
plt.savefig(silplot)  # Saves the plot as a PNG file. You can also save as .pdf, .svg, etc.
# plt.show()  # disabled for non-notebook execution

# Function to compute trustworthiness
def trustworthiness(X, X_embedded, n_neighbors):
    n_samples = X.shape[0]
    
    # Find nearest neighbors in original space
    nn_orig = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X)
    dist_orig, ind_orig = nn_orig.kneighbors(X)
    
    # Find nearest neighbors in embedded space
    nn_embedded = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X_embedded)
    dist_embedded, ind_embedded = nn_embedded.kneighbors(X_embedded)
    
    # Remove the first column (self-neighbors)
    ind_orig = ind_orig[:, 1:]
    ind_embedded = ind_embedded[:, 1:]
    
    # Create rank matrices
    rank_orig = np.zeros((n_samples, n_samples))
    rank_embedded = np.zeros((n_samples, n_samples))
    
    for i in range(n_samples):
        rank_orig[i, ind_orig[i]] = np.arange(1, n_neighbors + 1)
        rank_embedded[i, ind_embedded[i]] = np.arange(1, n_neighbors + 1)
    
    # Calculate trustworthiness
    U = np.zeros(n_samples)
    for i in range(n_samples):
        U[i] = np.sum((rank_orig[i, ind_embedded[i]] > n_neighbors) * (rank_orig[i, ind_embedded[i]] - n_neighbors))
    
    trust = 1 - 2 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1)) * np.sum(U)
    return trust

# Function to compute continuity
def continuity(X, X_embedded, n_neighbors):
    n_samples = X.shape[0]
    
    # Find nearest neighbors in original space
    nn_orig = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X)
    dist_orig, ind_orig = nn_orig.kneighbors(X)
    
    # Find nearest neighbors in embedded space
    nn_embedded = NearestNeighbors(n_neighbors=n_neighbors + 1).fit(X_embedded)
    dist_embedded, ind_embedded = nn_embedded.kneighbors(X_embedded)
    
    # Remove the first column (self-neighbors)
    ind_orig = ind_orig[:, 1:]
    ind_embedded = ind_embedded[:, 1:]
    
    # Create rank matrices
    rank_orig = np.zeros((n_samples, n_samples))
    rank_embedded = np.zeros((n_samples, n_samples))
    
    for i in range(n_samples):
        rank_orig[i, ind_orig[i]] = np.arange(1, n_neighbors + 1)
        rank_embedded[i, ind_embedded[i]] = np.arange(1, n_neighbors + 1)
    
    # Calculate continuity
    V = np.zeros(n_samples)
    for i in range(n_samples):
        V[i] = np.sum((rank_embedded[i, ind_orig[i]] > n_neighbors) * (rank_embedded[i, ind_orig[i]] - n_neighbors))
    
    cont = 1 - 2 / (n_samples * n_neighbors * (2 * n_samples - 3 * n_neighbors - 1)) * np.sum(V)
    return cont

### Additional cluster indices 
#Calinski-Harabasz Index (Variance Ratio Criterion):
#Measures the ratio of the sum of between-cluster dispersion and within-cluster dispersion.
#Higher values indicate better-defined clusters.

# Compute trustworthiness and continuity
trust = trustworthiness(X, clusterable_embedding, n_neighbors=30)
cont = continuity(X, clusterable_embedding, n_neighbors=30)

from sklearn.metrics import calinski_harabasz_score

ch_score = calinski_harabasz_score(clusterable_embedding, labels)

#Davies-Bouldin Index:

#Measures the average similarity ratio of each cluster with its most similar cluster.
#Lower values indicate better clustering.

from sklearn.metrics import davies_bouldin_score

db_score = davies_bouldin_score(clusterable_embedding, labels)

#Dunn Index:

#Ratio of the smallest distance between clusters to the largest within-cluster distance.
#Higher values indicate well-separated clusters.

from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

def dunn_index(X, labels):
    distances = euclidean_distances(clusterable_embedding)
    unique_labels = np.unique(labels)
    inter_cluster_distances = [distances[np.ix_(labels == i, labels == j)].min()
                               for i in unique_labels for j in unique_labels if i != j]
    intra_cluster_distances = [distances[labels == i, :][:, labels == i].max() for i in unique_labels]
    return min(inter_cluster_distances) / max(intra_cluster_distances)

dunn = dunn_index(clusterable_embedding, labels)

print(f"Trustworthiness: {trust:.4f}")
print(f"Continuity: {cont:.4f}")
print(f"DBSCAN eps: {epsilon}")
print(f"HDBSCAN minsamples: {min_samples}")
print(f"HDBSCAN min cluster size: {min_cluster_size}")
print(f"Clusters: {hdb_n_clusters}")
print(f"Silhouette_avg: {silhouette_avg}")
print(f"Calinski-Harabasz Index: {ch_score:.4f}")
print(f"Davies-Bouldin Index: {db_score:.4f}")
print(f"Dunn Index: {dunn:.4f}")


import logging

#### LOGGING INFORMATION *SPECIFIC LOG NAME ACCORDINGLY* #### 
filename = logfile

# Clear previous logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging again
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(filename),
                        logging.StreamHandler()
                    ])

# Log the output
print("generating fit statistics....")
logging.info("Trustworthiness: {0:.4f}".format(trust))
logging.info("Continuity: {0:.4f}".format(cont))
logging.info("DBSCAN eps: {0}".format(epsilon))
logging.info("HDBSCAN minsamples: {0}".format(min_samples))
logging.info("HDBSCAN min cluster size: {0}".format(min_cluster_size))
logging.info("Clusters: {0}".format(hdb_n_clusters))
logging.info("Silhouette_avg: {0}".format(silhouette_avg))
logging.info("Calinski-Harabasz Index: {0:.4f}".format(ch_score))
logging.info("Davies-Bouldin Index: {0:.4f}".format(db_score))
logging.info("Dunn Index: {0:.4f}".format(dunn))

# Create a DataFrame for easy visualization

print("creating data frame for easy visualization....")
n_components = 3
df_umap = pd.DataFrame(clusterable_embedding_viz, columns=[f'UMAP_{i+1}' for i in range(n_components)])
df_umap['label'] = labels

# Print out the samples in each cluster
for cluster_label in sorted(df_umap['label'].unique()):
    cluster_samples = df_umap[df_umap['label'] == cluster_label]
    print(f"Cluster {cluster_label}: {len(cluster_samples)} samples")
    print(cluster_samples.index.to_list())


idp_label=X.iloc[:,0:1].reset_index().drop(0,axis=1)
df_umap_with_label=pd.concat([idp_label,df_umap],axis=1)

df_umap_with_label.to_csv(umapdataframe)

## check umap results 

print("checking umap viz with cluster solutions.....")
df_umap_with_label

### 3D plotly solution

print("generating 3D plotly solutions....")

import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Assuming clusterable_embedding and labels are defined

# Determine which points are clustered
clustered = (labels >= 0)

# Get unique labels and assign colors using a qualitative color palette
unique_labels = np.unique(labels[clustered])
#colors = px.colors.qualitative.Set1  # A qualitative color palette from Plotly Express
all_palettes = px.colors.qualitative.Plotly + px.colors.qualitative.Dark24  # Combining two palettes
colors = all_palettes[:len(unique_labels)]  # Adjust length to match number of unique labels


# Create the 3D scatter plot
fig = go.Figure()

# Add a trace for each unique label in clustered data
for i, label in enumerate(unique_labels):
    mask = (labels == label)
    fig.add_trace(go.Scatter3d(
        x=clusterable_embedding_viz[mask, 0],
        y=clusterable_embedding_viz[mask, 1],
        z=clusterable_embedding_viz[mask, 2],
        mode='markers',
        marker=dict(
            size=5,
            color=colors[i % len(colors)],  # Cycle through colors if there are more labels than colors
        ),
        name=f'hdbs k {label}'  # Each trace gets a unique name corresponding to its label
    ))

# Handle non-clustered points (label == -1) separately if needed
if any(labels == -1):
    mask = (labels == -1)
    fig.add_trace(go.Scatter3d(
        x=clusterable_embedding_viz[mask, 0],
        y=clusterable_embedding_viz[mask, 1],
        z=clusterable_embedding_viz[mask, 2],
        mode='markers',
        marker=dict(
            size=5,
            color='grey',
        ),
        name='Noise'
    ))

# Update plot layout
fig.update_layout(
    title='Neuroimaging IDP Cluster Solution',
    scene=dict(
        xaxis_title='UMAP1',
        yaxis_title='UMAP2',
        zaxis_title='UMAP3'
    ),
    legend_title='IDP Clusters',
    legend=dict(
        x=0.8, 
        y=0.5,
        bgcolor='rgba(255,255,255,0.5)', 
        bordercolor='Black'
    )
)

# Show the plot
# fig.show()  # disabled for non-notebook execution

import plotly.express as px
import plotly.io as pio

print("saving 3D plotly diagram...")

pio.write_html(fig, file=clusterplot1, auto_open=False)

## merge in KEY IDP labels

print("merging IDP key with UMAP data....")

import pandas as pd

# Load the IDP-KEY.csv file
idp_key = pd.read_csv('IDP_KEY.csv')

# Ensure that the 'index' in idp_key is of string type
idp_key['index'] = idp_key['index'].astype(str)

# Assuming df_umap_with_label uses 'index' as a column of string IDs
# If it's not already set as the index, you might want to set it
if 'index' in df_umap_with_label.columns:
    df_umap_with_label['index'] = df_umap_with_label['index'].astype(str)
else:
    # If the index of df_umap_with_label is these IDs and not set as a column
    df_umap_with_label.reset_index(inplace=True)
    df_umap_with_label['index'] = df_umap_with_label['index'].astype(str)
    df_umap_with_label.set_index('index', inplace=True)

# Merge the data on the 'index' column from both DataFrames
merged_df = pd.merge(idp_key, df_umap_with_label, on='index', how='left')

# Check the first few rows to ensure it merged correctly
print(merged_df.head())

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

# Assuming merged_df is your DataFrame containing the necessary data

print("generating 3D plotly with modalities....")

# List of available shapes in Plotly for 3D scatter plots
available_shapes = ['circle', 'circle-open', 'square', 'square-open', 'diamond', 'cross', 'x', 'diamond-open']

# Generate a dictionary that maps each unique category to a different shape
unique_categories = merged_df['original_Category name'].unique()
shape_map = {category: available_shapes[i % len(available_shapes)] for i, category in enumerate(unique_categories)}

# Prepare a distinct color palette for labels (assuming labels are categorical/discrete)
unique_labels = merged_df['label'].unique()
colors = px.colors.qualitative.Plotly  # Using Plotly's qualitative color palette
color_map = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels) if label != -1}

# Special color assignment for label -1
color_map[-1] = 'gray'  # Gray color for label -1

# Create the 3D scatter plot
fig = go.Figure()

# Iterate through categories to add clustered points
for category in unique_categories:
    category_data = merged_df[merged_df['original_Category name'] == category]
    fig.add_trace(go.Scatter3d(
        x=category_data['UMAP_1'],
        y=category_data['UMAP_2'],
        z=category_data['UMAP_3'],
        mode='markers',
        marker=dict(
            size=5,
            symbol=shape_map[category],  # Use auto-assigned shape
            color=[color_map[label] if label in color_map else 'gray' for label in category_data['label']],  # Assign colors based on label
            opacity=0.8
        ),
        name=f"{category}",
        text=category_data.apply(lambda row: f"IDP: {row['original_IDP']}<br>Category: {row['original_Category name']}", axis=1),
        hoverinfo='text+name'
    ))

# Update plot layout
fig.update_layout(
    title='3D Scatter Plot with Categorically Color-coded IDPs',
    scene=dict(
        xaxis_title='UMAP_1',
        yaxis_title='UMAP_2',
        zaxis_title='UMAP_3'
    ),
    legend_title='IDP Categories'
)

# Display the plot
# fig.show()  # disabled for non-notebook execution

import plotly.express as px
import plotly.io as pio

print("saving 3D plotly diagram with modalities...")
pio.write_html(fig, file=clusterplot2, auto_open=False)