AVAILABLE = 0
BUSY = 1
BLOCKED = 2

DECLINED = -1
ACCEPTED = -2

TIME_DELTA = 0.01
DECLINED_REQUESTS_COUNT = 0
PROCESSED_REQUEST_COUNT = 0
QUEUE_CAPACITY = 3

processed_requests = dict()
declined_requests = dict()
input_requests = dict()

GLOBAL_TIME = 0.
