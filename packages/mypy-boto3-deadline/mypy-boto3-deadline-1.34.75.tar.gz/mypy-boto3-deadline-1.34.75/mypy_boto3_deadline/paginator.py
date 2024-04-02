"""
Type annotations for deadline service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_deadline.client import DeadlineCloudClient
    from mypy_boto3_deadline.paginator import (
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
        ListSessionsPaginator,
        ListSessionsForWorkerPaginator,
        ListStepConsumersPaginator,
        ListStepDependenciesPaginator,
        ListStepsPaginator,
        ListStorageProfilesPaginator,
        ListStorageProfilesForQueuePaginator,
        ListTasksPaginator,
        ListWorkersPaginator,
    )

    session = Session()
    client: DeadlineCloudClient = session.client("deadline")

    get_sessions_statistics_aggregation_paginator: GetSessionsStatisticsAggregationPaginator = client.get_paginator("get_sessions_statistics_aggregation")
    list_available_metered_products_paginator: ListAvailableMeteredProductsPaginator = client.get_paginator("list_available_metered_products")
    list_budgets_paginator: ListBudgetsPaginator = client.get_paginator("list_budgets")
    list_farm_members_paginator: ListFarmMembersPaginator = client.get_paginator("list_farm_members")
    list_farms_paginator: ListFarmsPaginator = client.get_paginator("list_farms")
    list_fleet_members_paginator: ListFleetMembersPaginator = client.get_paginator("list_fleet_members")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_job_members_paginator: ListJobMembersPaginator = client.get_paginator("list_job_members")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_license_endpoints_paginator: ListLicenseEndpointsPaginator = client.get_paginator("list_license_endpoints")
    list_metered_products_paginator: ListMeteredProductsPaginator = client.get_paginator("list_metered_products")
    list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    list_queue_environments_paginator: ListQueueEnvironmentsPaginator = client.get_paginator("list_queue_environments")
    list_queue_fleet_associations_paginator: ListQueueFleetAssociationsPaginator = client.get_paginator("list_queue_fleet_associations")
    list_queue_members_paginator: ListQueueMembersPaginator = client.get_paginator("list_queue_members")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_session_actions_paginator: ListSessionActionsPaginator = client.get_paginator("list_session_actions")
    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    list_sessions_for_worker_paginator: ListSessionsForWorkerPaginator = client.get_paginator("list_sessions_for_worker")
    list_step_consumers_paginator: ListStepConsumersPaginator = client.get_paginator("list_step_consumers")
    list_step_dependencies_paginator: ListStepDependenciesPaginator = client.get_paginator("list_step_dependencies")
    list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
    list_storage_profiles_paginator: ListStorageProfilesPaginator = client.get_paginator("list_storage_profiles")
    list_storage_profiles_for_queue_paginator: ListStorageProfilesForQueuePaginator = client.get_paginator("list_storage_profiles_for_queue")
    list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import BudgetStatusType, FleetStatusType, QueueStatusType
from .type_defs import (
    GetSessionsStatisticsAggregationResponseTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsResponsePaginatorTypeDef,
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
    ListTasksResponseTypeDef,
    ListWorkersResponsePaginatorTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetSessionsStatisticsAggregationPaginator",
    "ListAvailableMeteredProductsPaginator",
    "ListBudgetsPaginator",
    "ListFarmMembersPaginator",
    "ListFarmsPaginator",
    "ListFleetMembersPaginator",
    "ListFleetsPaginator",
    "ListJobMembersPaginator",
    "ListJobsPaginator",
    "ListLicenseEndpointsPaginator",
    "ListMeteredProductsPaginator",
    "ListMonitorsPaginator",
    "ListQueueEnvironmentsPaginator",
    "ListQueueFleetAssociationsPaginator",
    "ListQueueMembersPaginator",
    "ListQueuesPaginator",
    "ListSessionActionsPaginator",
    "ListSessionsPaginator",
    "ListSessionsForWorkerPaginator",
    "ListStepConsumersPaginator",
    "ListStepDependenciesPaginator",
    "ListStepsPaginator",
    "ListStorageProfilesPaginator",
    "ListStorageProfilesForQueuePaginator",
    "ListTasksPaginator",
    "ListWorkersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetSessionsStatisticsAggregationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
    """

    def paginate(
        self, *, aggregationId: str, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetSessionsStatisticsAggregationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
        """


class ListAvailableMeteredProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listavailablemeteredproductspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAvailableMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listavailablemeteredproductspaginator)
        """


class ListBudgetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListBudgets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listbudgetspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        status: BudgetStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListBudgets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listbudgetspaginator)
        """


class ListFarmMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarmMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmmemberspaginator)
    """

    def paginate(
        self, *, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFarmMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarmMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmmemberspaginator)
        """


class ListFarmsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarms)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmspaginator)
    """

    def paginate(
        self, *, principalId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFarmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFarms.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfarmspaginator)
        """


class ListFleetMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleetMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetmemberspaginator)
    """

    def paginate(
        self, *, farmId: str, fleetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFleetMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleetMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetmemberspaginator)
        """


class ListFleetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        displayName: str = ...,
        principalId: str = ...,
        status: FleetStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListFleetsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListFleets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listfleetspaginator)
        """


class ListJobMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobmemberspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListJobMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobmemberspaginator)
        """


class ListJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        queueId: str,
        principalId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listjobspaginator)
        """


class ListLicenseEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListLicenseEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listlicenseendpointspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLicenseEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListLicenseEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listlicenseendpointspaginator)
        """


class ListMeteredProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMeteredProducts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmeteredproductspaginator)
    """

    def paginate(
        self, *, licenseEndpointId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMeteredProducts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmeteredproductspaginator)
        """


class ListMonitorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMonitors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmonitorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListMonitors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listmonitorspaginator)
        """


class ListQueueEnvironmentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueEnvironments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueueenvironmentspaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQueueEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueEnvironments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueueenvironmentspaginator)
        """


class ListQueueFleetAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueFleetAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuefleetassociationspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        fleetId: str = ...,
        queueId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListQueueFleetAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueFleetAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuefleetassociationspaginator)
        """


class ListQueueMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuememberspaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQueueMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueueMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuememberspaginator)
        """


class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuespaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        principalId: str = ...,
        status: QueueStatusType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListQueues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listqueuespaginator)
        """


class ListSessionActionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionActions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionactionspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        sessionId: str = ...,
        taskId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListSessionActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionActions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionactionspaginator)
        """


class ListSessionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionspaginator)
        """


class ListSessionsForWorkerPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionsForWorker)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionsforworkerpaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        fleetId: str,
        workerId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListSessionsForWorkerResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSessionsForWorker.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listsessionsforworkerpaginator)
        """


class ListStepConsumersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepConsumers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepconsumerspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListStepConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepConsumers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepconsumerspaginator)
        """


class ListStepDependenciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepDependencies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepdependenciespaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListStepDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStepDependencies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepdependenciespaginator)
        """


class ListStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSteps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListSteps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststepspaginator)
        """


class ListStorageProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilespaginator)
    """

    def paginate(
        self, *, farmId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStorageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilespaginator)
        """


class ListStorageProfilesForQueuePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilesforqueuepaginator)
    """

    def paginate(
        self, *, farmId: str, queueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStorageProfilesForQueueResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#liststorageprofilesforqueuepaginator)
        """


class ListTasksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listtaskspaginator)
    """

    def paginate(
        self,
        *,
        farmId: str,
        jobId: str,
        queueId: str,
        stepId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listtaskspaginator)
        """


class ListWorkersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListWorkers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listworkerspaginator)
    """

    def paginate(
        self, *, farmId: str, fleetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListWorkersResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline.html#DeadlineCloud.Paginator.ListWorkers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_deadline/paginators/#listworkerspaginator)
        """
