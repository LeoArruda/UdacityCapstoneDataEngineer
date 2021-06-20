from typing import List, Optional, Union

from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.utils.redshift import build_credentials_block
from airflow.providers.postgres.hooks.postgres import PostgresHook

class S3ToRedshiftOperator(BaseOperator):
    """
    S3ToRedshiftOperator runs a copy of data from files at Amazon S3 and
    inserts into an specified table at Redshift.
    """
    template_fields = ('s3_bucket', 's3_key', 'schema', 'table', 'column_list', 'copy_options')
    template_ext = ()
    ui_color = '#f0f2a0'

    def __init__(
        self,
        *,
        schema: str,
        table: str,
        s3_bucket: str,
        s3_key: str,
        redshift_conn_id: str = 'redshift',
        aws_conn_id: str = 'my_aws_credentials',
        verify: Optional[Union[bool, str]] = None,
        column_list: Optional[List[str]] = None,
        copy_options: Optional[List] = None,
        autocommit: bool = False,
        truncate_table: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.schema = schema
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.verify = verify
        self.column_list = column_list
        self.copy_options = copy_options or []
        self.autocommit = autocommit
        self.truncate_table = truncate_table

    def _build_copy_query(self, credentials_block: str, copy_options: str) -> str:
        column_names = "(" + ", ".join(self.column_list) + ")" if self.column_list else ''
        return f"""
                    COPY {self.schema}.{self.table} {column_names}
                    FROM 's3://{self.s3_bucket}/{self.s3_key}'
                    with credentials
                    '{credentials_block}'
                    {copy_options};
        """

    def execute(self, context) -> None:
        postgres_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        s3_hook = S3Hook(aws_conn_id=self.aws_conn_id, verify=self.verify)
        credentials = s3_hook.get_credentials()
        credentials_block = build_credentials_block(credentials)
        copy_options = '\n\t\t\t'.join(self.copy_options)

        copy_statement = self._build_copy_query(credentials_block, copy_options)

        if self.truncate_table:
            truncate_statement = f'TRUNCATE TABLE {self.schema}.{self.table};'
            sql = f"""
            BEGIN;
            {truncate_statement}
            {copy_statement}
            COMMIT
            """
        else:
            sql = copy_statement

        self.log.info('Executing COPY command...')
        postgres_hook.run(sql, self.autocommit)
        self.log.info("COPY command complete...")