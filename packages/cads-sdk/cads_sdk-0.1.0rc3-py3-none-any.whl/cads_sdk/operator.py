import os
import subprocess

import fsspec
from fsspec.implementations.sftp import SFTPFileSystem
import s3fs
import pyarrow.fs as fs
import concurrent.futures
from urllib.parse import urlparse

from cads_sdk.add_on import get_spark


class SftpFileTransfer:
    def __init__(self, sftp_host, sftp_port, sftp_username, sftp_password):
        """
        Initialize the SFTPFileTransfer class.

        Parameters
        ----------
        sftp_host : str
            The hostname of the SFTP server.
        sftp_port : int
            The port number of the SFTP server.
        sftp_username : str
            The username for the SFTP server.
        sftp_password : str
            The password for the SFTP server.
        """
        from .conf import HADOOP_HOST, HADOOP_PORT

        self.sftp_host = sftp_host
        self.sftp_port = sftp_port
        self.sftp_username = sftp_username
        self.sftp_password = sftp_password

        self.hdfs_host = HADOOP_HOST
        self.hdfs_port = HADOOP_PORT

        self.sftp_url = (
            f"sftp://{sftp_username}:{sftp_password}@{sftp_host}:{sftp_port}"
        )
        self.hdfs_url = f"hdfs://{self.hdfs_host}:{self.hdfs_port}"

        self.sftp_fs = SFTPFileSystem(
            host=self.sftp_host,
            port=self.sftp_port,
            username=self.sftp_username,
            password=self.sftp_password,
        )

        # Set Hadoop classpath
        os.environ["CLASSPATH"] = subprocess.check_output(
            "$HADOOP_HOME/bin/hadoop classpath --glob", shell=True
        ).decode("utf-8")

    def transfer_file(self, source_path, destination_path, chunk_size=1024 * 1024):
        """
        Transfer a file from the source path to the destination path.

        Parameters
        ----------
        source_path : str
            The path of the source file on the SFTP server.
        destination_path : str
            The path of the destination file on HDFS.
        chunk_size : int
            The size of each chunk to read from the source file. Defaults to 1 MB.

        Returns
        -------
        str
            The source path of the transferred file.

        Raises
        ------
        Exception
            If an error occurs during the file transfer.
        """
        try:
            with fsspec.open(self.sftp_url + source_path, "rb") as source_file:
                with fsspec.open(
                    self.hdfs_url + destination_path,
                    "wb",
                    kerb_ticket="/var/run/krb5cc/tkt",
                ) as destination_file:
                    while True:
                        data = source_file.read(chunk_size)
                        if not data:
                            break
                        destination_file.write(data)
        except Exception as err:
            print(err)

    def sync(
        self,
        source_path,
        destination_path,
        chunk_size=1024 * 1024,
        max_workers=1,
    ):
        """
        Synchronize files from the source path to the destination path.

        Parameters
        ----------
        source_path : str
            The path of the source file or directory on the SFTP server.
        destination_path : str
            The path of the destination directory on HDFS.
        chunk_size : int, optional
            The size of each chunk to read from the source file. Defaults to 1 MB.
        max_worker : int, optional
            The maximum number of worker processes to use. Defaults to 1 worker.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs during the synchronization process.

        Examples
        --------
        >>> import cads_sdk as cs
        >>> file_transfer = cs.SFTPFileTransfer(sftp_host, sftp_port, sftp_username, sftp_password)
        >>> file_transfer.sync(source_path="/home/user/a.parquet", destination_path="hdfs:///data/source/files/a.parquet", max_worker=1)
        """
        try:
            file_list = self.list_files(source_path)

            def transfer_file(file):
                destination_file = os.path.join(
                    destination_path, file.replace(source_path + "/", "")
                )
                self.transfer_file(file, destination_file, chunk_size)
                print(f"Successfully synced {file}")

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(transfer_file, file_list)
        except Exception as err:
            print(err)

    def list_files(self, path):
        file_list = []
        for entry in self.sftp_fs.ls(path):
            if self.sftp_fs.isdir(entry):
                file_list.extend(self.list_files(entry))
            else:
                file_list.append(entry)
        return file_list


