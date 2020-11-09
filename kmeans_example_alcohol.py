from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import VectorAssembler,StringIndexer
from pyspark.ml import Pipeline



conf = SparkConf().setAppName("Kmeans").set("spark.hadoop.yarn.resourcemanager.address", "spark01:8032")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
# Loads data.
df = spark.read.csv("hdfs://spark01:9000/user/mstrasse/assig_2_data/DigitalBreathTestData2014.txt", header=True,inferSchema=True)
stages = []
input_columns = ['Reason', 'Month', 'Year', 'WeekType', 'TimeBand', 'AgeBand', 'Gender','BreathAlcoholLevel(microg 100ml)']

si = [StringIndexer(inputCol = col, outputCol = "idx_{0}".format(col)).fit(df) for col in input_columns]
stages+=si

stages.append(VectorAssembler(inputCols = ["idx_{0}".format(col) for col in input_columns], outputCol = 'features'))

pipeline = Pipeline(stages = stages)

model = pipeline.fit(df)

dataset = model.transform(df)

dataset.select("features").show(truncate=False)
# Trains a k-means model.
kmeans = KMeans().setK(2).setSeed(1)
model = kmeans.fit(dataset)

# Make predictions
predictions = model.transform(dataset)

# Evaluate clustering by computing Silhouette score
evaluator = ClusteringEvaluator()

silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

# Shows the result.
centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)

# Evaluate clustering by computing Within Set Sum of Squared Errors
wssse = model.computeCost(dataset)
print("Within Set Sum of Squared Errors = " + str(wssse))
