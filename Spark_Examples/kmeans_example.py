from pyspark.ml.clustering import KMeans
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
