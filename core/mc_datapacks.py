#!/usr/bin/env python3

import os
import shutil

# Where your datapacks are stored on disk
DATAPACKS_BASE_PATH = "./datapacks"

DATAPACKS = [
    {
        "path": "mc_buildings",
        "label": "Buildings"
    }
]

class MC_DATAPACKS:

    @staticmethod
    def getAll():
        return DATAPACKS

    @staticmethod
    def _world_datapacks_dir(world_path: str) -> str:
        return os.path.join(world_path, "datapacks")

    @staticmethod
    def checkStatus(world_path: str):
        """
        Returns a list with datapack status (installed: True/False)
        """
        world_dp = MC_DATAPACKS._world_datapacks_dir(world_path)
        status = []

        for dp in DATAPACKS:
            dp_path = os.path.join(world_dp, dp["path"])
            status.append({
                "label": dp["label"],
                "path": dp["path"],
                "installed": os.path.isdir(dp_path)
            })

        return status

    @staticmethod
    def add(world_path: str, index: int):
        """
        Copy datapack into the world
        """
        dp = DATAPACKS[index]

        src = os.path.join(DATAPACKS_BASE_PATH, dp["path"])
        dst = os.path.join(
            MC_DATAPACKS._world_datapacks_dir(world_path),
            dp["path"]
        )

        if not os.path.isdir(src):
            raise FileNotFoundError(f"Source datapack not found: {src}")

        if os.path.exists(dst):
            raise FileExistsError(f"Datapack already installed: {dst}")

        shutil.copytree(src, dst)

    @staticmethod
    def delete(world_path: str, index: int):
        """
        Remove datapack from the world
        """
        dp = DATAPACKS[index]
        dst = os.path.join(
            MC_DATAPACKS._world_datapacks_dir(world_path),
            dp["path"]
        )

        if not os.path.isdir(dst):
            raise FileNotFoundError(f"Datapack not installed: {dst}")

        shutil.rmtree(dst)
