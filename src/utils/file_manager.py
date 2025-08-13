import json
import csv
from loguru import logger


class FileManager:
    def __init__(self, filename: str, csv_header=None):
        self.filename = filename
        self._split_file = filename.split(".")
        self._split_length = len(self._split_file)
        self._file_type = self._split_file[self._split_length - 1].strip()
        self._supported_modes = {"r", "w", "a"}
        self._accepted_file_types = {"txt", "csv", "json"}
        self._is_supported = self._file_type in self._accepted_file_types
        self.csv_header = csv_header

    def _read(self) -> list:
        try:
            with open(self.filename, "r") as file:
                match self._file_type:
                    case "txt":
                        data = file.read().splitlines()
                    case "csv":
                        reader = csv.reader(file)
                        for row in reader:
                            data.append(row)
                    case "json":
                        data = json.load(file)
                    case _:
                        data = []
            return data
        except Exception as e:
            logger.error(f"Error reading from file {self.filename}: {str(e)}")
            return []

    def _write(self, data: list | dict) -> bool:
        try:
            with open(self.filename, "w", newline="") as file:
                match self._file_type:
                    case "txt":
                        for line in data:
                            file.write(line + "\n")
                    case "csv":
                        writer = csv.writer(
                            file,
                        )
                        if self.csv_header:
                            writer.writerow(self.csv_header)
                        for row in data:
                            writer.writerow(row)
                    case "json":
                        json.dump(data, file, indent=4)
                    case _:
                        pass
            return True
        except Exception as e:
            logger.error(f"Error writing to file {self.filename}: {str(e)}")
            return False

    def _append(self, data: list | dict) -> bool:
        try:
            with open(self.filename, "a", newline="") as file:
                match self._file_type:
                    case "txt":
                        for line in data:
                            file.write(line + "\n")
                    case "csv":
                        writer = csv.writer(file)
                        writer.writerows(data)
                    case "json":
                        json.dump(data, file, indent=4)
                    case _:
                        pass
            return True
        except Exception as e:
            logger.error(f"Error writing to file {self.filename}: {str(e)}")
            return False

    def open_file(
        self,
        mode: str = "r",
        data: list | dict | None = None,
    ) -> list | bool:
        operation_supported = mode in self._supported_modes and self._is_supported
        if not operation_supported:
            logger.warning(
                f"Operation for {self.filename} is not supported: unsupported mode or file type"
            )
            return []
        else:
            match mode:
                case "r":
                    logger.info(f"Reading from {self.filename}")
                    res = self._read()
                case "w":
                    logger.info(f"Writing to {self.filename} - Full Write mode")
                    if data:
                        res = self._write(data)
                    else:
                        logger.warning("No data passed to write")
                        res = False
                case "a":
                    logger.info(f"Writing to {self.filename} - Append mode")
                    if data:
                        res = self._append(data)
                    else:
                        logger.warning("No data passed to append")
                        res = False
            return res
