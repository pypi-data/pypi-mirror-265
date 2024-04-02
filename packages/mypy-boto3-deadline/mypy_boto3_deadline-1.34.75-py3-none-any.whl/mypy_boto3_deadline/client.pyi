"""
Type annotations for deadline service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_deadline.client import DeadlineCloudClient

    session = Session()
    client: DeadlineCloudClient = session.client("deadline")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    BudgetStatusType,
    CreateJobTargetTaskRunStatusType,
    DefaultQueueBudgetActionType,
    EnvironmentTemplateTypeType,
    FleetStatusType,
    JobTargetTaskRunStatusType,
    JobTemplateTypeType,
    MembershipLevelType,
    PeriodType,
    PrincipalTypeType,
    QueueStatusType,
    StepTargetTaskRunStatusType,
    StorageProfileOperatingSystemFamilyType,
    TaskTargetRunStatusType,
    UpdatedWorkerStatusType,
    UpdateQueueFleetAssociationStatusType,
    UsageGroupByFieldType,
    UsageStatisticType,
)
from .paginator import (
    GetSessionsStatisticsAggregationPaginator,
    ListAvailableMeteredProductsPaginator,
    ListBudgetsPaginator,
    ListFarmMembersPaginator,
    ListFarmsPaginator,
    ListFleetMembersPaginator,
    ListFleetsPaginator,
    ListJobMembersPaginator,
    ListJobsPaginator,
    ListLicenseEndpointsPaginator,
    ListMeteredProductsPaginator,
    ListMonitorsPaginator,
    ListQueueEnvironmentsPaginator,
    ListQueueFleetAssociationsPaginator,
    ListQueueMembersPaginator,
    ListQueuesPaginator,
    ListSessionActionsPaginator,
    ListSessionsForWorkerPaginator,
    ListSessionsPaginator,
    ListStepConsumersPaginator,
    ListStepDependenciesPaginator,
    ListStepsPaginator,
    ListStorageProfilesForQueuePaginator,
    ListStorageProfilesPaginator,
    ListTasksPaginator,
    ListWorkersPaginator,
)
from .type_defs import (
    AssumeFleetRoleForReadResponseTypeDef,
    AssumeFleetRoleForWorkerResponseTypeDef,
    AssumeQueueRoleForReadResponseTypeDef,
    AssumeQueueRoleForUserResponseTypeDef,
    AssumeQueueRoleForWorkerResponseTypeDef,
    AttachmentsTypeDef,
    BatchGetJobEntityResponseTypeDef,
    BudgetActionToAddTypeDef,
    BudgetActionToRemoveTypeDef,
    BudgetScheduleTypeDef,
    CopyJobTemplateResponseTypeDef,
    CreateBudgetResponseTypeDef,
    CreateFarmResponseTypeDef,
    CreateFleetResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateLicenseEndpointResponseTypeDef,
    CreateMonitorResponseTypeDef,
    CreateQueueEnvironmentResponseTypeDef,
    CreateQueueResponseTypeDef,
    CreateStorageProfileResponseTypeDef,
    CreateWorkerResponseTypeDef,
    FileSystemLocationTypeDef,
    FleetConfigurationTypeDef,
    GetBudgetResponseTypeDef,
    GetFarmResponseTypeDef,
    GetFleetResponseTypeDef,
    GetJobResponseTypeDef,
    GetLicenseEndpointResponseTypeDef,
    GetMonitorResponseTypeDef,
    GetQueueEnvironmentResponseTypeDef,
    GetQueueFleetAssociationResponseTypeDef,
    GetQueueResponseTypeDef,
    GetSessionActionResponseTypeDef,
    GetSessionResponseTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    GetStepResponseTypeDef,
    GetStorageProfileForQueueResponseTypeDef,
    GetStorageProfileResponseTypeDef,
    GetTaskResponseTypeDef,
    GetWorkerResponseTypeDef,
    HostPropertiesRequestTypeDef,
    JobAttachmentSettingsTypeDef,
    JobEntityIdentifiersUnionTypeDef,
    JobParameterTypeDef,
    JobRunAsUserTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersResponseTypeDef,
    S3LocationTypeDef,
    SearchGroupedFilterExpressionsTypeDef,
    SearchJobsResponseTypeDef,
    SearchSortExpressionTypeDef,
    SearchStepsResponseTypeDef,
    SearchTasksResponseTypeDef,
    SearchWorkersResponseTypeDef,
    SessionsStatisticsResourcesTypeDef,
    StartSessionsStatisticsAggregationResponseTypeDef,
    TimestampTypeDef,
    UpdatedSessionActionInfoTypeDef,
    UpdateWorkerResponseTypeDef,
    UpdateWorkerScheduleResponseTypeDef,
    UsageTrackingResourceTypeDef,
    WorkerCapabilitiesTypeDef,
)
from .waiter import (
    FleetActiveWaiter,
    JobCreateCompleteWaiter,
    LicenseEndpointDeletedWaiter,
    LicenseEndpointValidWaiter,
    QueueFleetAssociationStoppedWaiter,
    QueueSchedulingBlockedWaiter,
    QueueSchedulingWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DeadlineCloudClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DeadlineCloudClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DeadlineCloudClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#exceptions)
        """

    def associate_member_to_farm(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
    ) -> Dict[str, Any]:
        """
        Assigns a farm membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#associate_member_to_farm)
        """

    def associate_member_to_fleet(
        self,
        *,
        farmId: str,
        fleetId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
    ) -> Dict[str, Any]:
        """
        Assigns a fleet membership level to a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#associate_member_to_fleet)
        """

    def associate_member_to_job(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        jobId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
        queueId: str,
    ) -> Dict[str, Any]:
        """
        Assigns a job membership level to a member See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/deadline-2023-10-12/AssociateMemberToJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#associate_member_to_job)
        """

    def associate_member_to_queue(
        self,
        *,
        farmId: str,
        identityStoreId: str,
        membershipLevel: MembershipLevelType,
        principalId: str,
        principalType: PrincipalTypeType,
        queueId: str,
    ) -> Dict[str, Any]:
        """
        Assigns a queue membership level to a member See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/deadline-2023-10-12/AssociateMemberToQueue).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.associate_member_to_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#associate_member_to_queue)
        """

    def assume_fleet_role_for_read(
        self, *, farmId: str, fleetId: str
    ) -> AssumeFleetRoleForReadResponseTypeDef:
        """
        Get Amazon Web Services credentials from the fleet role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_fleet_role_for_read)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#assume_fleet_role_for_read)
        """

    def assume_fleet_role_for_worker(
        self, *, farmId: str, fleetId: str, workerId: str
    ) -> AssumeFleetRoleForWorkerResponseTypeDef:
        """
        Get credentials from the fleet role for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_fleet_role_for_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#assume_fleet_role_for_worker)
        """

    def assume_queue_role_for_read(
        self, *, farmId: str, queueId: str
    ) -> AssumeQueueRoleForReadResponseTypeDef:
        """
        Gets Amazon Web Services credentials from the queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_read)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#assume_queue_role_for_read)
        """

    def assume_queue_role_for_user(
        self, *, farmId: str, queueId: str
    ) -> AssumeQueueRoleForUserResponseTypeDef:
        """
        Allows a user to assume a role for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_user)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#assume_queue_role_for_user)
        """

    def assume_queue_role_for_worker(
        self, *, farmId: str, fleetId: str, queueId: str, workerId: str
    ) -> AssumeQueueRoleForWorkerResponseTypeDef:
        """
        Allows a worker to assume a queue role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.assume_queue_role_for_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#assume_queue_role_for_worker)
        """

    def batch_get_job_entity(
        self,
        *,
        farmId: str,
        fleetId: str,
        identifiers: Sequence[JobEntityIdentifiersUnionTypeDef],
        workerId: str,
    ) -> BatchGetJobEntityResponseTypeDef:
        """
        Get batched job details for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.batch_get_job_entity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#batch_get_job_entity)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#close)
        """

    def copy_job_template(
        self, *, farmId: str, jobId: str, queueId: str, targetS3Location: S3LocationTypeDef
    ) -> CopyJobTemplateResponseTypeDef:
        """
        Copies a job template to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.copy_job_template)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#copy_job_template)
        """

    def create_budget(
        self,
        *,
        actions: Sequence[BudgetActionToAddTypeDef],
        approximateDollarLimit: float,
        displayName: str,
        farmId: str,
        schedule: BudgetScheduleTypeDef,
        usageTrackingResource: UsageTrackingResourceTypeDef,
        clientToken: str = ...,
        description: str = ...,
    ) -> CreateBudgetResponseTypeDef:
        """
        Creates a budget to set spending thresholds for your rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_budget)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_budget)
        """

    def create_farm(
        self,
        *,
        displayName: str,
        clientToken: str = ...,
        description: str = ...,
        kmsKeyArn: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFarmResponseTypeDef:
        """
        Creates a farm to allow space for queues and fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_farm)
        """

    def create_fleet(
        self,
        *,
        configuration: FleetConfigurationTypeDef,
        displayName: str,
        farmId: str,
        maxWorkerCount: int,
        roleArn: str,
        clientToken: str = ...,
        description: str = ...,
        minWorkerCount: int = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateFleetResponseTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_fleet)
        """

    def create_job(
        self,
        *,
        farmId: str,
        priority: int,
        queueId: str,
        template: str,
        templateType: JobTemplateTypeType,
        attachments: AttachmentsTypeDef = ...,
        clientToken: str = ...,
        maxFailedTasksCount: int = ...,
        maxRetriesPerTask: int = ...,
        parameters: Mapping[str, JobParameterTypeDef] = ...,
        storageProfileId: str = ...,
        targetTaskRunStatus: CreateJobTargetTaskRunStatusType = ...,
    ) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_job)
        """

    def create_license_endpoint(
        self,
        *,
        securityGroupIds: Sequence[str],
        subnetIds: Sequence[str],
        vpcId: str,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateLicenseEndpointResponseTypeDef:
        """
        Creates a license endpoint to integrate your various licensed software used for
        rendering on Deadline
        Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_license_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_license_endpoint)
        """

    def create_monitor(
        self,
        *,
        displayName: str,
        identityCenterInstanceArn: str,
        roleArn: str,
        subdomain: str,
        clientToken: str = ...,
    ) -> CreateMonitorResponseTypeDef:
        """
        Creates an Amazon Web Services Deadline Cloud monitor that you can use to view
        your farms, queues, and
        fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_monitor)
        """

    def create_queue(
        self,
        *,
        displayName: str,
        farmId: str,
        allowedStorageProfileIds: Sequence[str] = ...,
        clientToken: str = ...,
        defaultBudgetAction: DefaultQueueBudgetActionType = ...,
        description: str = ...,
        jobAttachmentSettings: JobAttachmentSettingsTypeDef = ...,
        jobRunAsUser: JobRunAsUserTypeDef = ...,
        requiredFileSystemLocationNames: Sequence[str] = ...,
        roleArn: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a queue to coordinate the order in which jobs run on a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_queue)
        """

    def create_queue_environment(
        self,
        *,
        farmId: str,
        priority: int,
        queueId: str,
        template: str,
        templateType: EnvironmentTemplateTypeType,
        clientToken: str = ...,
    ) -> CreateQueueEnvironmentResponseTypeDef:
        """
        Creates an environment for a queue that defines how jobs in the queue run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_queue_environment)
        """

    def create_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Creates an association between a queue and a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_queue_fleet_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_queue_fleet_association)
        """

    def create_storage_profile(
        self,
        *,
        displayName: str,
        farmId: str,
        osFamily: StorageProfileOperatingSystemFamilyType,
        clientToken: str = ...,
        fileSystemLocations: Sequence[FileSystemLocationTypeDef] = ...,
    ) -> CreateStorageProfileResponseTypeDef:
        """
        Creates a storage profile that specifies the operating system, file type, and
        file location of resources used on a
        farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_storage_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_storage_profile)
        """

    def create_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        clientToken: str = ...,
        hostProperties: HostPropertiesRequestTypeDef = ...,
    ) -> CreateWorkerResponseTypeDef:
        """
        Creates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.create_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#create_worker)
        """

    def delete_budget(self, *, budgetId: str, farmId: str) -> Dict[str, Any]:
        """
        Deletes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_budget)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_budget)
        """

    def delete_farm(self, *, farmId: str) -> Dict[str, Any]:
        """
        Deletes a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_farm)
        """

    def delete_fleet(self, *, farmId: str, fleetId: str, clientToken: str = ...) -> Dict[str, Any]:
        """
        Deletes a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_fleet)
        """

    def delete_license_endpoint(self, *, licenseEndpointId: str) -> Dict[str, Any]:
        """
        Deletes a license endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_license_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_license_endpoint)
        """

    def delete_metered_product(self, *, licenseEndpointId: str, productId: str) -> Dict[str, Any]:
        """
        Deletes a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_metered_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_metered_product)
        """

    def delete_monitor(self, *, monitorId: str) -> Dict[str, Any]:
        """
        Removes a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_monitor)
        """

    def delete_queue(self, *, farmId: str, queueId: str) -> Dict[str, Any]:
        """
        Deletes a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_queue)
        """

    def delete_queue_environment(
        self, *, farmId: str, queueEnvironmentId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Deletes a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_queue_environment)
        """

    def delete_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Deletes a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_queue_fleet_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_queue_fleet_association)
        """

    def delete_storage_profile(self, *, farmId: str, storageProfileId: str) -> Dict[str, Any]:
        """
        Deletes a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_storage_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_storage_profile)
        """

    def delete_worker(self, *, farmId: str, fleetId: str, workerId: str) -> Dict[str, Any]:
        """
        Deletes a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.delete_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#delete_worker)
        """

    def disassociate_member_from_farm(self, *, farmId: str, principalId: str) -> Dict[str, Any]:
        """
        Disassociates a member from a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#disassociate_member_from_farm)
        """

    def disassociate_member_from_fleet(
        self, *, farmId: str, fleetId: str, principalId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#disassociate_member_from_fleet)
        """

    def disassociate_member_from_job(
        self, *, farmId: str, jobId: str, principalId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#disassociate_member_from_job)
        """

    def disassociate_member_from_queue(
        self, *, farmId: str, principalId: str, queueId: str
    ) -> Dict[str, Any]:
        """
        Disassociates a member from a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.disassociate_member_from_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#disassociate_member_from_queue)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#generate_presigned_url)
        """

    def get_budget(self, *, budgetId: str, farmId: str) -> GetBudgetResponseTypeDef:
        """
        Get a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_budget)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_budget)
        """

    def get_farm(self, *, farmId: str) -> GetFarmResponseTypeDef:
        """
        Get a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_farm)
        """

    def get_fleet(self, *, farmId: str, fleetId: str) -> GetFleetResponseTypeDef:
        """
        Get a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_fleet)
        """

    def get_job(self, *, farmId: str, jobId: str, queueId: str) -> GetJobResponseTypeDef:
        """
        Gets a Deadline Cloud job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_job)
        """

    def get_license_endpoint(self, *, licenseEndpointId: str) -> GetLicenseEndpointResponseTypeDef:
        """
        Gets a licence endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_license_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_license_endpoint)
        """

    def get_monitor(self, *, monitorId: str) -> GetMonitorResponseTypeDef:
        """
        Gets information about the specified monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_monitor)
        """

    def get_queue(self, *, farmId: str, queueId: str) -> GetQueueResponseTypeDef:
        """
        Gets a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_queue)
        """

    def get_queue_environment(
        self, *, farmId: str, queueEnvironmentId: str, queueId: str
    ) -> GetQueueEnvironmentResponseTypeDef:
        """
        Gets a queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_queue_environment)
        """

    def get_queue_fleet_association(
        self, *, farmId: str, fleetId: str, queueId: str
    ) -> GetQueueFleetAssociationResponseTypeDef:
        """
        Gets a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_queue_fleet_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_queue_fleet_association)
        """

    def get_session(
        self, *, farmId: str, jobId: str, queueId: str, sessionId: str
    ) -> GetSessionResponseTypeDef:
        """
        Gets a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_session)
        """

    def get_session_action(
        self, *, farmId: str, jobId: str, queueId: str, sessionActionId: str
    ) -> GetSessionActionResponseTypeDef:
        """
        Gets a session action for the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_session_action)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_session_action)
        """

    def get_sessions_statistics_aggregation(
        self, *, aggregationId: str, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> GetSessionsStatisticsAggregationResponseTypeDef:
        """
        Gets a set of statistics for queues or farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_sessions_statistics_aggregation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_sessions_statistics_aggregation)
        """

    def get_step(
        self, *, farmId: str, jobId: str, queueId: str, stepId: str
    ) -> GetStepResponseTypeDef:
        """
        Gets a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_step)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_step)
        """

    def get_storage_profile(
        self, *, farmId: str, storageProfileId: str
    ) -> GetStorageProfileResponseTypeDef:
        """
        Gets a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_storage_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_storage_profile)
        """

    def get_storage_profile_for_queue(
        self, *, farmId: str, queueId: str, storageProfileId: str
    ) -> GetStorageProfileForQueueResponseTypeDef:
        """
        Gets a storage profile for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_storage_profile_for_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_storage_profile_for_queue)
        """

    def get_task(
        self, *, farmId: str, jobId: str, queueId: str, stepId: str, taskId: str
    ) -> GetTaskResponseTypeDef:
        """
        Gets a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_task)
        """

    def get_worker(self, *, farmId: str, fleetId: str, workerId: str) -> GetWorkerResponseTypeDef:
        """
        Gets a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_worker)
        """

    def list_available_metered_products(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListAvailableMeteredProductsResponseTypeDef:
        """
        A list of the available metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_available_metered_products)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_available_metered_products)
        """

    def list_budgets(
        self,
        *,
        farmId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: BudgetStatusType = ...,
    ) -> ListBudgetsResponseTypeDef:
        """
        A list of budgets in a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_budgets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_budgets)
        """

    def list_farm_members(
        self, *, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFarmMembersResponseTypeDef:
        """
        Lists the members of a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_farm_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_farm_members)
        """

    def list_farms(
        self, *, maxResults: int = ..., nextToken: str = ..., principalId: str = ...
    ) -> ListFarmsResponseTypeDef:
        """
        Lists farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_farms)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_farms)
        """

    def list_fleet_members(
        self, *, farmId: str, fleetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListFleetMembersResponseTypeDef:
        """
        Lists fleet members.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_fleet_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_fleet_members)
        """

    def list_fleets(
        self,
        *,
        farmId: str,
        displayName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
        status: FleetStatusType = ...,
    ) -> ListFleetsResponseTypeDef:
        """
        Lists fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_fleets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_fleets)
        """

    def list_job_members(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListJobMembersResponseTypeDef:
        """
        Lists members on a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_job_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_job_members)
        """

    def list_jobs(
        self,
        *,
        farmId: str,
        queueId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
    ) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_jobs)
        """

    def list_license_endpoints(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListLicenseEndpointsResponseTypeDef:
        """
        Lists license endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_license_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_license_endpoints)
        """

    def list_metered_products(
        self, *, licenseEndpointId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListMeteredProductsResponseTypeDef:
        """
        Lists metered products.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_metered_products)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_metered_products)
        """

    def list_monitors(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListMonitorsResponseTypeDef:
        """
        Gets a list of your monitors in Deadline Cloud.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_monitors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_monitors)
        """

    def list_queue_environments(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListQueueEnvironmentsResponseTypeDef:
        """
        Lists queue environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_environments)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_queue_environments)
        """

    def list_queue_fleet_associations(
        self,
        *,
        farmId: str,
        fleetId: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        queueId: str = ...,
    ) -> ListQueueFleetAssociationsResponseTypeDef:
        """
        Lists queue-fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_fleet_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_queue_fleet_associations)
        """

    def list_queue_members(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListQueueMembersResponseTypeDef:
        """
        Lists the members in a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queue_members)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_queue_members)
        """

    def list_queues(
        self,
        *,
        farmId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        principalId: str = ...,
        status: QueueStatusType = ...,
    ) -> ListQueuesResponseTypeDef:
        """
        Lists queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_queues)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_queues)
        """

    def list_session_actions(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        maxResults: int = ...,
        nextToken: str = ...,
        sessionId: str = ...,
        taskId: str = ...,
    ) -> ListSessionActionsResponseTypeDef:
        """
        Lists session actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_session_actions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_session_actions)
        """

    def list_sessions(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListSessionsResponseTypeDef:
        """
        Lists sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_sessions)
        """

    def list_sessions_for_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListSessionsForWorkerResponseTypeDef:
        """
        Lists sessions for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_sessions_for_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_sessions_for_worker)
        """

    def list_step_consumers(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListStepConsumersResponseTypeDef:
        """
        Lists step consumers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_step_consumers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_step_consumers)
        """

    def list_step_dependencies(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListStepDependenciesResponseTypeDef:
        """
        Lists the dependencies for a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_step_dependencies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_step_dependencies)
        """

    def list_steps(
        self, *, farmId: str, jobId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStepsResponseTypeDef:
        """
        Lists steps for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_steps)
        """

    def list_storage_profiles(
        self, *, farmId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStorageProfilesResponseTypeDef:
        """
        Lists storage profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_storage_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_storage_profiles)
        """

    def list_storage_profiles_for_queue(
        self, *, farmId: str, queueId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListStorageProfilesForQueueResponseTypeDef:
        """
        Lists storage profiles for a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_storage_profiles_for_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_storage_profiles_for_queue)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_tags_for_resource)
        """

    def list_tasks(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListTasksResponseTypeDef:
        """
        Lists tasks for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_tasks)
        """

    def list_workers(
        self, *, farmId: str, fleetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkersResponseTypeDef:
        """
        Lists workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.list_workers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#list_workers)
        """

    def put_metered_product(self, *, licenseEndpointId: str, productId: str) -> Dict[str, Any]:
        """
        Adds a metered product.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.put_metered_product)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#put_metered_product)
        """

    def search_jobs(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchJobsResponseTypeDef:
        """
        Searches for jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#search_jobs)
        """

    def search_steps(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        jobId: str = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchStepsResponseTypeDef:
        """
        Searches for steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#search_steps)
        """

    def search_tasks(
        self,
        *,
        farmId: str,
        itemOffset: int,
        queueIds: Sequence[str],
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        jobId: str = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchTasksResponseTypeDef:
        """
        Searches for tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#search_tasks)
        """

    def search_workers(
        self,
        *,
        farmId: str,
        fleetIds: Sequence[str],
        itemOffset: int,
        filterExpressions: "SearchGroupedFilterExpressionsTypeDef" = ...,
        pageSize: int = ...,
        sortExpressions: Sequence[SearchSortExpressionTypeDef] = ...,
    ) -> SearchWorkersResponseTypeDef:
        """
        Searches for workers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.search_workers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#search_workers)
        """

    def start_sessions_statistics_aggregation(
        self,
        *,
        endTime: TimestampTypeDef,
        farmId: str,
        groupBy: Sequence[UsageGroupByFieldType],
        resourceIds: SessionsStatisticsResourcesTypeDef,
        startTime: TimestampTypeDef,
        statistics: Sequence[UsageStatisticType],
        period: PeriodType = ...,
        timezone: str = ...,
    ) -> StartSessionsStatisticsAggregationResponseTypeDef:
        """
        Starts an asynchronous request for getting aggregated statistics about queues
        and
        farms.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.start_sessions_statistics_aggregation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#start_sessions_statistics_aggregation)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str] = ...) -> Dict[str, Any]:
        """
        Tags a resource using the resource's ARN and desired tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from a resource using the resource's ARN and tag to remove.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#untag_resource)
        """

    def update_budget(
        self,
        *,
        budgetId: str,
        farmId: str,
        actionsToAdd: Sequence[BudgetActionToAddTypeDef] = ...,
        actionsToRemove: Sequence[BudgetActionToRemoveTypeDef] = ...,
        approximateDollarLimit: float = ...,
        clientToken: str = ...,
        description: str = ...,
        displayName: str = ...,
        schedule: BudgetScheduleTypeDef = ...,
        status: BudgetStatusType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a budget that sets spending thresholds for rendering activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_budget)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_budget)
        """

    def update_farm(
        self, *, farmId: str, description: str = ..., displayName: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a farm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_farm)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_farm)
        """

    def update_fleet(
        self,
        *,
        farmId: str,
        fleetId: str,
        clientToken: str = ...,
        configuration: FleetConfigurationTypeDef = ...,
        description: str = ...,
        displayName: str = ...,
        maxWorkerCount: int = ...,
        minWorkerCount: int = ...,
        roleArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_fleet)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_fleet)
        """

    def update_job(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        clientToken: str = ...,
        lifecycleStatus: Literal["ARCHIVED"] = ...,
        maxFailedTasksCount: int = ...,
        maxRetriesPerTask: int = ...,
        priority: int = ...,
        targetTaskRunStatus: JobTargetTaskRunStatusType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_job)
        """

    def update_monitor(
        self, *, monitorId: str, displayName: str = ..., roleArn: str = ..., subdomain: str = ...
    ) -> Dict[str, Any]:
        """
        Modifies the settings for a Deadline Cloud monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_monitor)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_monitor)
        """

    def update_queue(
        self,
        *,
        farmId: str,
        queueId: str,
        allowedStorageProfileIdsToAdd: Sequence[str] = ...,
        allowedStorageProfileIdsToRemove: Sequence[str] = ...,
        clientToken: str = ...,
        defaultBudgetAction: DefaultQueueBudgetActionType = ...,
        description: str = ...,
        displayName: str = ...,
        jobAttachmentSettings: JobAttachmentSettingsTypeDef = ...,
        jobRunAsUser: JobRunAsUserTypeDef = ...,
        requiredFileSystemLocationNamesToAdd: Sequence[str] = ...,
        requiredFileSystemLocationNamesToRemove: Sequence[str] = ...,
        roleArn: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_queue)
        """

    def update_queue_environment(
        self,
        *,
        farmId: str,
        queueEnvironmentId: str,
        queueId: str,
        clientToken: str = ...,
        priority: int = ...,
        template: str = ...,
        templateType: EnvironmentTemplateTypeType = ...,
    ) -> Dict[str, Any]:
        """
        Updates the queue environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue_environment)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_queue_environment)
        """

    def update_queue_fleet_association(
        self,
        *,
        farmId: str,
        fleetId: str,
        queueId: str,
        status: UpdateQueueFleetAssociationStatusType,
    ) -> Dict[str, Any]:
        """
        Updates a queue-fleet association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_queue_fleet_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_queue_fleet_association)
        """

    def update_session(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        sessionId: str,
        targetLifecycleStatus: Literal["ENDED"],
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_session)
        """

    def update_step(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        targetTaskRunStatus: StepTargetTaskRunStatusType,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_step)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_step)
        """

    def update_storage_profile(
        self,
        *,
        farmId: str,
        storageProfileId: str,
        clientToken: str = ...,
        displayName: str = ...,
        fileSystemLocationsToAdd: Sequence[FileSystemLocationTypeDef] = ...,
        fileSystemLocationsToRemove: Sequence[FileSystemLocationTypeDef] = ...,
        osFamily: StorageProfileOperatingSystemFamilyType = ...,
    ) -> Dict[str, Any]:
        """
        Updates a storage profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_storage_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_storage_profile)
        """

    def update_task(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        targetRunStatus: TaskTargetRunStatusType,
        taskId: str,
        clientToken: str = ...,
    ) -> Dict[str, Any]:
        """
        Updates a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_task)
        """

    def update_worker(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        capabilities: WorkerCapabilitiesTypeDef = ...,
        hostProperties: HostPropertiesRequestTypeDef = ...,
        status: UpdatedWorkerStatusType = ...,
    ) -> UpdateWorkerResponseTypeDef:
        """
        Updates a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_worker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_worker)
        """

    def update_worker_schedule(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        updatedSessionActions: Mapping[str, UpdatedSessionActionInfoTypeDef] = ...,
    ) -> UpdateWorkerScheduleResponseTypeDef:
        """
        Updates the schedule for a worker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.update_worker_schedule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#update_worker_schedule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_sessions_statistics_aggregation"]
    ) -> GetSessionsStatisticsAggregationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_available_metered_products"]
    ) -> ListAvailableMeteredProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_budgets"]) -> ListBudgetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_farm_members"]
    ) -> ListFarmMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_farms"]) -> ListFarmsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_fleet_members"]
    ) -> ListFleetMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_fleets"]) -> ListFleetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_members"]) -> ListJobMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_endpoints"]
    ) -> ListLicenseEndpointsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_metered_products"]
    ) -> ListMeteredProductsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_environments"]
    ) -> ListQueueEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_fleet_associations"]
    ) -> ListQueueFleetAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_queue_members"]
    ) -> ListQueueMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_session_actions"]
    ) -> ListSessionActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sessions"]) -> ListSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sessions_for_worker"]
    ) -> ListSessionsForWorkerPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_consumers"]
    ) -> ListStepConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_step_dependencies"]
    ) -> ListStepDependenciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_steps"]) -> ListStepsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles"]
    ) -> ListStorageProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_profiles_for_queue"]
    ) -> ListStorageProfilesForQueuePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workers"]) -> ListWorkersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["fleet_active"]) -> FleetActiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["job_create_complete"]) -> JobCreateCompleteWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_deleted"]
    ) -> LicenseEndpointDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["license_endpoint_valid"]
    ) -> LicenseEndpointValidWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_fleet_association_stopped"]
    ) -> QueueFleetAssociationStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["queue_scheduling"]) -> QueueSchedulingWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["queue_scheduling_blocked"]
    ) -> QueueSchedulingBlockedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Client.get_waiter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/client/#get_waiter)
        """
