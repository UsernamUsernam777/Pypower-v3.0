"""Excel workbook editing helpers.

This module provides utilities for updating cell values in an existing
Excel workbook using the openpyxl library.

Example:
    from pypower.Analysis import edit_cells

    edit_cells(
        file_path="report.xlsx",
        sheet_name="Summary",
        cell_names=["B2", "C2"],
        values=[100, "Complete"],
    )

Dependencies:
    openpyxl
"""

import openpyxl


def edit_cells(file_path, sheet_name, cell_names, values):
    """Update cells in a worksheet and save the workbook.

    Args:
        file_path (str): Path to the Excel workbook to edit.
        sheet_name (str): Name of the worksheet to modify.
        cell_names (Sequence[str]): Iterable of Excel cell references
            (for example, ["A1", "B2", "C3"]).
        values (Sequence[Any]): Iterable of values to write into the
            corresponding cells.

    Raises:
        KeyError: If the requested worksheet does not exist.
        ValueError: If the workbook cannot be loaded or saved.

    Notes:
        The function pairs cell_names and values positionally using zip.
        Extra cells or values beyond the shortest sequence are ignored.
    """
    wb = openpyxl.load_workbook(file_path)
    for c, v in zip(cell_names, values):
        wb[sheet_name][c] = v
    wb.save(file_path)
    wb.close()
