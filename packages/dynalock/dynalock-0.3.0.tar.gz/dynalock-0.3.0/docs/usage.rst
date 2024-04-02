=====
Usage
=====

DynaLock utilizes Python's context manager making it easier and safer to manage locks. 
When used in a `with` statement, DynaLock automatically acquires the lock at the beginning of the block and releases it upon exiting, regardless of whether the block exits normally or with an exception. 
This eliminates the need for explicit release calls, reducing the boilerplate code and minimizing the risk of errors.

**Example Usage:**

.. code-block:: python

    from dynalock import DynaLock

    # Initialize a distributed lock
    distributed_lock = DynaLock(
        table_name='my_lock_table',
        region_name='us-west-2',
        lock_id='api_lock',
    )

    # Use the lock with a context manager
    with distributed_lock.lock():
        # Protected code goes here
        # The lock is automatically managed
        print("This code is protected by the lock")
        print("Critical section executed")
    
    # The lock is automatically released after exiting the block
    print("This code is not protected by the lock")

TTL
---
By default, DynaLock uses a Time-to-Live (TTL) mechanism to automatically release the lock if the process holding the lock crashes or fails to release it.
The TTL is set to 60 seconds by default, but you can customize it by passing the `ttl` parameter when initializing the lock.

**Example with Custom TTL:**

.. code-block:: python

    from dynalock import DynaLock

    # Initialize a distributed lock with a custom TTL of 120 seconds
    distributed_lock = DynaLock(
        table_name='my_lock_table',
        region_name='us-west-2',
        lock_id='api_lock',
        ttl=120,
    )

    # Use the lock with a context manager
    with distributed_lock.lock():
        # Protected code goes here
        print("This code is protected by the lock")
        print("Critical section executed")

    print("This code is not protected by the lock")

Error Handling
--------------

DynaLock defines custom exceptions to handle various lock-related errors gracefully:

- **LockAcquisitionError**: Raised when the lock cannot be acquired.
- **LockAlreadyAcquiredError**: Raised if the lock is already acquired by another process and cannot be acquired until it's released or expired.
- **LockReleaseError**: Raised when releasing the lock fails.

You do not need to handle these exceptions explicitly, as DynaLock automatically manages the lock and releases even if an exception occurs within the block.
These exceptions are provided for use cases where you might want to log or handle specific errors differently.

.. code-block:: python

    from dynalock import DynaLock, LockAcquisitionError

    distributed_lock = DynaLock(
        table_name='my_table',
        region_name='us-west-2',
        lock_id='api_lock',
    )

    try:
        with distributed_lock.lock():
            # Protected code goes here
            print("This code is protected by the lock")
            print("Critical section executed")
    except LockAcquisitionError as e:
        print(f"Failed to acquire lock: {e}")
        # Handle the error accordingly



AWS Access Credentials Setup
----------------------

DynaLock requires AWS access credentials to interact with DynamoDB for lock management. 
These credentials must be set up outside of the package, following standard AWS security best practices. 
Here are the common methods to configure your AWS credentials:

1. **Environment Variables**: Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as environment variables.

2. **AWS Credentials File**: Place your credentials in the AWS credentials file located at `~/.aws/credentials` (Linux & Mac) or `%USERPROFILE%\.aws\credentials` (Windows).

3. **AWS IAM Roles**: If DynaLock is used within an AWS service (e.g., EC2, Lambda), you can assign IAM roles to the service with the necessary permissions to access DynamoDB.

Please refer to the AWS documentation for more detailed instructions on setting up your access credentials.

By ensuring your AWS access credentials are correctly configured, DynaLock can seamlessly authenticate with AWS services, providing a secure and efficient way to manage distributed locks.


DynamoDB Table Setup
---------------------

Before using DynaLock, you need to create a DynamoDB table to store the lock information.
The table is quite simple should have the following attributes:

- **Partition Key (also known as Hash Key)**: `LockId` (String) - The unique identifier for the lock.
- **TTL Attribute**: `TTL` (Number) - The Time-to-Live attribute to automatically release the lock after a specified duration.

Here is an example of creating an example table using terraform:

.. code-block:: terraform
    # Specify the Terraform version and provider requirements
    terraform {
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = "~> 3.0"
        }
    }

    required_version = ">= 0.12"
    }

    # Configure the AWS Provider
    provider "aws" {
    region = "eu-west-2" # Specify your AWS region
    }

    # Create a DynamoDB table
    resource "aws_dynamodb_table" "example" {
    name           = "example-table" # Change this to your table name
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "LockId"

    attribute {
        name = "LockId"
        type = "S"
    }

    # Enable TTL
    ttl {
        attribute_name = "TTL"
        enabled        = true
    }

    tags = {
        Name = "ExampleTable"
    }
    }


You can refer to the AWS documentation for more detailed instructions on creating DynamoDB tables.


Conclusion
----------

DynaLock simplifies distributed lock management by leveraging the simplicity of AWS DynamoDB and the convenience of Python's context managers. 
By following the guidelines above for usage and AWS credential setup, you can easily integrate DynaLock into your distributed applications to enhance data consistency and prevent race conditions.


=================


