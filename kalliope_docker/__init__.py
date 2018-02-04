from .core import (generate_dockerfile, build_shell_command,
                   execute_shell_command, get_git_repository_name_from_url)
from .pipelines import (resources_pipeline, profile_pipeline,
                        standard_dependencies_pipeline)
