# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from abc import ABC, abstractmethod
import shutil
from pathlib import Path
import tempfile
import shlex
from typing import List, Optional


class NsightTool(ABC):
    def __init__(self, kernel_id: str, installation_path: str, args: str):
        self.kernel_id = kernel_id
        self.installation_path = installation_path
        self.args = shlex.split(args)
        self.target_exe = shutil.which(self.target_exe_name(), path=self.target_exe_dir())
        self.host_exe = shutil.which(self.host_exe_name(), path=self.host_exe_dir())

    @abstractmethod
    def target_exe_name(self) -> str:
        """
        Returns the name of the tool executable
        """

    @abstractmethod
    def target_exe_dir(self) -> Optional[Path]:
        """
        Returns the path to the directory of the tool executable.
        """

    @abstractmethod
    def host_exe_name(self) -> str:
        """
        Returns the name of the tool's host executable
        """

    @abstractmethod
    def host_exe_dir(self, installation_path: str) -> Optional[Path]:
        """
        Returns the path to the directory of the tool's host executable.
        """

    @abstractmethod
    def launch_kernel_cmd(self) -> List[str]:
        """
        Returns the tool command to inject to the kernel launch command.
        """

    @abstractmethod
    def get_start_code(self, **kwargs) -> str:
        """
        Returns the Python code to start the tool (to be executed by the kernel).
        """

    @abstractmethod
    def get_stop_code(self, **kwargs) -> str:
        """
        Returns the Python code to stop the tool (to be executed by the kernel).
        """

    @abstractmethod
    def cleanup(self):
        pass


class NsysProfiler(NsightTool):
    # TODO: DTSP-16323
    # TODO: DTSP-16324
    nsys_target_dir_name = 'target-linux-x64'
    nsys_host_dir_name = 'host-linux-x64'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requested_stats_report_path: Optional[Path] = None

    def target_exe_name(self) -> str:
        return 'nsys'

    def target_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path) / self.nsys_target_dir_name

    def host_exe_name(self) -> str:
        return 'nsys-ui'

    def host_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path) / self.nsys_host_dir_name

    def launch_kernel_cmd(self) -> List[str]:
        return [self.target_exe, 'launch', f'--session={self.kernel_id}'] + self.args

    def get_start_code(self, report_path: str, args: str) -> str:
        report_path = Path(report_path).absolute()
        args = shlex.split(args)
        if '--stats=true' in args or \
           ('--stats' in args and len(args) > args.index('--stats') + 1 and args[args.index('--stats') + 1] == 'true'):
            self.requested_stats_report_path = report_path

        return f"""
subprocess.check_call(
    ['{self.target_exe}', 'start', '--session={self.kernel_id}', '--output={report_path}'] + {args})
"""

    def get_stop_code(self) -> str:
        code = f"""subprocess.check_call(
            ['{self.target_exe}', 'stop', '--session={self.kernel_id}'], stderr=subprocess.PIPE)
"""
        if self.requested_stats_report_path:
            code += f"""
if pathlib.Path('{self.requested_stats_report_path}').exists():
    subprocess.check_call(
        ['{self.target_exe}', 'stats', '{self.requested_stats_report_path}', '--force-export=true'])
"""
        self.requested_stats_report_path = None
        return code

    def cleanup(self):
        pass


class NcuProfiler(NsightTool):
    nvtx_domain = 'JupyterLabNvidiaNsight'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.report_path contains the profiling results during the whole kernel lifecycle.
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.report_path = Path(self.tmp_dir.name) / 'report.ncu-rep'

    def target_exe_name(self) -> str:
        return 'ncu'

    def target_exe_dir(self) -> Optional[Path]:
        if self.installation_path:
            return Path(self.installation_path)

    def host_exe_name(self) -> str:
        return 'ncu-ui'

    def host_exe_dir(self) -> Optional[Path]:
        return self.target_exe_dir()

    def launch_kernel_cmd(self) -> List[str]:
        return [self.target_exe,
                '-o', str(self.report_path), '--nvtx',
                '--nvtx-include', f'regex:{self.nvtx_domain}@/[0-9]+',
                '--nvtx-exclude', f'{self.nvtx_domain}@exclude'] + self.args

    def get_start_code(self) -> str:
        return ''

    def get_stop_code(self, args: str, range_id: str) -> str:
        if not self.report_path.exists():
            return ''
        return f"""
subprocess.check_call(
    ['{self.target_exe}', '-i', '{self.report_path}',
     '--nvtx-include', '{self.nvtx_domain}@{range_id}'] + {shlex.split(args)})
"""

    def cleanup(self):
        self.tmp_dir.cleanup()


tools = {
    'nsys': NsysProfiler,
    'ncu': NcuProfiler
}
