"""
Module for integrating with PeakRDL. This module is not intended to be used directly
refer to the PeakRDL documentation
"""
from typing import TYPE_CHECKING

# depending on whether peakrdl is installed or not you get a slightly different pylint error
# from the following line, therefore two errors have to be suppressed
#pylint: disable=no-name-in-module,import-error
from peakrdl.plugins.exporter import ExporterSubcommandPlugin  # type: ignore[import]
from peakrdl.config import schema  # type: ignore[import]
#pylint: enable=no-name-in-module,import-error

from .exporter import PythonExporter

if TYPE_CHECKING:
    import argparse
    from systemrdl.node import AddrmapNode  # type: ignore


class Exporter(ExporterSubcommandPlugin):
    """
    PeakRDL export class, see PeakRDL for more details
    """
    short_desc = "Generater Python Wrappers"
    long_desc = "Generate Python Wrappers for the Register Model"

    cfg_schema = {
        "user_template_dir": schema.DirectoryPath(),
    }

    def add_exporter_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        """
        Added the arguments to the PeakRDL arguments

        Args:
            arg_group: from PeakRDL

        Returns:

        """
        arg_group.add_argument('--async', action='store_true', dest='is_async',
                               help='define accesses to register model as asynchronous')
        arg_group.add_argument('--skip_test_case_generation', action='store_true',
                               help='skip the generation of the test cases')
        arg_group.add_argument('--suppress_cleanup', action='store_true', dest='suppress_cleanup',
                               help='by default peakrdl_python deletes all existing python .py '
                                    'files found in the directory where the package will be'
                                    ' generated. This is normally useful if the user is '
                                    'generating over the top of an existing package and prevents '
                                    'problems when the strucutre of the register map changes. '
                                    'However, if additional python files are added by the user '
                                    '(not recommended) this cleanup will need to be suppressed '
                                    'and managed by the user')

    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        """
        Perform the export operation

        Args:
            top_node: Top Node from the systemRDL compile
            options: Command line arguments for PeakRDL-Python

        Returns:

        """
        templates = self.cfg['user_template_dir']
        peakrdl_exporter = \
            PythonExporter(user_template_dir=templates)  # type: ignore[no-untyped-call]

        peakrdl_exporter.export(
            top_node,
            options.output,
            options.is_async,
            skip_test_case_generation=options.skip_test_case_generation,
            delete_existing_package_content=not options.suppress_cleanup
        )
