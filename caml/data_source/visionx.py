from . import DataSource
from typing import Tuple, Optional, List
from clearml import Task as _Task
import getpass
import requests


class VisionX(DataSource):
    PARAM_NAME = 'Token/VisionX'
    BASE_URL = ''

    def __init__(
        self,
        project_id: int,
    ):
        super(VisionX, self).__init__()
        self.project_id = project_id

        task = _Task.current_task()
        token = task.get_parameter(VisionX.PARAM_NAME)

        if not token:
            token = self.get_token()
            _Task.current_task().set_parameter(VisionX.PARAM_NAME, token)

        self.token = token

    def samples(self) -> Tuple[list, Optional[list]]:
        _samples = []
        task_ids = self.get_task_ids(self.project_id)

        for task_id in task_ids:
            anno_file = self.get_annotations(task_id)
            task_samples = self.get_samples(anno_file)
            _samples.extend(task_samples)

        return _samples

    def create_dataset(
        self,
        samples: list,
        targets: list = None,
    ) -> str:
        pass

    def get_token(self) -> str:
        user = getpass.getuser()
        password = getpass.getpass()
        client_id = 'dp-service'
        grant_type = 'password'
        client_secret = '27bb8fb7-68ad-4932-a7c5-c8ecb114f3f8'
        url = 'https://keycloak.dp.vinai-systems.com/auth/realms/vinai/protocol/openid-connect/token'
        payload = {
            'username': user,
            'password': password,
            'client_id': client_id,
            'grant_type': grant_type,
            'client_secret': client_secret,
        }
        res = requests.post(url, data=payload)
        res.raise_for_status()
        token = res.json()['access_token']
        return token

    def get_task_ids(
        self,
        project_id: int,
    ) -> List[int]:
        url = f'{VisionX.BASE_URL}/api/v1/projects/{project_id}'
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        task_ids = [task['id'] for task in res.json()['tasks']]
        return task_ids

    def get_annotations(
        self,
        task_id: int,
    ) -> str:
        pass
