import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import * as XLSX from "xlsx";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import { useTable, useSortBy, usePagination } from "react-table";
import { FaChevronDown } from "react-icons/fa";
import { ToastContainer } from "react-toastify";

pdfMake.vfs = pdfFonts.pdfMake.vfs;

const AttendanceTable = ({ records }) => {
  const [filteredData, setFilteredData] = useState(records);
  const [loading, setLoading] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  useEffect(() => {
    setFilteredData(records);
  }, [records]);

  const handleExportToPdf = () => {
    const docDefinition = {
      content: [
        { text: "Employee Attendance", style: "header" },
        {
          table: {
            headerRows: 1,
            widths: ["*", "*", "*", "*", "*", "*"],
            body: [
              [
                { text: "Employee ID", style: "tableHeader" },
                { text: "Employee Name", style: "tableHeader" },
                { text: "Date", style: "tableHeader" },
                { text: "Log Time", style: "tableHeader" },
              ],
            ],
          },
          layout: {
            fillColor: (rowIndex) => {
              if (filteredData[rowIndex - 1]?.status === "present")
                return "#d4edda";
              if (filteredData[rowIndex - 1]?.status === "late")
                return "#aaaaaa";
              if (
                filteredData[rowIndex - 1]?.status === "leave" ||
                filteredData[rowIndex - 1]?.status === "sick_leave" ||
                filteredData[rowIndex - 1]?.status === "casual_leave"
              )
                return "#fff3cd";
              if (filteredData[rowIndex - 1]?.status === "absent")
                return "#f8d7da";
              return null;
            },
          },
        },
      ],
      styles: {
        header: {
          fontSize: 16,
          bold: true,
          margin: [0, 0, 0, 10],
        },
        tableHeader: {
          bold: true,
          fontSize: 10,
          color: "black",
          fillColor: "#4CAF50",
          alignment: "center",
        },
        tableData: {
          fontSize: 8,
          margin: [0, 2, 0, 2],
          alignment: "center",
        },
      },
      pageMargins: [40, 60, 40, 40],
    };

    pdfMake.createPdf(docDefinition).download("attendance.pdf");
  };

  const handleExportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(filteredData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Attendance");
    XLSX.writeFile(workbook, "attendance.xlsx");
  };

  const handleExportSelection = (format) => {
    if (format === "excel") {
      handleExportToExcel();
    } else if (format === "pdf") {
      handleExportToPdf();
    }
    setIsDropdownOpen(false);
  };

  const columns = useMemo(
    () => [
      { Header: "Employee ID", accessor: "employee_id" },
      { Header: "Employee Name", accessor: "employee_name" },
      { Header: "Date", accessor: "date" },
      { Header: "Log Time", accessor: "log_time" },
      {
        Header: "Actions",
        Cell: ({ row }) => (
          <button
            onClick={() => {}}
            className="bg-blue-500 text-white py-1 px-2 rounded-md"
          >
            Edit
          </button>
        ),
      },
    ],
    []
  );

  const data = useMemo(() => filteredData, [filteredData]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    canPreviousPage,
    canNextPage,
    pageOptions,
    gotoPage,
    previousPage,
    nextPage,
    setPageSize: setTablePageSize,
    state: { pageIndex },
  } = useTable(
    {
      columns,
      data,
      initialState: {
        pageSize: 10,
        sortBy: [
          {
            id: "date",
            desc: true,
          },
        ],
      },
    },
    useSortBy,
    usePagination
  );

  return (
    <div className="max-w-7xl mx-auto p-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="flex items-center space-x-2 bg-caribbean-current text-white py-2 px-3 rounded-md"
          >
            Export <FaChevronDown />
          </button>
          {isDropdownOpen && (
            <div className="absolute bg-white border shadow-lg mt-2 rounded-md">
              <button
                onClick={() => handleExportSelection("excel")}
                className="block px-4 py-2 text-black hover:bg-gray-100"
              >
                Export to Excel
              </button>
              <button
                onClick={() => handleExportSelection("pdf")}
                className="block px-4 py-2 text-black hover:bg-gray-100"
              >
                Export to PDF
              </button>
            </div>
          )}
        </div>
      </div>
      <table
        {...getTableProps()}
        className="min-w-full divide-y divide-gray-200"
      >
        <thead className="bg-gray-100">
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {column.render("Header")}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? " 🔽"
                        : " 🔼"
                      : ""}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody
          {...getTableBodyProps()}
          className="bg-white divide-y divide-gray-200"
        >
          {page.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td
                    {...cell.getCellProps()}
                    className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                  >
                    {cell.render("Cell")}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
      <div className="flex justify-between items-center mt-4">
        <button
          onClick={() => previousPage()}
          disabled={!canPreviousPage}
          className="bg-caribbean-current text-white py-2 px-4 rounded-md"
        >
          Previous
        </button>
        <button
          onClick={() => nextPage()}
          disabled={!canNextPage}
          className="bg-caribbean-current text-white py-2 px-4 rounded-md"
        >
          Next
        </button>
        <span>
          Page {pageIndex + 1} of {pageOptions.length}
        </span>
      </div>
      <ToastContainer />
    </div>
  );
};

export default AttendanceTable;
