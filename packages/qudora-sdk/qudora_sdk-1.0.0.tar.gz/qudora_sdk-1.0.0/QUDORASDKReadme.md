# QUDORA SDK

**This package can currently only be used by members of QUDORA.**

The QUDORA Software Development Kit (SDK) enables an interaction with quantum devices hosted on the [QUDORA Cloud](https://cloud.qudora.com) from Python code.

The included [Qiskit](https://www.ibm.com/quantum/qiskit)-provider allows direct execution of Qiskit-`QuantumCircuits` on the QUDORA Cloud quantum devices.

## Installation 

To install the latest version of the QUDORA SDK run 

```shell
pip install qudora-sdk
```

## Qiskit-Provider Usage

This section explains the usage of the included Qiskit-provider to access QUDORA Cloud quantum devices.
In order to use the provider an API-Token from the QUDORA Cloud is required. Such a token can be generated [here](https://cloud.qudora.com/main/api-tokens).

### Access to Quantum Devices

To authenticate with the QUDORA Cloud the provider requires the generated API-Token, which is here called `my-example-token`.

```python
from qudora_sdk.qiskit import QUDORAProvider

provider = QUDORAProvider(token="my-example-token")
```
If the authentication was successful, all available quantum devices can be listed.

```python
print(provider.backends())
```

Selecting a particular backend is done with the `get_backend()` function.

```python
backend = provider.get_backend('QVLS Simulator')
```

### Running Qiskit-QuantumCircuits

The quantum devices can execute `QuantumCircuit`-objects written with Qiskit. More information about writing circuits with qiskit can be found [here](https://docs.quantum.ibm.com/build).
Previously created Backend-objects have a `run()`-function to submit circuits to a selected backend.

```python
qc = Quantum Circuit(2,2)
qc.h(0)
qc.h(1)
qc.cx(0,1)

qc.measure(0,0)
qc.measure(1,1)

job = backend.run(qc, job_name='My example job')
```

The `job` object represents a job in the QUDORA Cloud. Its status can be retrieved by calling `job.status()`.
To obtain the result of a job, the `result()` function can be called. This function will wait until the job finishes and return the measurement results.

```python
result = job.result(timeout=30)
print(result)
```

### Customised Settings

A backend has parameters (mostly used for noise models), which you can modify to your needs.
You can list all available settings using the `show_available_settings()`-method.

```python
backend.show_available_settings()
```

To run a job with custom settings, you can pass a settings dictionary to the `run()` method.

```python
custom_settings = {
    'measurement_error_probability': 0.005,
    'two_qubit_gate_noise_strength': 1.0
}

job = backend.run(qc, job_name='Job with custom settings', backend_settings=custom_settings)
```

# LICENSE 

Copyright (C) 2024  QUDORA GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