class MysqlSync:
    def __init__(
        self, mysql_host, mysql_port, mysql_username, mysql_password, mysql_database
    ):
        """
        Initialize the MysqlSync object.

        Parameters
        ----------
        mysql_host : str
            The hostname of the MySQL server.
        mysql_port : int
            The port number of the MySQL server.
        mysql_username : str
            The username for the MySQL server.
        mysql_password : str
            The password for the MySQL server.
        mysql_database : str
            The MySQL database name.
        """
        from .conf import HADOOP_HOST, HADOOP_PORT

        self.mysql_username = mysql_username
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

        self.hdfs_host = HADOOP_HOST
        self.hdfs_port = HADOOP_PORT

        self.mysql_url = f"jdbc:mysql://{mysql_host}:{mysql_port}/{mysql_database}"
        self.hdfs_url = f"hdfs://{self.hdfs_host}:{self.hdfs_port}"

    def sync(self, source_table, destination_path, mode="append"):
        """
        Sync data from a MySQL table to a specified destination in HDFS.

        Parameters
        ----------
        source_table : str
            The source MySQL table name.
        destination_path : str
            The path in HDFS where the data will be written.
        mode : str, optional
            The write mode for the data (default: "append").

        Examples
        --------
        >>> import cads_sdk as cs
        >>> sync_data = cs.MysqlSync(mysql_host, mysql_port, mysql_username, mysql_password, mysql_database)
        >>> sync_data.sync(source_table="example_table", destination_path="hdfs:///data/source/files/a.parquet", mode="append")
        """
        PS = get_spark(driver_memory="1G", num_executors="2", executor_memory="2G")
        df = (
            PS.spark.read.format("jdbc")
            .option("driver", "com.mysql.cj.jdbc.Driver")
            .option("url", self.mysql_url)
            .option("dbtable", source_table)
            .option("user", self.mysql_username)
            .option("password", self.mysql_password)
            .load()
        )

        df.write.mode(mode).parquet(f"{self.hdfs_url}/{destination_path}")


class S3FileTransfer:
    def __init__(self, s3_endpoint_url, s3_key, s3_secret, s3_bucket):
        """
        Initialize the S3FileTransfer object.

        Parameters
        ----------
        s3_endpoint_url : str
            The endpoint URL of the S3 server.
        s3_key : str
            The access key for the S3 server.
        s3_secret : str
            The secret key for the S3 server.
        s3_bucket : str
            The name of the S3 bucket.
        """
        from .conf import HADOOP_HOST, HADOOP_PORT

        self.s3_endpoint_url = s3_endpoint_url
        self.s3_key = s3_key
        self.s3_secret = s3_secret
        self.s3_bucket = s3_bucket

        self.hdfs_host = HADOOP_HOST
        self.hdfs_port = HADOOP_PORT

        self.s3 = s3fs.S3FileSystem(
            anon=False, key=s3_key, secret=s3_secret, endpoint_url=s3_endpoint_url
        )

        self.s3_url = f"s3://{s3_bucket}"
        self.hdfs_url = f"hdfs://{self.hdfs_host}:{self.hdfs_port}"

        self.s3_mapper = self.s3.get_mapper(self.s3_url)
        self.hdfs_mapper = fsspec.get_mapper(
            self.hdfs_url, kerb_ticket="/var/run/krb5cc/tkt"
        )

        # Set Hadoop classpath
        os.environ["CLASSPATH"] = subprocess.check_output(
            "$HADOOP_HOME/bin/hadoop classpath --glob", shell=True
        ).decode("utf-8")

    def transfer_file(self, source_path, destination_path):
        """
        Transfer a file from S3 to HDFS.

        Parameters
        ----------
        source_path : str
            The source path of the file in S3.
        destination_path : str
            The destination path of the file in HDFS.
        """
        try:
            self.hdfs_mapper[destination_path] = self.s3_mapper[source_path]
            print(f"Successfully synced {source_path}")
        except Exception as err:
            print(err)

    def sync(self, source_path, destination_path):
        """
        Sync files or directories from S3 to HDFS.

        Parameters
        ----------
        source_path : str
            The source path in S3.
        destination_path : str
            The destination path in HDFS.


        Examples
        --------
        >>> import cads_sdk as cs
        >>> file_transfer = cs.S3FileTransfer(endpoint_url, key, secret, bucket)
        >>> file_transfer.sync("images", "/data/source/files/images")
        """
        source_full_path = os.path.join(self.s3_url, source_path)

        if self.s3.isfile(source_full_path):
            self.transfer_file(source_path, destination_path)
        elif self.s3.isdir(source_full_path):
            file_list = self.s3.ls(source_full_path)
            for file in file_list:
                self.sync(
                    file.replace(self.s3_bucket + "/", ""),
                    os.path.join(destination_path, file.split("/")[-1]),
                )


