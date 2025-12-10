# Copyright (C) 2024 by Badhacker98@Github
# Owner https://t.me/ll_BAD_MUNDA_ll

import socket
import time

import heroku3
from pyrogram import filters

import config
from BADMUSIC.core.mongo import pymongodb
from .logging import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def dbb():
    global db, clonedb
    db = {}
    clonedb = {}
    LOGGER(__name__).info("Database Initialized.")


def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID

    # ✅ MOST IMPORTANT FIX
    # Mongo abhi init nahi hua → crash se bachao
    if pymongodb is None:
        for user_id in OWNER:
            SUDOERS.add(user_id)
        LOGGER(__name__).warning(
            "MongoDB not initialized yet. Using OWNER_ID as sudoers."
        )
        return

    sudoersdb = pymongodb.sudoers
    sudoers_data = sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers_data else sudoers_data.get("sudoers", [])

    for user_id in OWNER:
        SUDOERS.add(user_id)
        if user_id not in sudoers:
            sudoers.append(user_id)

    sudoersdb.update_one(
        {"sudo": "sudo"},
        {"$set": {"sudoers": sudoers}},
        upsert=True,
    )

    for user_id in sudoers:
        SUDOERS.add(user_id)

    LOGGER(__name__).info("Sudoers Loaded.")


def heroku():
    global HAPP

    # ✅ function call fix
    if not is_heroku():
        return

    if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
        try:
            Heroku = heroku3.from_key(config.HEROKU_API_KEY)
            HAPP = Heroku.app(config.HEROKU_APP_NAME)
            LOGGER(__name__).info("Heroku App Configured")
        except Exception as e:
            LOGGER(__name__).warning(
                f"Heroku init failed: {e}"
            )
