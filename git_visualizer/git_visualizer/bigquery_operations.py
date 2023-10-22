from google.cloud import bigquery
from models import Version
from typing import Optional

class BigQueryOperations:
    def __init__(self, dataset_id: str = 'git_visualizer', table_id: str = 'versions'):
        self.client = bigquery.Client()
        self.dataset_id = dataset_id
        self.table_id = table_id

    def save_to_bigquery(self, version: Version):
        # Specify the table
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        table = self.client.get_table(table_ref)

        # Insert the version data
        rows_to_insert = [(version.id, version.content, version.timestamp, version.project_id)]
        errors = self.client.insert_rows(table, rows_to_insert)

        if errors:
            raise Exception(f'Error occurred while inserting rows: {errors}')

    def get_version(self, version_id: int) -> Optional[str]:
        query = f"""
            SELECT content
            FROM `{self.dataset_id}.{self.table_id}`
            WHERE id = {version_id}
        """
        query_job = self.client.query(query)
        results = query_job.result()

        for row in results:
            return row.content

        return None
