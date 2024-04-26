"""
This module contains Task 1.3 "Search with parallelism".

You need to design a frequency-counting program with parallelism programming.
Your task is to count the frequency of each name in the text.

You are given two files:
- One is the file with a long text.
- The other is a file including a set of names.

The Result:
- The result is like “Harry” 102, “Ron” 54 and so on.
- The result should be saved in a new file.
- Compound words including these names should be counted too.

For example, the word like “Harry's talk ...” should be counted
even if “Harry” is not an independent word.
"""

import os
import multiprocessing
import types
import typing

from datetime import datetime


class Process(multiprocessing.Process):
    """
    Spawn a single process to run a worker/task on.
    """

    def __init__(
        self,
        process_id: int,
        name: str,
        target: types.FunctionType = None,
        args: tuple = None,
        verbose: bool = True
    ):
        super().__init__(name=name, target=target, args=args)
        self.process_id = process_id + multiprocessing.current_process().pid
        self.process_state = ""
        self.name = name
        self.start_time = datetime.now()
        self.target = target
        self.args = args
        self.verbose = verbose

        self.manager = multiprocessing.Manager().dict({"process_state": ""})

    def _process_status(self, state: int = None):
        try:
            process_id = f"Process ID: {self.process_id}"
            end_time = datetime.now()
            elapsed_time = end_time - self.start_time
            process_end_time = end_time.strftime(
                '%H:%M:%S'
            )
            processed_start_time = self.start_time.strftime(
                '%H:%M:%S'
            )
            if state == 1:
                self.process_state = "complete"
                finished_at = f" @ {process_end_time}."

                if self.verbose:
                    s1 = f"PID: {self.process_id} {self.process_state}"
                    s2 = f"{finished_at} [{elapsed_time}] "
                    s3 = f"[{self.name} | {self.manager['result']}]"
                    result = s1 + s2 + s3

                    return result
                return f"PID: {self.process_id} {self.process_state}."

            self.process_state = "spawned"
            process_spawn = self.process_state.capitalize() + " " + process_id
            at_time = f" @ {processed_start_time}."

            if self.verbose:
                return process_spawn + at_time

            return f"PID: {self.process_id} {self.process_state}."

        except Exception as e:
            return f"Unable to evaluate Process ID: {self.process_id}, " + \
                "terminating... " + f"ERROR: {e}."

    def run(self) -> str:
        """
        Execute a task or computation via this process (worker).
        """

        # self.process_state = ""
        result = self.target(*self.args)
        self.manager["end_time"] = datetime.now()
        self._process_status(1)
        self.manager["result"] = result
        self.manager["process_state"] = "complete"

    def __str__(self):
        if self.manager["process_state"] == "complete":
            return self._process_status(1)
        return self._process_status()


class FrequencyCounter:
    """
    This algorihtm is an counting sort which incorporates
    parallelism to dynamically allocate workload more efficiently
    taking advantage of the available CPU cores.
    We use Processes to create subroutines then each routine is executed
    in parallel on each process to reduce time complexity.
    """

    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__name__))
        self.current_directory = current_directory + "\\"
        self.task_directory = self.current_directory + "\\tasks\\Task 1_3\\"
        self.available_workers = multiprocessing.cpu_count()

        self.text = self.get_text()
        self.text_array = self.get_text_by_arraylist()

    def get_stringfile(self, file_name: str) -> str:
        """
        This function gets the ASCII characters from a text file
        and reads it into an array of characters.
        :return: str
        """

        with open(file_name, "r", encoding="utf-8") as file:
            file_string = file.read()
        return file_string

    def get_names(self) -> dict:
        """
        Return a map of names from the task file.
        """

        names_map = {}
        names_file = self.get_stringfile(
            self.task_directory +
            "task1_3_names.txt"
        ).split("\n")

        for string_name in names_file:
            names_map[string_name] = 0

        return names_map

    def get_text(self):
        """
        Returns the text file about the
        Harry Potter and the Deathly Hallows - J.K. Rowling.
        """

        text = self.get_stringfile(
            self.task_directory +
            "task1_3_text.txt"
        )

        return text

    def get_text_by_arraylist(self) -> typing.List[str]:
        """
        Returns an array list of the text.
        This removes all possible trailing whitespaces,
        therefore reducing computation.
        :returns: List[str]
        """

        return self.text.strip().split()

    def get_frequency(self, string_name) -> int:
        """
        Returns the total frequency of a string.
        Predicate:∀string_name∀counter∀row(get_frequency(string_name,counter,row).
        """

        counter = 0
        for row in self.text_array:
            if string_name in row:
                counter += 1
            continue

        return counter


if __name__ == "__main__":
    freq_counter = FrequencyCounter()
    name_map = freq_counter.get_names()
    names = list(name_map.keys())
    result_queue = multiprocessing.Queue()
    processes: typing.DefaultDict[str, Process] = {
        process_id: Process(
            process_id,
            names[process_id],
            target=freq_counter.get_frequency,
            args=(names[process_id], ),
        )
        for process_id in range(len(names))
    }

    # Start and join the processes seperately
    # so we can use parallelism.
    for process in processes.values():
        process.start()
        print(process)

    for process in processes.values():
        process.join()
        print(process)
        result = process.manager["result"]
        name_map[process.name] = process.manager["result"]

    print(
        name_map, f"\n\033[91m{names[-1]} putting himself " +
        "in a J.K Rowling Book :)\033[0m"
    )
