# autodatapre

#### Project description
Automated System for Efficient Generation of Data Preparation Pipeline


#### Quick Start

1.  Before running the code, please make sure your Python version is 3.10. 
2.  pip install autodatapre

#### Run Example

1.  AutoDP.testFunction() provide two examples
2.  datasetName=csv_path
    datasetTarget = ''
    runTime = 10
    df = pd.read_csv(datasetName, sep=',', encoding='ISO-8859-1')
    detailResult, preparedDataset = Classifier(df, datasetName, datasetTarget, runTime)
    EnhancedFunction(df, preparedDataset, detailResult, taskType="CLA")
3.  datasetName=csv_path
    datasetTarget = ''
    df = pd.read_csv(datasetName, sep=',', encoding='ISO-8859-1')
    detailResult, preparedDataset = Regressor(df, datasetName, datasetTarget, runTime)
    EnhancedFunction(df, preparedDataset, detailResult, taskType="CLA")
