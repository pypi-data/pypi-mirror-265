.. figure:: ./DynaLockLogo.png
    :alt: DynaLock 
    :align: center


.. image:: https://img.shields.io/pypi/v/dynalock.svg
        :target: https://pypi.python.org/pypi/dynalock


.. image:: https://readthedocs.org/projects/dynalock/badge/?version=latest
        :target: https://dynalock.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Distributed locking implementation in python with DynamoDB

Getting Started
----------------
To install DynaLock, simply use pip:

.. code-block:: bash

    $ pip install dynalock


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



* Free software: MIT license
* Full Documentation: https://dynalock.readthedocs.io.




