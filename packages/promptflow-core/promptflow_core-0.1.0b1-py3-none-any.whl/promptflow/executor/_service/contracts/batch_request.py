# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from typing import Any, Mapping, Optional

from promptflow._constants import LINE_TIMEOUT_SEC
from promptflow.contracts.run_mode import RunMode
from promptflow.executor._service.contracts.base_request import BaseRequest
from promptflow.executor._service.contracts.execution_request import BaseExecutionRequest


class InitializationRequest(BaseExecutionRequest):
    """Request model for teh batch run initialization."""

    worker_count: Optional[int] = None
    line_timeout_sec: Optional[int] = LINE_TIMEOUT_SEC

    def get_run_mode(self):
        return RunMode.Batch


class LineExecutionRequest(BaseRequest):
    """Request model for line execution in the batch run."""

    run_id: str
    line_number: int
    inputs: Mapping[str, Any]


class AggregationRequest(BaseRequest):
    """Request model for executing aggregation nodes in the batch run."""

    run_id: str
    batch_inputs: Mapping[str, Any]
    aggregation_inputs: Mapping[str, Any]
