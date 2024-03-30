import ipih

import os
from pih import A
from pih.tools import j, js, n

TEST: bool = False
#
TEST_NAME: str = "test"
STUB_DIRECTORY_NAME: str = "stub"
#
POLIBASE_NAME: str = "Polibase"
ARCHIVE_TYPE: str = A.CT_F_E.ARCHIVE


class MOUNT_POINT:
    POLIBASE: str = "C:"
    NAS: str = "K:"
    POLIBASE2: str = "L:"


class DATABASE_DUMP:
    FILE_NAME: str = "DatabaseDump"
    FILE_EXTENSION: str = "DMP"


class PolibaseDBApi:

    @staticmethod
    def create_dump(file_name: str | None = None, test: bool | None = None) -> None:
        test = TEST if n(test) else test

        local_polibase_database_dump_folder_name: str = j(
            (POLIBASE_NAME, DATABASE_DUMP.FILE_NAME)
        )
        nas_polibase_database_dump_folder_name: str = A.PTH.join(
            POLIBASE_NAME, DATABASE_DUMP.FILE_NAME
        )
        polibase_folder_path: str = A.PTH.join(
            MOUNT_POINT.POLIBASE, "\\", local_polibase_database_dump_folder_name
        )

        dump_file_name_result: str = "IN"

        if test:
            file_name = TEST_NAME
        else:
            if n(file_name):
                file_name = A.D.now_to_string(A.CT_P.DB_DATETIME_FORMAT)

        dump_file_name_result = A.PTH.add_extension(
            dump_file_name_result, DATABASE_DUMP.FILE_EXTENSION
        )
        file_database_dump_name_out: str = A.PTH.add_extension(
            file_name, DATABASE_DUMP.FILE_EXTENSION
        )
        if test:
            polibase_folder_path_src: str = polibase_folder_path
            polibase_folder_path = A.PTH.for_windows(
                A.PTH.join(polibase_folder_path, TEST_NAME)
            )
            os.system(
                js(
                    (
                        "robocopy",
                        A.PTH.join(polibase_folder_path_src, STUB_DIRECTORY_NAME),
                        polibase_folder_path,
                        file_database_dump_name_out,
                    )
                )
            )
        polibase2_folder_path: str = A.PTH.for_windows(
            A.PTH.join(A.CT_H.POLIBASE2.NAME, local_polibase_database_dump_folder_name)
        )

        nas_folder_path: str = A.PTH.for_windows(
            A.PTH.join(
                A.CT_H.NAS.NAME, "backups", nas_polibase_database_dump_folder_name
            )
        )

        archiver_program_path: str = 'C:/"Program Files"/7-Zip/7z'

        file_out_name = A.PTH.add_extension(file_name, ARCHIVE_TYPE)

        nas_create_connection_command = js(
            (
                "net",
                "use",
                MOUNT_POINT.NAS,
                nas_folder_path,
                j(("/user:", A.D_V_E.value("NAS_USER_LOGIN"))),
                A.D_V_E.value("NAS_USER_PASSWORD"),
            )
        )
        polibase2_create_connection_command = js(
            (
                "net",
                "use",
                MOUNT_POINT.POLIBASE2,
                polibase2_folder_path,
            )
        )
        nas_copy_command = js(
            ("robocopy", polibase_folder_path, MOUNT_POINT.NAS, file_out_name, "/J")
        )
        polibase2_copy_command = js(
            (
                "robocopy",
                polibase_folder_path,
                MOUNT_POINT.POLIBASE2,
                file_database_dump_name_out,
                "/J",
            )
        )
        os.chdir(polibase_folder_path)
        # step 1
        A.E.backup_notify_about_polibase_creation_db_dumb_start(not test)
        if not test:
            os.system(
                j(
                    (
                        "exp userid=POLIBASE/POLIBASE owner=POLIBASE file=",
                        file_database_dump_name_out,
                        " ",
                        "parfile=backpar.txt",
                    )
                )
            )
        A.E.backup_notify_about_polibase_creation_db_dumb_complete(
            os.path.getsize(
                A.PTH.join(polibase_folder_path, file_database_dump_name_out)
            ),
            not test,
        )

        # step 2: connect net location with credentials
        os.system(nas_create_connection_command)
        os.system(polibase2_create_connection_command)

        # step 3
        A.E.backup_notify_about_polibase_creation_archived_db_dumb_start()
        os.system(
            js(
                (
                    archiver_program_path,
                    j(("a -t", ARCHIVE_TYPE)),
                    file_out_name,
                    file_database_dump_name_out,
                )
            )
        )

        A.E.backup_notify_about_polibase_creation_archived_db_dumb_complete(
            os.path.getsize(A.PTH.join(polibase_folder_path, file_out_name)), not test
        )

        # step 4
        A.E.backup_notify_about_polibase_coping_archived_db_dumb_start(
            A.CT_H.NAS.ALIAS.upper()
        )
        os.system(nas_copy_command)
        A.E.backup_notify_about_polibase_coping_archived_db_dumb_complete(
            A.CT_H.NAS.ALIAS.upper()
        )

        # step 5
        A.E.backup_notify_about_polibase_coping_db_dumb_start(
            A.CT_H.POLIBASE2.ALIAS.upper()
        )
        os.system(polibase2_copy_command)
        A.E.backup_notify_about_polibase_coping_db_dumb_complete(
            A.CT_H.POLIBASE2.ALIAS.upper()
        )

        # step 6
        polibase2_previous_file_delete_command: str = js(
            (
                "del",
                A.PTH.for_windows(
                    A.PTH.join(MOUNT_POINT.POLIBASE2, "\\", dump_file_name_result)
                ),
            )
        )
        polibase_file_rename_command: str = js(
            (
                "ren",
                A.PTH.for_windows(
                    A.PTH.join(MOUNT_POINT.POLIBASE2, "\\", file_database_dump_name_out)
                ),
                dump_file_name_result,
            )
        )

        os.system(polibase2_previous_file_delete_command)
        os.system(polibase_file_rename_command)

        # step 7: disconnect net location with credentials
        os.system(js(("net use", MOUNT_POINT.NAS, "/delete /y")))
        os.system(js(("net use", MOUNT_POINT.POLIBASE2, "/delete /y")))

        # step 8
        os.system(js(("del", file_database_dump_name_out)))
        os.system(js(("del", file_out_name)))
