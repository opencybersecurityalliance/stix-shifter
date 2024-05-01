from typing import Optional


class Timeouts:
    """Timeouts class wrapper.

    Arguments:
        * sock_connect(float): time for establish connection to server
        * sock_read(float): time until get first read
        * pool_acquire(float): time until get connection from
          connection's pool
        * request_timeout(float): time until complete request.
    """

    def __init__(
        self,
        sock_connect: Optional[float] = 5,
        sock_read: Optional[float] = 30,
        pool_acquire: Optional[float] = None,
        request_timeout: Optional[float] = 60,
    ) -> None:
        self.sock_connect = sock_connect
        self.sock_read = sock_read
        self.pool_acquire = pool_acquire
        self.request_timeout = request_timeout
