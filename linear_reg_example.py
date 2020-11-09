from pyspark.sql import SparkSession, SQLContext
from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext, SparkConf
from pyspark.ml import Pipeline
from pyspark.ml.linalg import DenseVector
from pyspark.ml.feature import VectorAssembler, OneHotEncoderEstimator, StringIndexer
from pyspark.sql.types import *
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator
import sys

def convertColumns(df, names, newType):
	for name in names:
		df = df.withColumn(name, df[name].cast(newType))
	return df

if __name__ == "__main__":
	# create Spark context with Spark configuration
	conf = SparkConf().setAppName("Airplane Delays").set("spark.hadoop.yarn.resourcemanager.address", "spark01:8032")
	sc = SparkContext(conf=conf)
	spark = SparkSession(sc)
	sqlContext = SQLContext(sc)
	# Load training data
	data_raw = spark.read.csv("hdfs://spark01:9000/user/mstrasse/assig_2_data/IDUGAirlineSatisfactionSurvey.csv", header=True,inferSchema=True)
	CONTIN_FEAT = ['Satisfaction']
	data_df = convertColumns(data_raw, CONTIN_FEAT, FloatType())

	# get rid of special characters 
	data = data_df.withColumnRenamed('No of Flights p.a.','No of Flights pa')
	data = data.withColumnRenamed('No of Flights p.a. grouped', 'No of Flights pa grouped')
	data = data.withColumnRenamed('% of Flight with other Airlines','Percent of Flight with other Airlines')
	data = data.withColumnRenamed('No. of other Loyalty Cards', 'No of other Loyalty Cards')
	data = data.withColumnRenamed('Arrival Delay in Minutes', 'label')

	continuous_cols = ['Satisfaction','Age','Price Sensitivity',\
	'Year of First Flight','No of Flights pa','Percent of Flight with other Airlines','No of other Loyalty Cards',\
	'Shopping Amount at Airport', 'Eating and Drinking at Airport',\
	'Day of Month','Scheduled Departure Hour','Departure Delay in Minutes',	'Flight time in minutes','Flight Distance']

	# debugging
	# data.printSchema()
	categ_cols = [ 'Class', 'Age Range','Gender', 'No of Flights pa grouped', 'Type of Travel','Airline Status',\
			'Flight date', 'Airline Code','Airline Name', 'Orgin City', 'Origin State', 'Destination City', 'Destination State',\
			'Flight cancelled', 'Arrival Delay greater 5 Mins']

	train, test = data.randomSplit([0.7, 0.3], seed=100)

	stages = [] 
	for col in categ_cols:
		stringIndexer = StringIndexer(inputCol = col, outputCol = "idx_{0}".format(col), handleInvalid='skip')
		encoder = OneHotEncoderEstimator(inputCols= ["idx_{0}".format(col)], outputCols = ["cvector_{0}".format(col)])
		stages += [stringIndexer, encoder]

	# Convert label into label indices using the StringIndexer
	#label_stringIdx =  StringIndexer(inputCol= 'label', outputCol="indexedLabel")
	#stages += [label_stringIdx]

	assemblerInputs = ["cvector_{0}".format(col) for col in categ_cols] + continuous_cols
	assembler = VectorAssembler(inputCols = assemblerInputs, outputCol="features", handleInvalid='skip')
	stages+=[assembler]

	lr = LinearRegression(featuresCol="features", labelCol = "label")
	stages.append(lr)

	# create pipeline
	pipeline = Pipeline(stages = stages)
	pipelineModel = pipeline.fit(train)
	predictions = pipelineModel.transform(test)

	predictions.select("prediction", "label", "features").show(5)


	evaluator = MulticlassClassificationEvaluator(
	    labelCol="label", predictionCol="prediction", metricName="accuracy")

	accuracy = evaluator.evaluate(predictions)

	print("Test Error = %g " % (1.0 - accuracy))

	# Select (prediction, true label) and compute test error
	evaluator = RegressionEvaluator(
	    labelCol="label", predictionCol="prediction", metricName="rmse")
	rmse = evaluator.evaluate(predictions)

	print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)

	# Print the coefficients and intercept for linear regression
	#print("Coefficients: %s" % str(lrModel.coefficients))
	#print("Intercept: %s" % str(lrModel.intercept))

	# Summarize the model over the training set and print out some metrics
"""
	eval_sum = lrmodel.evaluate(test)
	print("Mean Absolute Error: %d" % eval_sum .meanAbsoluteError)
	print("objectiveHistory: %s" % str(eval_sum.rootMeanSquaredError))
	eval_sum.residuals.show()
	print("RMSE: %f" % eval_sum.rootMeanSquaredError)
	print("r2: %f" % eval_sum.r2)
"""
