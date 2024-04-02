import time
from typing import TYPE_CHECKING, Optional

from .exceptions import BQSDKUsageError

if TYPE_CHECKING:
    from qiskit import QuantumCircuit

MAX_QUBITS_WITH_STATEVEC = 16


def _qiskit_remove_save_instructions_inplace(qc):
    indices = []
    for i, instruction in enumerate(qc.data):
        op = instruction.operation
        # E.g. save_amplitudes, save_state, save_statevector, ...
        if not op.name.startswith("save_"):
            continue
        indices.append(i)
    # We pop from the last one, so that the early indices are
    # not changed.
    for i in indices[::-1]:
        qc.data.pop(i)


def run_circuit_qiskit(qc: "QuantumCircuit", shots: Optional[int] = None):
    from qiskit import transpile
    from qiskit.circuit import Measure
    from qiskit.primitives import StatevectorSampler
    from qiskit.quantum_info import Statevector
    from qiskit_aer import Aer

    qiskit_backend = Aer.get_backend("aer_simulator")
    # Ensure there are no save_statevector.
    _qiskit_remove_save_instructions_inplace(qc)
    transpiled = transpile(qc, qiskit_backend)

    has_measurements = any(isinstance(instr, Measure) for instr, _, _ in qc.data)
    output = {
        "has_measurements": has_measurements,
    }
    if has_measurements or (shots is not None and shots > 0):
        if has_measurements and shots is None:
            raise BQSDKUsageError(
                "You have to specify shots when there are measurements."
            )
        run_start = time.time()
        result = qiskit_backend.run(transpiled, shots=shots).result()
        run_end = time.time()
        output["counts"] = result.get_counts(transpiled)
    elif shots is None or shots == 0:
        sampler = StatevectorSampler()
        run_start = time.time()
        sv = Statevector(transpiled)
        transpiled.measure_all()
        result = sampler.run([transpiled]).result()
        run_end = time.time()
        data_pub = result[0].data
        output["counts"] = data_pub.meas.get_counts()
        num_qubits = len(transpiled.qubits)
        if num_qubits <= MAX_QUBITS_WITH_STATEVEC:
            output["state_vector"] = sv
    else:
        raise BQSDKUsageError(
            f"Wrong configuration for bq.run with device=local: has_measurements={has_measurements}, shots={shots}"
        )
    output["run_start"] = run_start
    output["run_end"] = run_end
    return output


def run_circuit_cirq(circuit, shots: Optional[int] = None):
    try:
        # Prefer qsim whenever possible
        import qsimcirq

        simulator = qsimcirq.QSimSimulator()
    except ImportError:
        import cirq

        simulator = cirq.Simulator()

    has_measurements = circuit.has_measurements()
    output = {
        "has_measurements": has_measurements,
    }
    if has_measurements and shots is None:
        raise BQSDKUsageError("You have to specify shots when there are measurements.")
    run_start = time.time()
    result = simulator.simulate(circuit)
    run_end = time.time()
    output["state_vector"] = result.final_state_vector
    output["counts"] = result.final_state_vector * result.final_state_vector.conj()
    output["run_start"] = run_start
    output["run_end"] = run_end
    return output