class KafkaConsumer:
    def __init__(self, **kwargs):
        """
        Initialize the KafkaConsumer object.

        Parameters
        ----------
        **kwargs : keyword arguments
            Kafka consumer options.
        """
        self.options = kwargs

    def process_stream(
        self,
        destination_path,
        format="parquet",
        output_mode="append",
        checkpoint_location="tmp",
    ):
        """
        Process the Kafka stream and write the results to a specified destination.

        Parameters
        ----------
        destination_path : str
            The path where the processed data will be written.
        format : str, optional
            The format in which the data will be written (default: "parquet").
        output_mode : str, optional
            The output mode for writing data (default: "append").
        checkpoint_location : str, optional
            The location where checkpoint information will be stored (default: "tmp").

        Examples
        --------
        >>> import cads_sdk as cs
        >>> options = {
                "kafka.bootstrap.servers": "localhost:9092",
                "subscribe": "my_topic",
                "startingOffsets": "earliest"
            }
        >>> kafka_consume = cs.KafkaConsumer(**options)
        >>> kafka_consume.process_stream(format='parquet', destination_path='/data/source/files/a.parquet')
        """
        PS = get_spark(driver_memory="1G", num_executors="2", executor_memory="2G")

        df = PS.spark.readStream.format("kafka").options(**self.options).load()
        processed_df = df.selectExpr("CAST(value AS STRING)", "timestamp")

        processed_df.writeStream.outputMode(output_mode).format(format).option(
            "path", destination_path
        ).option("checkpointLocation", checkpoint_location).start()


