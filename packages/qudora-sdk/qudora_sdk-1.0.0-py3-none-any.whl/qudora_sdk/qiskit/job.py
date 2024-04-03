"""
    Copyright (C) 2024  QUDORA GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


Job interface to communicate with QUDORA Cloud Jobs endpoint.
"""

from qiskit.providers import JobV1 as Job
from qiskit.providers.jobstatus import JobStatus
from qiskit.providers.backend import BackendV2
from qiskit.result import Result
from .util import raise_exception_from_response, convert_jobstatusapi_to_jobstatusqiskit
import json
import requests


class QUDORAJob(Job):
    """ Job that interacts with the QUDORA Cloud"""

    def __init__(self, backend: BackendV2, job_id: int, job_json: json):
        """Initializes a job referencing a job in the QUDORA Cloud.

        Args:
            backend (BackendV2): Backend that executes the job
            job_id (int): ID of the job.
            job_json (json): JSON data describing the job.
        """
        super().__init__(backend, job_id)
        self._backend = backend
        self.job_json = job_json

    def result(self, return_raw_format=False, timeout=30, wait=5) -> Result:
        """Waits for result of job and returns it.

        Args:
            return_raw_format (bool, optional): Return unprocessed result. Defaults to False.
            timeout (int, optional): Maximum time [s] to wait for result. Defaults to 30.
            wait (int, optional): Rate [s] at which to query results. Defaults to 5.
        Raises:
            RuntimeError: Raised if job failed in QUDORA Cloud.
        Returns:
            Result: Results of job in Qiskit-format.
        """
        self.wait_for_final_state(timeout=timeout, wait=wait)
        result = self.__query_job_from_api(include_data=True)
        result = result.json()[0]

        if return_raw_format:
            return result

        # Check status from results
        status = convert_jobstatusapi_to_jobstatusqiskit(result['status'])
        if status != JobStatus.DONE:
            raise RuntimeError(f"Job finished with status {status.name}: \n \t {result['user_error']}")

        meas_result = [{'data': {'counts': json.loads(result['result'])}, 
                        'shots': result['shots'],
                        'success': True}]

        return Result.from_dict({
            'results': meas_result,
            'backend_name': str(self._backend),
            'backend_version': self._backend.version,
            'job_id': self._job_id,
            'qobj_id': self._job_id,
            'success': True,
        })
        
    def submit(self):
        print("Submission is handled via the backend.run() functionality.")
        raise NotImplementedError

    def status(self) -> JobStatus:
        """Queries the job status from QUDORA Cloud.

        Raises:
            RuntimeError: Raised when connection fails.

        Returns:
            JobStatus: Status in Qiskit-format.
        """
        response = self.__query_job_from_api(include_data=False)
        raise_exception_from_response(response)

        api_content = json.loads(response.text)
        status = api_content[0]["status"]
        job_status = convert_jobstatusapi_to_jobstatusqiskit(status)
        return job_status

    def __query_job_from_api(self, include_data=True) -> requests.Response: 
        """Queries the job from the API

        Args:
            include_data (bool, optional): Should job data (input,results,errors) be included. Defaults to True.
        Returns:
            requests.Response: Response from QUDORA Cloud.
        """
        response = requests.get(self._backend.url,
                    params={'job_id': self._job_id,
                            'include_results': include_data,
                            'include_tiasm': False,
                            'include_input_data': include_data,
                            'include_user_error': include_data},
                    headers=self._backend._provider.get_header(),
                    timeout=self._backend._provider.timeout)
        return response
 
    def cancel(self):
        """Tries to cancel a job"""
        response = requests.put(self._backend.url,
                                  params={'job_id': self._job_id,
                                          'status_name': "Canceled"}
                                  ,headers=self._backend._provider.get_header(),
                                  timeout=self._backend._provider.timeout)
        
        raise_exception_from_response(response)
