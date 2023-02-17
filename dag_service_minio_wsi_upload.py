from kaapana.operators.LocalMinioOperator import LocalMinioOperator
from kaapana.operators.LocalUnzipFileOperator import LocalUnzipFileOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator

from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from wsi.LocalWSI2DCMOperator import LocalWSI2DCMOperator




log = LoggingMixin().log

args = {
    'ui_visible': False,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    dag_id='service-wsi-upload',
    default_args=args,
    schedule_interval=None,
    concurrency=10,
    max_active_runs=5
    )


get_object_from_minio = LocalMinioOperator(dag=dag, action_operator_dirs=['wsi'], operator_out_dir='wsi', bucket_name='uploads')
unzip_files = LocalUnzipFileOperator(dag=dag, input_operator=get_object_from_minio)
wsi2dcm = LocalWSI2DCMOperator(dag=dag, input_operator=unzip_files, blacklist_files="__MACOSX")
dicom_send = DcmSendOperator(dag=dag, input_operator=wsi2dcm, ae_title='uploaded', level='batch')
remove_object_from_minio = LocalMinioOperator(dag=dag, parallel_id='removing', action='remove', trigger_rule=TriggerRule.ALL_DONE)
clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=True)

get_object_from_minio >> unzip_files >> wsi2dcm >> dicom_send >> remove_object_from_minio >> clean
