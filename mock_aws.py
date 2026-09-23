import os
import time
from moto.server import ThreadedMotoServer

PORT = int(os.environ.get("MOTO_PORT", "5000"))
server = ThreadedMotoServer(port=PORT)
server.start()
print(f"[mock-aws] moto API on 127.0.0.1:{PORT} (ec2, s3, cloudfront, sts)", flush=True)

while True:
    time.sleep(10)
