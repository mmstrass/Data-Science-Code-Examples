from pyspark.ml.clustering import GaussianMixtureModel, GaussianMixtureSummary, GaussianMixture
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext, SparkConf
from pyspark.ml.feature import VectorAssembler

conf = SparkConf().setAppName("Kmeans").set("spark.hadoop.yarn.resourcemanager.address", "spark01:8032")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
# Loads data.
df = spark.read.csv("hdfs://spark01:9000/user/mstrasse/assig_2_data/IDUGAirlineSatisfactionSurvey.csv", header=True,inferSchema=True)
df = df.withColumnRenamed('No of Flights p.a.','No of Flights pa')
df = df.withColumnRenamed('No of Flights p.a. grouped', 'No of Flights pa grouped')
df = df.withColumnRenamed('% of Flight with other Airlines','Percent of Flight with other Airlines')
df = df.withColumnRenamed('No. of other Loyalty Cards', 'No of other Loyalty Cards')

features = ['Satisfaction','Age','Price Sensitivity',\
'Year of First Flight','No of Flights pa','Percent of Flight with other Airlines','No of other Loyalty Cards',\
'Shopping Amount at Airport', 'Eating and Drinking at Airport',\
'Day of Month','Scheduled Departure Hour','Departure Delay in Minutes',	'Flight time in minutes','Flight Distance']

assembler = VectorAssembler(inputCols=features,outputCol="features", handleInvalid="skip")

dataset=assembler.transform(df)

dataset.select("features").show(truncate=False)
# Trains a k-means model.

gmm = GaussianMixture().setK(2).setSeed(538009335)
model = gmm.fit(dataset)

print("Gaussians shown as a DataFrame: ")
model.gaussiansDF.show(truncate=False)

summary = model.summary
print("k = ", summary.k)

print("cluster sizes", summary.clusterSizes)
print("log likelihood", summary.logLikelihood)
# Make predictions