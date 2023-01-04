REFERERS = {
    "network-traffic": {
        "src_ref": ["value"],
        "dst_ref": ["value"]
    },
    "x-ibm-finding": {
        "src_ip_ref": ["value"],
        "dst_ip_ref": ["value"]
    },
    "x-oca-event": {
        "network_ref": ["src_ref.value", "dst_ref.value"],
        # "network_ref": ["src_ref.value"],
        "file_ref": ["name"],
        "process_ref": ["pid"],
        "parent_process_ref": ["pid"],
        "user_ref": ["user_id"],
        "ip_refs": ["value"],
        "host_ref": ["x-oca-asset.hostname"]
    },
    "x-oca-asset": {
        "ip_refs": ["value"]
    },
    "process": {
        "binary_ref": ["name"],
        "parent_ref": ["binary_ref.name"],
        "creator_user_ref": ["user_id"]
    },
    "file": {
        "parent_directory_ref": ["path"]
    }
}

SUBSTITUTES = [{
        "name": "filename",
        "paths": [
            "payload.process.program.filename",
            "payload.process.program.fsName",
            "payload.data.filename",
            "payload.data.fsName",
            "payload.data.targetProcess.program.filename",
            "payload.data.childProcess.program.filename",
            "payload.data.targetProcess.program.fsName",
            "payload.data.childProcess.program.fsName",
            "payload.data.allocatorProc.program.filename",
            "payload.data.allocatorProc.program.fsName",
            "payload.data.accessorProcess.program.filename",
            "payload.data.accessorProcess.program.fsName",
            "payload.data.engineProcess.program.filename",
            "payload.data.engineProcess.program.fsName",
            "payload.data.serviceProcess.program.filename",
            "payload.data.serviceProcess.program.fsName"
        ]
    },
    {
        "name": "ip",
        "paths": [
            "payload.data.remoteAddr",
            "payload.data.localAddr"
        ]
    },
    {
        "name": "md5",
        "paths": [
            "payload.process.program.md5",
            "payload.data.md5",
            "payload.data.childProcess.program.md5",
            "payload.data.targetProcess.program.md5",
            "payload.data.allocatorProc.program.md5",
            "payload.data.engineProcess.program.md5",
            "payload.data.serviceProcess.program.md5"
        ]
    },
    {
        "name": "path",
        "paths": [
            "payload.process.program.path",
            "payload.data.childProcess.program.path",
            "payload.data.targetProcess.program.path",
            "payload.data.allocatorProc.program.path",
            "payload.data.file",
            "payload.data.path",
            "payload.data.rootObject",
            "payload.data.engineProcess.program.path",
            "payload.data.serviceProcess.program.path"
        ]
    },
    {
        "name": "sha1",
        "paths": [
            "payload.process.program.sha1",
            "payload.data.sha1",
            "payload.data.childProcess.program.sha1",
            "payload.data.targetProcess.program.sha1",
            "payload.data.allocatorProc.program.sha1",
            "payload.data.engineProcess.program.sha1",
            "payload.data.serviceProcess.program.sha1"
        ]
    },
    {
        "name": "sha256",
        "paths": [
            "payload.process.program.sha256",
            "payload.data.sha256",
            "payload.data.childProcess.program.sha256",
            "payload.data.targetProcess.program.sha256",
            "payload.data.allocatorProc.program.sha256",
            "payload.data.engineProcess.program.sha256",
            "payload.data.serviceProcess.program.sha256"
        ]
    }
]

