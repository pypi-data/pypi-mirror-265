"""
    Copyright (C) 2024  QUDORA GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

This files defines the interface to connect to quantum devices hosted on the QUDORA Cloud.
"""
import warnings
import requests
import json
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options, Provider
from qiskit.transpiler import Target, InstructionProperties
from qiskit.circuit.library import RGate, RXXGate, Measure, Reset
from qiskit.circuit import Parameter
from qiskit import QuantumCircuit, qasm2
from .job import QUDORAJob
from .util import raise_exception_from_response

def circuit_to_openqasm(circuit: QuantumCircuit) -> str:
    """Converts QuantumCircuit objects to OpenQASM2
    
    Args:
        circuit (QuantumCircuit): Input Circuit
    Returns:
        str: OpenQASM2 string representing the input circuit.
    """
    return qasm2.dumps(circuit)

class QUDORABackend(Backend):
    """ Defines a QUDORA backend available on the QUDORA Cloud """

    def __init__(self, url : str, provider : Provider, info : dict):
        """Creates a QUDORABackend object

        Args:
            url (str): URL of the QUDORA API
            provider (Provider): QUDORAProvider object
            username (str): Username of the Backend at QUDORA Cloud (email-adress)
            display_name (str): Display name of the Backend
        """
        self.url = url
        self.info = info
        
        try:
            self.__username = info['username']
            self.__display_name = info['full_name']
            self.__max_qubits = info['max_n_qubits']
            self.__max_shots = info['max_shots']
            self.__available_settings = info['user_settings_schema']['properties']
        except KeyError as e:
            e.add_note("Did not receive required information from the QUDORA Cloud API.")
            raise e
            
        super().__init__(provider=provider)
        
        # Define target gates
        self._target = Target("Target gates for QUDORA Backends")
        theta = Parameter('theta')
        phi = Parameter('phi')
        rxx_properties = {
            (i,j): InstructionProperties(duration=1e-3, error=1e-4) for i in range(self.num_qubits) for j in range(self.num_qubits)
        }
        r_properties = {
            (i,): InstructionProperties(duration=1e-4, error=1e-4) for i in range(self.num_qubits)
        }
        measure_properties = {
            (i,): InstructionProperties(duration=1e-3, error=1e-3) for i in range(self.num_qubits)
        }
        self._target.add_instruction(RXXGate(theta), rxx_properties)
        self._target.add_instruction(RGate(theta, phi), r_properties)
        self._target.add_instruction(Measure(), measure_properties)
        self._target.add_instruction(Reset(), measure_properties)

        self.options.set_validator("shots", (1,self.__max_shots))

    @property
    def target(self):
        return self._target
    
    @property
    def max_circuits(self):
        return 1
    
    @property
    def num_qubits(self):
        return self.__max_qubits
    
    @property
    def coupling_map(self):
        return None

    @classmethod
    def _default_options(cls):
        """ Sets the default options """
        return Options(shots=1)
    
    def __repr__(self):
        return f"<QUDORABackend('{self.__display_name}')>"
    
    def __post_job(self, job_json: json) -> QUDORAJob:
        """Posts a job to the QUDORA API

        Args:
            job_json (json): Data describing the job.
        Raises:
            RuntimeError: Raised when access to QUDORA Cloud fails.
        Returns:
            QUDORAJob: Referencing the created job in the QUDORA Cloud.
        """
        response = requests.post(self.url, json=job_json, headers=self._provider.get_header(), timeout=self._provider.timeout)
        raise_exception_from_response(response)
       
        # Return the job
        job_id = json.loads(response.text)
        job = QUDORAJob(self, job_id, job_json)
        return job
    
    def show_available_settings(self):
        """Shows available settings for this backend."""
        example_settings = {}
        for key in self.__available_settings.keys():
            example_settings[key] = self.__available_settings[key]['default']

        print(  f"\n Available Options for backend {self.__display_name}: \n \n " \
                f"{json.dumps(self.__available_settings, indent=2)} \n \n" \
                f"You can set these parameters by passing a dictionary to the backend.run() method. \n" \
                f"Below is an example settings dictionary: \n" \
                f"{json.dumps(example_settings, indent=1)}")
        
    def run(self, run_input: QuantumCircuit, job_name: str = "Job from Qiskit-Provider", backend_settings : dict = None, **kwargs) -> QUDORAJob:
        """Submits a given circuit to the QUDORA Cloud.

        Args:
            run_input (QuantumCircuit): Circuit to run.
            job_name (str, optional): Name of the job. Defaults to "Job from Qiskit-Provider".
            backend_settings (_type_, optional): Additional settings for the Backend. Defaults to None.
        Returns:
            QUDORAJob: Object referencing the job in the QUDORA Cloud.
        """

        # Check the keyworded args
        for kwarg in kwargs:
            if not hasattr(self.options, kwarg):
                warnings.warn(
                    f"Option {kwarg} is not used by this backend",
                    UserWarning, stacklevel=2)

        # Get number of shots from args
        shots = kwargs.get('shots', self.options.shots)
        openqasm = circuit_to_openqasm(run_input)
        json_data = {
            'name': job_name,
            'language': 'OpenQASM2',
            'shots': shots,
            'target': self.__username,
            'input_data': openqasm,
            'backend_settings': backend_settings
        }

        # Post the job to the backend
        job = self.__post_job(job_json=json_data)
        return job
