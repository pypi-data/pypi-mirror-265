"""
Type annotations for deadline service client waiters.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_deadline.client import DeadlineCloudClient
    from mypy_boto3_deadline.waiter import (
        FleetActiveWaiter,
        JobCreateCompleteWaiter,
        LicenseEndpointDeletedWaiter,
        LicenseEndpointValidWaiter,
        QueueFleetAssociationStoppedWaiter,
        QueueSchedulingWaiter,
        QueueSchedulingBlockedWaiter,
    )

    session = Session()
    client: DeadlineCloudClient = session.client("deadline")

    fleet_active_waiter: FleetActiveWaiter = client.get_waiter("fleet_active")
    job_create_complete_waiter: JobCreateCompleteWaiter = client.get_waiter("job_create_complete")
    license_endpoint_deleted_waiter: LicenseEndpointDeletedWaiter = client.get_waiter("license_endpoint_deleted")
    license_endpoint_valid_waiter: LicenseEndpointValidWaiter = client.get_waiter("license_endpoint_valid")
    queue_fleet_association_stopped_waiter: QueueFleetAssociationStoppedWaiter = client.get_waiter("queue_fleet_association_stopped")
    queue_scheduling_waiter: QueueSchedulingWaiter = client.get_waiter("queue_scheduling")
    queue_scheduling_blocked_waiter: QueueSchedulingBlockedWaiter = client.get_waiter("queue_scheduling_blocked")
    ```
"""

from botocore.waiter import Waiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "FleetActiveWaiter",
    "JobCreateCompleteWaiter",
    "LicenseEndpointDeletedWaiter",
    "LicenseEndpointValidWaiter",
    "QueueFleetAssociationStoppedWaiter",
    "QueueSchedulingWaiter",
    "QueueSchedulingBlockedWaiter",
)

class FleetActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.FleetActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#fleetactivewaiter)
    """

    def wait(self, *, farmId: str, fleetId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.FleetActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#fleetactivewaiter)
        """

class JobCreateCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.JobCreateComplete)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#jobcreatecompletewaiter)
    """

    def wait(
        self, *, farmId: str, jobId: str, queueId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.JobCreateComplete.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#jobcreatecompletewaiter)
        """

class LicenseEndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.LicenseEndpointDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#licenseendpointdeletedwaiter)
    """

    def wait(self, *, licenseEndpointId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.LicenseEndpointDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#licenseendpointdeletedwaiter)
        """

class LicenseEndpointValidWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.LicenseEndpointValid)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#licenseendpointvalidwaiter)
    """

    def wait(self, *, licenseEndpointId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.LicenseEndpointValid.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#licenseendpointvalidwaiter)
        """

class QueueFleetAssociationStoppedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queuefleetassociationstoppedwaiter)
    """

    def wait(
        self, *, farmId: str, fleetId: str, queueId: str, WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queuefleetassociationstoppedwaiter)
        """

class QueueSchedulingWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueScheduling)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queueschedulingwaiter)
    """

    def wait(self, *, farmId: str, queueId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueScheduling.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queueschedulingwaiter)
        """

class QueueSchedulingBlockedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueSchedulingBlocked)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queueschedulingblockedwaiter)
    """

    def wait(self, *, farmId: str, queueId: str, WaiterConfig: WaiterConfigTypeDef = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Waiter.QueueSchedulingBlocked.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/waiters/#queueschedulingblockedwaiter)
        """
