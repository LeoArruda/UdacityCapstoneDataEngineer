from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers


# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_capstone_plugin"
    operators = [
        operators.S3ToRedshiftOperator,
        operators.DataQualityOperator,
        operators.DataAnalysisOperator,
        operators.RenderToS3Operator,
        operators.LoadFactDimOperator,
    ]
    helpers = [
        helpers.SqlQueries,
        helpers.DataValidationQueries,
    ]