from typing import List, Union, Optional
from pydantic import BaseModel


class Label(BaseModel):
    """
    Labeled Object
    """
    id: Optional[int] = None
    name: Optional[str] = None


class AccuracyResult(BaseModel):
    """
    mIOU Result
    """
    accuracy: Optional[float] = None


class Accuracy(BaseModel):
    """
    mIOU Metric
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[AccuracyResult] = None


class CategoryPrecisionResult(BaseModel):
    """
    Category IOU Result
    """
    categoryName: Optional[str] = None
    precision: Optional[float] = None
    recall: Optional[float] = None


class CategoryPrecision(BaseModel):
    """
    Category IOU Metric
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[List[CategoryPrecisionResult]]


class ConfusionMatrixAnnotationSpec(BaseModel):
    """
    Confusion Matrix Result
    """
    id: Optional[int] = None
    labelName: Optional[str] = None


class ConfusionMatrixRow(BaseModel):
    """
    Confusion Matrix Result
    """
    row: Optional[List[int]] = None


class ConfusionMatrixResult(BaseModel):
    """
    Confusion Matrix Result
    """
    annotationSpecs: Optional[List[ConfusionMatrixAnnotationSpec]] = None
    rows: Optional[List[ConfusionMatrixRow]] = None


class ConfusionMatrix(BaseModel):
    """
    Confusion Matrix
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[ConfusionMatrixResult] = None


class ClassificationMetric(BaseModel):
    """
    Object Detection Metric
    """
    modelName: Optional[str] = None
    datasetName: Optional[str] = None
    baselineJobName: Optional[str] = None
    timestamp: Optional[str] = None
    labels: Optional[List[Label]] = None
    metrics: Optional[List[Union[
        Accuracy,
        CategoryPrecision,
        ConfusionMatrix]]] = None

# --------------------------------------------------------
LOSS_METRIC = "Loss"
ACC_METRIC = "ACC"


class BaseTrainMetric(BaseModel):
    """
    Loss Metric
    """
    name: Optional[str] = None
    displayName: Optional[str] = None
    result: Optional[float] = None


class TrainMetric(BaseModel):
    """
    Object Detection Metric
    """
    epoch: Optional[str] = None
    step: Optional[str] = None
    metrics: Optional[List[BaseTrainMetric]] = None