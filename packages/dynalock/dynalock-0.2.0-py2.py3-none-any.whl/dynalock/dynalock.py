import time
from contextlib import contextmanager
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from .exceptions import LockAcquisitionError, LockAlreadyAcquiredError, LockReleaseError


class DynaLock:
    DEFAULT_LOCK_TTL: int = 60

    def __init__(
        self,
        lock_id: Optional[str] = None,
        region_name: Optional[str] = None,
        table_name: Optional[str] = None,
        ttl: int = DEFAULT_LOCK_TTL,
    ) -> None:
        """
        Initialize a DynaLock object.

        Args:
            lock_id (str): The ID of the lock.
            region_name (str): The name of the AWS region.
            table_name (str): The name of the DynamoDB table.
            ttl (int): The time-to-live (TTL) of the lock.
        """
        self.region_name = region_name 
        self.table_name = table_name
        self.ttl = ttl

        if not self.table_name or not self.region_name or not lock_id:
            raise ValueError(
                "Please provide a valid dynamodb table name, aws region name and lock id."
            )

        self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)
        self.table = self.dynamodb.Table(name=self.table_name)
        self.lock_id = lock_id
        self.lock_acquired = False

    def _acquire_lock(self) -> bool:
        """
        Try to acquire the lock.

        Returns:
            bool: True if the lock was acquired, False otherwise.

        Raises:
            LockAlreadyAcquiredError: If the lock is already acquired and cannot be acquired until released or expired.
        """
        try:
            self.table.put_item(
                Item={"LockId": self.lock_id, "TTL": int(time.time()) + self.ttl},
                ConditionExpression="attribute_not_exists(LockId) OR #T < :current_time",
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

    def _release_lock(self) -> bool:
        """
        Release the lock.

        Returns:
            bool: True if the lock was released, False otherwise.

        Raises:
            LockReleaseError: If the lock release failed.
        """
        if not self.lock_acquired:
            return False
        try:
            self.table.delete_item(Key={"LockId": self.lock_id})
            self.lock_acquired = False
            return True
        except ClientError as e:
            raise LockReleaseError("Failed to release lock.") from e

    @contextmanager
    def lock(self):
        """
        Context manager for acquiring and automatically releasing the lock.

        Raises:
            LockAcquisitionError: If the lock acquisition failed.
            LockAlreadyAcquiredError: If the lock is already acquired and cannot be acquired until released or expired.
            LockReleaseError: If the lock release failed.
        """
        try:
            if self._acquire_lock():
                yield self
            else:
                raise LockAcquisitionError("Failed to acquire lock.")
        except Exception as e:
            raise e
        finally:
            if self.lock_acquired:
                self._release_lock()