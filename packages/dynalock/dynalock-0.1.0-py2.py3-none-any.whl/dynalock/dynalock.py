import time
from contextlib import contextmanager

import boto3
from botocore.exceptions import ClientError


class LockAcquisitionError(Exception):
    pass

class LockAlreadyAcquiredError(Exception):
    pass

class LockReleaseError(Exception):
    pass


class DynaLock:
    DEFALUT_LOCK_TTL = 60

    def __init__(self, lock_id, region_name=None, table_name=None):
        self.region_name = region_name 
        self.table_name = table_name

        if not self.table_name or not self.region_name or not lock_id:
            raise ValueError(
                "Please provide a valid dynamodb table name, aws region name and lock id."
            )

        self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)
        self.table = self.dynamodb.Table(name=self.table_name)
        self.lock_id = lock_id
        self.lock_acquired = False

    def _acquire_lock(self, ttl=DEFALUT_LOCK_TTL):
        try:
            self.table.put_item(
                Item={"LockId": self.lock_id, "TTL": int(time.time()) + ttl},
                ConditionExpression="attribute_not_exists(LockID) OR #T < :current_time",
                ExpressionAttributeNames={"#T": "TTL"},
                ExpressionAttributeValues={":current_time": int(time.time())},
            )
            self.lock_acquired = True
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise LockAlreadyAcquiredError("Lock already acquired. Cannot acquire until released or expired.")
            else:
                raise


    def _release_lock(self):
        if not self.lock_acquired:
            return False
        try:
            self.table.delete_item(Key={"LockId": self.lock_id})
            self.lock_acquired = False
            return True
        except ClientError as e:
            raise LockReleaseError("Failed to release lock.") from e



    @contextmanager
    def lock(self, ttl=DEFALUT_LOCK_TTL):
        try:
            if self._acquire_lock(ttl):
                yield self
            else:
                raise LockAcquisitionError("Failed to acquire lock.")
        except Exception as e:
            raise e
        finally:
            if self.lock_acquired:
                self._release_lock()
