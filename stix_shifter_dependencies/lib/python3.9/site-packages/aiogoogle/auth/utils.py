__all__ = ["create_secret"]

import hashlib
import os
import datetime
import sys

from ..utils import _parse_isoformat


def create_secret(bytes_length=1024):  # pragma: no cover
    # return hashlib.sha256(os.urandom(bytes_length << 3)).hexdigest()
    return hashlib.sha256(os.urandom(bytes_length)).hexdigest()


def _get_expires_at(expires_in):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    # account for clock skew
    expires_at -= datetime.timedelta(seconds=120)
    return expires_at.isoformat()


def _is_expired(expires_at):
    # Refresh in case there's no expires_at present
    if expires_at is None:
        return True
    if not isinstance(expires_at, datetime.datetime):
        # datetime.fromisoformat is 3.7+
        if sys.version_info[1] <= 6:
            expires_at = _parse_isoformat(expires_at)
        else:
            expires_at = datetime.datetime.fromisoformat(expires_at)
    if datetime.datetime.utcnow() >= expires_at:
        return True
    else:
        return False
