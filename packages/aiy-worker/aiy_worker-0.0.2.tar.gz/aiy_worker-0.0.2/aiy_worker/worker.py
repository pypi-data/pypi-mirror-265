
from enum import Enum
from typing import Callable
import requests
from .ws_client import GraphQLClient
from .types import WsData, Task, PayloadError
from .utils import encode_image, png2webp, png2avif, make_thumbnail, check_pngquant_bin
import logging

logger = logging.getLogger(__name__)

sub_task_query = """
  subscription ($token: String!) {
    subscribeTasks(token: $token) {
        id
        text2Image {
            prompt
            negativePrompt
            seed
        }
    }
  }
"""


def wait_shutdown(fn: Callable):
    import signal
    import sys

    def signal_handler(sig, frame):
        logger.info('You pressed Ctrl+C!')
        fn()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    logger.info('Press Ctrl+C')
    try:
        while True:
            import time
            time.sleep(1)
    except:
        pass

class TaskState:
    RECEIVED = "RECEIVED"
    GENERATING = "GENERATING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"

class ImageKind:
    PNG = 1
    WEBP = 2
    AVIF = 3

class AiyWorker:

    def __init__(self, token: str, server: str = "http://localhost:8080", ws_server="ws://localhost:8080", image_kind=ImageKind.WEBP) -> None:
        check_pngquant_bin()
        self.token = token
        self.query_url = f'{server}/graphql'
        self.ws_url = f'{ws_server}/subscriptions'
        self.image_kind = image_kind
        # TODO 注册 GPU 数据

    def __on_task(self, _id, data):
        ws_data = WsData(data)
        if ws_data.payload:
            errors = ws_data.payload.errors
            if errors:
                raise Exception(errors[0].message)
            task = ws_data.payload.task
            # received state
            self.__submit_task_result(task, TaskState.RECEIVED)
            def _set_progress(progress: float):
                self.set_progress(task, progress)
            try:
                logger.info("Start to generate image")
                image_path = self.on_task(task, _set_progress)
                logger.info("Generate image successfully: %s", image_path)
                # 制作缩略图
                thumbnail = make_thumbnail(image_path)
                # 转换图片格式
                suffix = 'png'
                if self.image_kind == ImageKind.WEBP:
                    # 将 png 转化为 webp
                    suffix = 'webp'
                    image_path = png2webp(image_path, quality=50) # 50 肉眼基本看不出差别
                elif self.image_kind == ImageKind.AVIF:
                    suffix = 'avif'
                    image_path = png2avif(image_path, quality=50)
                    logger.info("convert png to avif format successfully: %s", image_path)
                result = encode_image(image_path)
                
                logger.info("Image encoded to base64 successfully")
                self.__submit_task_result(task, TaskState.SUCCESSFUL, None, result, suffix, thumbnail)
            except Exception as e:
                logger.info(e)
                self.__submit_task_result(task, TaskState.FAILED)

    def __submit_task_result(self, task: Task, state: TaskState, progress: float = None,
                             result: str = None, suffix: str = None, thumbnail_base64: str=None):
        logger.info(f"set worker's state to {state}")
        query = """
mutation ($task_id: Int!, $worker_token: String!, $progress: Float, $result: String, $suffix: String, $thumbnail_base64: String) {{
    worker_service {{
        submitTaskResult(
            taskId: $task_id
            workerToken: $worker_token
            state: {state}
            progress: $progress,
            result: {{
                kind: IMAGE,
                bytesBase64: $result
                suffix: $suffix
                thumbnailBase64: $thumbnail_base64
            }}
        )
    }}
}}
        """.format(state=state)
        variables = {
            'task_id': task.id,
            'worker_token': self.token,
            'progress': progress,
            'result': result,
            'suffix': suffix,
            'thumbnail_base64': thumbnail_base64
        }
        headers = {'Authorization': 'Bearer xxxx'}
        response = requests.post(self.query_url,
                                 json={
                                     "query": query, "variables": variables, "headers": headers}
                                 )

        _r = response.json()
        if _r :
            data = _r['data']
            if data and data.get('worker_service'):
                r = data.get('worker_service').get('submitTaskResult')
                if r == 'OK':
                    return
            errors = [PayloadError(i) for i in _r.get('errors', [])]
            if len(errors) > 0:
                logger.info('Error: %s' % errors[0].message)

    def on_task(self, task: Task, progress_callback: Callable[[float], None]):
        """ 接收到任务，并进行处理，返回处理结果（生成的图片的路径） """
        raise NotImplementedError

    def set_progress(self, task: Task, progress: float):
        """ 设置进度条 """
        logger.info(f'progress: {progress}')
        self.__submit_task_result(task, TaskState.GENERATING, progress)

    def run(self):
        logger.info("Starting...")
        """ 运行任务 """
        # 发起 ws 连接
        with GraphQLClient(self.ws_url) as client:
            logger.info("Create client success")
            self.client = client
            self.sub_id = client.subscribe(sub_task_query, variables={
                                           "token": self.token}, callback=self.__on_task)

            def on_exit():
                logger.info("Stop client...")
                client.stop_subscribe(self.sub_id)
                logger.info("Stop client success")
            wait_shutdown(on_exit)
