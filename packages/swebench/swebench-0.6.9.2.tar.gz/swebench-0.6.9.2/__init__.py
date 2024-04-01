__version__ = "0.6.9.2"

from collect.build_dataset import main as build_dataset
from collect.get_tasks_pipeline import main as get_tasks_pipeline
from collect.print_pulls import main as print_pulls

from harness.constants import (
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION,
    MAP_REPO_TO_TEST_FRAMEWORK,
    MAP_VERSION_TO_INSTALL,
)

from harness.run_evaluation import (
  main as run_evaluation,
)

from harness.utils import (
    get_environment_yml,
    get_instances,
    get_requirements,
)

from metrics.conversion import (
    convert_log_to_ground_truth
)

from metrics.getters import (
    get_diffs,
    get_logs_eval,
    get_logs_gold,
)

from metrics.log_parsers import (
    MAP_REPO_TO_PARSER,
)

from metrics.metrics import (
    compute_fail_to_pass,
    compute_fail_to_pass_unweighted,
    compute_fail_to_pass_weighted,
    compute_pass_to_pass,
    compute_pass_to_pass_unweighted,
    compute_pass_to_pass_weighted,
    get_resolution_status,
)

from metrics.monitor import (
    monitor_validation,
    monitor_logs_same_diff,
)

from metrics.report import (
    get_eval_report,
    get_eval_reports_for_logs,
    get_eval_reports_for_dir,
    get_model_eval_summary,
    get_model_report,
)

from versioning.constants import (
    MAP_REPO_TO_VERSION_PATHS,
    MAP_REPO_TO_VERSION_PATTERNS,
)

from versioning.get_versions import (
    get_version,
    map_version_to_task_instances,
    get_versions_from_build,
    get_versions_from_web,
)

from versioning.utils import (
    split_instances,
)