class ArchiveData:
    def __init__(self, sftp_host, sftp_port, sftp_username, sftp_password):
        """
        Initialize the ArchiveData class.

        Parameters
        ----------
        sftp_host : str
            The hostname of the SFTP server.
        sftp_port : int
            The port number of the SFTP server.
        sftp_username : str
            The username for the SFTP server.
        sftp_password : str
            The password for the SFTP server.
        """
        from .conf import HADOOP_HOST, HADOOP_PORT

        self.sftp_host = sftp_host
        self.sftp_port = sftp_port
        self.sftp_username = sftp_username
        self.sftp_password = sftp_password

        self.hdfs_host = HADOOP_HOST
        self.hdfs_port = HADOOP_PORT

        self.sftp_url = (
            f"sftp://{sftp_username}:{sftp_password}@{sftp_host}:{sftp_port}"
        )
        self.hdfs_url = f"hdfs://{self.hdfs_host}:{self.hdfs_port}"

        self.sftp_fs = SFTPFileSystem(
            host=self.sftp_host,
            port=self.sftp_port,
            username=self.sftp_username,
            password=self.sftp_password,
        )
        self.hdfs_fs = fs.HadoopFileSystem(
            host=HADOOP_HOST,
            port=int(HADOOP_PORT),
            user="silm",
            kerb_ticket="/var/run/krb5cc/tkt",
        )

        self.archive_path = "/home/silm/archive_dir"

        # Set Hadoop classpath
        os.environ["CLASSPATH"] = subprocess.check_output(
            "$HADOOP_HOME/bin/hadoop classpath --glob", shell=True
        ).decode("utf-8")

    def transfer_file_hdfs_to_sftp(
        self, source_path, destination_path, chunk_size=1024 * 1024
    ):
        """Transfer a file from HDFS to SFTP.

        Parameters
        ----------
        source_path : str
            The path of the source file in HDFS.
        destination_path : str
            The path of the destination file in SFTP.
        chunk_size : int, optional
            The size of each data chunk to read from the source file and write to the destination file,
            by default 1024*1024.

        Returns
        -------
        str
            The source path of the transferred file.

        """
        try:
            with fsspec.open(
                self.hdfs_url + source_path,
                "rb",
                kerb_ticket="/var/run/krb5cc/tkt",
            ) as source_file:
                with fsspec.open(
                    self.sftp_url + destination_path, "wb"
                ) as destination_file:
                    while True:
                        data = source_file.read(chunk_size)
                        if not data:
                            break
                        destination_file.write(data)
            return source_path
        except Exception as err:
            print(err)

    def transfer_file_sftp_to_hdfs(
        self, source_path, destination_path, chunk_size=1024 * 1024
    ):
        """Transfer a file from SFTP to HDFS.

        Parameters
        ----------
        source_path : str
            The path of the source file in SFTP.
        destination_path : str
            The path of the destination file in HDFS.
        chunk_size : int, optional
            The size of each data chunk to read from the source file and write to the destination file,
            by default 1024*1024.

        Returns
        -------
        str
            The source path of the transferred file.

        """
        try:
            with fsspec.open(self.sftp_url + source_path, "rb") as source_file:
                with fsspec.open(
                    self.hdfs_url + destination_path,
                    "wb",
                    kerb_ticket="/var/run/krb5cc/tkt",
                ) as destination_file:
                    while True:
                        data = source_file.read(chunk_size)
                        if not data:
                            break
                        destination_file.write(data)
            return source_path
        except Exception as err:
            print(err)

    def archive_table(
        self, table_name, partition_values, chunk_size=1024 * 1024, max_workers=1
    ):
        """
        Archive a table by transferring its data files from HDFS to SFTP.

        Parameters
        ----------
        table_name : str
            The name of the table to archive.
        partition_values : list
            A list of partition values to select specific partitions of the table for archiving.
        chunk_size : int, optional
            The size of each data chunk to transfer, by default 1024*1024.
        max_workers : int, optional
            The maximum number of concurrent workers to use for transferring files, by default 1.

        Returns
        -------
        None

        """
        try:
            PS = get_spark(driver_memory="1G", num_executors="2", executor_memory="2G")
            location = urlparse(
                PS.spark.sql(f"describe formatted {table_name}")
                .filter("col_name=='Location'")
                .collect()[0]
                .data_type
            ).path
            source_path = os.path.join(location, "data")
            file_list = []
            for partition in partition_values:
                file_list += self.hdfs_fs.get_file_info(
                    fs.FileSelector(
                        os.path.join(source_path, partition), recursive=True
                    )
                )

            def transfer_file(file):
                destination_file = os.path.join(
                    self.archive_path,
                    table_name,
                    file.path.replace(source_path + "/", ""),
                )
                self.transfer_file_hdfs_to_sftp(file.path, destination_file, chunk_size)
                print(f"Successfully archived {file.path}")

            def remove_file():
                PS = get_spark(
                    driver_memory="1G", num_executors="2", executor_memory="2G"
                )
                for partition in partition_values:
                    column, value = partition.split("=")
                    PS.spark.sql(f"DELETE FROM {table_name} where {column}='{value}'")
                    os.system(f"hdfs dfs -rm -r {location}/data/{partition}")

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(transfer_file, file_list)

            remove_file()
        except Exception as err:
            print(err)

    def restore_table(
        self,
        table_name,
        partition_values,
        chunk_size=1024 * 1024,
        max_workers=1,
    ):
        """
        Restore a table by transferring its data files from SFTP to HDFS.

        Parameters
        ----------
        table_name : str
            The name of the table to restore.
        partition_values : list
            A list of partition values to select specific partitions of the table for restoration.
        chunk_size : int, optional
            The size of each data chunk to transfer, by default 1024*1024.
        max_workers : int, optional
            The maximum number of concurrent workers to use for transferring files, by default 1.

        Returns
        -------
        None

        """
        try:
            PS = get_spark(driver_memory="1G", num_executors="2", executor_memory="2G")
            source_path = os.path.join(self.archive_path, table_name)
            location = urlparse(
                PS.spark.sql(f"describe formatted {table_name}")
                .filter("col_name=='Location'")
                .collect()[0]
                .data_type
            ).path
            destination_path = os.path.join(location, "data")
            file_list = []
            for partition in partition_values:
                file_list += self.list_files_recursive_sftp(
                    os.path.join(source_path, partition)
                )

            def transfer_file(file):
                destination_file = os.path.join(
                    destination_path, file.replace(source_path + "/", "")
                )
                self.transfer_file_sftp_to_hdfs(file, destination_file, chunk_size)
                print(f"Successfully restored {file}")

            def add_files():
                for partition in partition_values:
                    column, value = partition.split("=")
                    PS.spark.sql(f"""
                            CALL spark_catalog.system.add_files(
                                table => '{table_name}',
                                source_table => '`parquet`.`{location}/data`',
                                partition_filter => map('{column}', '{value}')
                            )
                        """)

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(transfer_file, file_list)

            add_files()
        except Exception as err:
            print(err)

    def list_files_recursive_sftp(self, path):
        """
        Recursively list files in a directory on SFTP.

        Parameters
        ----------
        path : str
            The path of the directory to list files from.

        Returns
        -------
        list
            A list of file paths.

        """
        file_list = []
        for entry in self.sftp_fs.ls(path):
            if self.sftp_fs.isdir(entry):
                file_list.extend(self.list_files_recursive_sftp(entry))
            else:
                file_list.append(entry)
        return file_list

    def archive_file(
        self, path, partition_values, chunk_size=1024 * 1024, max_workers=1
    ):
        """
        Archive a file by transferring it from HDFS to SFTP.

        Parameters
        ----------
        path : str
            The path of the file to archive.
        partition_values : list
            A list of partition values to select specific partitions of the file for archiving.
        chunk_size : int, optional
            The size of each data chunk to transfer, by default 1024*1024.
        max_workers : int, optional
            The maximum number of concurrent workers to use for transferring files, by default 1.

        Returns
        -------
        None

        """
        try:
            file_list = []
            for partition in partition_values:
                file_list += self.hdfs_fs.get_file_info(
                    fs.FileSelector(os.path.join(path, partition), recursive=True)
                )

            def transfer_file(file):
                destination_file = os.path.join(
                    self.archive_path,
                    os.path.basename(path),
                    file.path.replace(path + "/", ""),
                )
                self.transfer_file_hdfs_to_sftp(file.path, destination_file, chunk_size)
                print(f"Successfully archived {file.path}")

            def remove_file():
                for partition in partition_values:
                    os.system(f"hdfs dfs -rm -r {path}/{partition}")

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(transfer_file, file_list)

            remove_file()
        except Exception as err:
            print(err)

    def restore_file(
        self,
        path,
        partition_values,
        chunk_size=1024 * 1024,
        max_workers=1,
    ):
        """
        Restore a file by transferring it from SFTP to HDFS.

        Parameters
        ----------
        path : str
            The path of the file to restore.
        partition_values : list
            A list of partition values to select specific partitions of the file for restoration.
        chunk_size : int, optional
            The size of each data chunk to transfer, by default 1024*1024.
        max_workers : int, optional
            The maximum number of concurrent workers to use for transferring files, by default 1.

        Returns
        -------
        None

        """
        try:
            file_list = []
            for partition in partition_values:
                file_list += self.list_files_recursive_sftp(
                    os.path.join(self.archive_path, os.path.basename(path), partition)
                )

            def transfer_file(file):
                destination_file = os.path.join(
                    path,
                    file.replace(
                        os.path.join(self.archive_path, os.path.basename(path)) + "/",
                        "",
                    ),
                )
                self.transfer_file_sftp_to_hdfs(file, destination_file, chunk_size)
                print(f"Successfully restored {file}")

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(transfer_file, file_list)

        except Exception as err:
            print(err)
