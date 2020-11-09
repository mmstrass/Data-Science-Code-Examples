from pyspark.sql import SparkSession, SQLContext
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark import SparkContext, SparkConf
from pyspark.mllib.util import MLUtils
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator

import sys


if __name__ == "__main__":
	# create Spark context with Spark configuration
	conf = SparkConf().setAppName("Airplane Delays").set("spark.hadoop.yarn.resourcemanager.address", "spark01:8032")
	sc = SparkContext(conf=conf)
	spark = SparkSession(sc)
	sqlContext = SQLContext(sc)
	df = spark.read.csv("hdfs://spark01:9000/user/mstrasse/assig_2_data/DigitalBreathTestData2014.txt", header=True,inferSchema=True)

	df = df.withColumnRenamed('BreathAlcoholLevel(microg 100ml)','label')
	stages = []
	input_columns = ['Reason', 'Month', 'Year', 'WeekType', 'TimeBand', 'AgeBand', 'Gender']
	#labelIndexer = [StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)]

	#stages += labelIndexer
	si = [StringIndexer(inputCol = col, outputCol = "idx_{0}".format(col)).fit(df) for col in input_columns]
	stages+=si
	stages.append(VectorAssembler(inputCols = ["idx_{0}".format(col) for col in input_columns], outputCol = 'features'))
	dec_tree = DecisionTreeRegressor(labelCol='label', featuresCol='features', maxDepth=5)

	stages.append(dec_tree)

	# Split the data into training and test sets (30% held out for testing)
	trainingData, testData = df.randomSplit([0.7, 0.3], seed = 123)
	evaluator = RegressionEvaluator(metricName='rmse', labelCol='label')
	grid = ParamGridBuilder().addGrid(dec_tree.maxDepth, [3,5,7,10]).build()
	cv = CrossValidator(estimator = dec_tree, estimatorParamMaps=grid, evaluator=evaluator, numFolds=10)
	stages
	pipeline = Pipeline(stages = stages)

	model = pipeline.fit(trainingData)

	predictions = model.transform(testData)

	output = []

	output.append(predictions.select("prediction", "label", "features").show(5))

	output.append((model.stages[-1]))


	# Select (prediction, true label) and compute test error
	evaluator = MulticlassClassificationEvaluator(
	    labelCol="label", predictionCol="prediction", metricName="accuracy")

	accuracy = evaluator.evaluate(predictions)

	output.append("Test Error = %g " % (1.0 - accuracy))

	# Select (prediction, true label) and compute test error
	evaluator = RegressionEvaluator(
	    labelCol="label", predictionCol="prediction", metricName="rmse")
	rmse = evaluator.evaluate(predictions)

	output.append("Root Mean Squared Error (RMSE) on test data = %g" % rmse)

	treeModel = model.stages[1]
	# summary only
	output.append(treeModel)

	dtm = model.stages[-1] # you estimator is the last stage in the pipeline
	# hence the DecisionTreeClassifierModel will be the last transformer in the PipelineModel object 
	output.append(dtm.explainParams())
	rdd = sc.parallelize(output)
	rdd.saveAsTextFile("hdfs://spark01:9000/user/mstrasse/outputoutputDT.txt")
	#output.saveAsTextFile("hdfs://spark01:9000/user/mstrasse/outputDT")

