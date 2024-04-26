"""
Task 1.4: (25%) cheapest train tickets

The requirements of the task are as follows:
1. Import the csv file.
2. Input two station names for departure and destination.
3. Return the cheapest cost of the two stations and all the station names on
the route.

"""

import os
import csv
import typing
# from datetime import datetime


def read_csv(file_name) -> typing.List[typing.List]:
    """
    Similarly to getting a text file,
    we return comma seperated values data.
    """

    csv_data = []
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            csv_data.append(row)
    return csv_data


class DataFrame:
    """
    A heterogeneous tabular data structure with rows and columns.
    Similarly to a Pandas DataFrame except coded in a python environment
    to prevent additional use of external libraries.
    """

    def __init__(self, data: typing.List = None, columns: typing.List = None):
        self.columns = columns

        # Fill empty columns
        for row in data:
            if len(row) != len(columns):
                row.extend("" for _ in range(len(columns) - len(row)))

        self.data = data

    def __str__(self):
        """
        A visualised display of our Data Frame.
        Useful for interpreting data.
        """

        df_len = 50

        index_column = "Index"
        index_width = len(index_column) + 1
        index_values = [str(idx) for idx in range(len(self.data[:df_len]))]

        col_widths = [
            max(len(col), max(len(str(row[i])) for row in self.data[:df_len]))
            for i, col in enumerate(self.columns)
        ]
        idx_width = max(index_width, max(len(idx) for idx in index_values))
        idx_values = [idx.ljust(idx_width) for idx in index_values]

        headers = "\n\n" + index_column.ljust(idx_width) + " | " + " | ".join(
            col.ljust(width) for col, width in zip(self.columns, col_widths)
        )
        separator = "-" * (
            idx_width + 3 + sum(col_widths) + (len(self.columns) - 1) * 3
        )

        rows = [
            idx_values[i] + " | " +
            " | ".join(
                str(row[i]).ljust(width) for i, width in enumerate(col_widths)
            )
            for i, row in enumerate(self.data[:df_len])
        ]

        hidden_rows = len(self.data)-df_len
        str_hidden_rows = f"\n{abs(hidden_rows)} rows have been hidden."

        if len(self.data) > df_len:
            return "\n".join(
                [headers, separator] +
                rows
            ) + str_hidden_rows

        return "\n".join(
            [headers, separator] +
            rows
        )

    def add_row(self, row_data: typing.List | typing.Tuple):
        """
        Insert a row to the existing Data Frame.
        """

        return self.data.append(row_data)

    def add_row_data(self, index: int, data: typing.List):
        """
        Add data to an existing row in a Data Frame.
        """

        if len(data) != len(self.columns):
            raise ValueError("Data row is out of range.")

        if index < 0 or index >= len(self.data):
            raise IndexError("This index does not exist.")

        self.data[index] = data
        return self

    def remove_row(
        self,
        index: int = None
    ):
        """
        Remove a row from the existing Data Frame.
        """

        self.data.remove(self.data[index])
        return self

    def add_column(self, columns: typing.List[str]):
        """
        Insert a column to an existing DataFrame.
        """

        if len(columns) == 1:
            return DataFrame(self.data, self.columns + columns)

        return DataFrame(self.data, self.columns + columns)

    def remove_column(self, columns: typing.List[str]) -> 'DataFrame':
        """
        Remove column(s) and corresponding data
        """
        indices_to_remove = [self.columns.index(col) for col in columns]
        self.columns = [col for col in self.columns if col not in columns]
        self.data = [
            [row[i] for i in range(len(row)) if i not in indices_to_remove]
            for row in self.data
        ]
        return self

    def get_columns(self, columns: typing.List):
        """
        Get a column and row data for it from a DataFrame.
        """

        for col in columns:
            if col not in self.columns:
                raise ValueError(f"Column '{col}' not found.")

        data_columns = [
            [row[self.columns.index(col)] for row in self.data]
            for col in columns
        ]

        transposed_data = list(zip(*data_columns))
        return DataFrame(transposed_data, columns)

    def get_row(self, index):
        """
        Get row data via index from a DataFrame.
        """

        return self.data[index]

    def head(self, n: int):
        """
        Display the 'n' number of rows from the top
        of the Data Frame.
        """

        return DataFrame(self.data[0:n], self.columns)

    def tail(self, n: int):
        """
        Display the 'n' number of rows from the bottom
        of the Data Frame.
        """

        return DataFrame(self.data[-1-n::], self.columns)

    def find(self, value: typing.Any, column: str):
        """
        Find a all rows of value in a Data Frame.
        """

        col_data = []
        for row in self.data:
            if value in row[self.columns.index(column)]:
                col_data.append(row)

            else:
                raise ValueError(
                    f"Value '{value}' not found in column '{column}'."
                )

        self.data = col_data
        return self


class Node:
    """
    A unique node to be used within the Dijkstra Algorithm.
    """

    def __init__(self, name, to_relative, price):
        self.name = name
        self.to_relative = to_relative
        self.price = price


class CheapestTrainTickets:
    """
    In a train ticket search system, users require the
    cheapest train tickets between their departure and destination.

    This object contains functions and attributes about their journey,
    price, start or end points, and more.
    """

    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__name__))
        self.current_directory = current_directory + "\\"
        self.task_directory = self.current_directory + "\\tasks\\Task 1_4\\"

    def __str__(self):
        return ""

    def get_nodes(self):
        """
        Convert all data points to nodes
        """

        csv_file = read_csv(
            self.task_directory +
            "task1_4_railway_network.csv"
        )

        return [
            Node(
                name=node[0], to_relative=node[1], price=node[2]
            ) for node in csv_file
        ]

    def get_visitied_nodes(self):
        return

    def get_unvisited_nodes(self):
        return

    def get_route_stations(self, departure: str, destination: str):
        """
        Input two station names for departure and destination
        to return all stations for that particular route,
        if available.
        :returns: typing.DefaultDict[
            journey: [str, ...],
            price: [int, ...]
        ]
        """

        visited_nodes = []
        unvisited_nodes = self.get_nodes()


if __name__ == '__main__':
    ctt = CheapestTrainTickets()
    # user_input_departure = input("Enter your Departure Location: ")
    # user_input_destination = input("Enter your Destination Location: ")

    user_input_departure = "PENZANCE"
    user_input_destination = "BRISTOL TEMPLE MEADS"
    # ctt.get_route_stations(
    #     departure=user_input_departure,
    #     destination=user_input_destination
    # )
