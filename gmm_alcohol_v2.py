from pyspark.ml.clustering import GaussianMixtureModel, GaussianMixtureSummary, GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import VectorAssembler,StringIndexer
from pyspark.ml import Pipeline


conf = SparkConf().setAppName("GMM").set("spark.hadoop.yarn.resourcemanager.address", "spark01:8032")
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

gmm = GaussianMixture().setK(2).setSeed(538009335)
model = gmm.fit(dataset)

print("Gaussians shown as a DataFrame: ")
model.gaussiansDF.show(truncate=False)

summary = model.summary
print("k = ", summary.k)

print("cluster sizes", summary.clusterSizes)
print("log likelihood", summary.logLikelihood)
# Make predictions