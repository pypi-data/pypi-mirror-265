import difflib
import time

text1 = """
The project, "micrograd", is currently at version 0.8.0 and was authored by Andrej Karpathy. It is structured into two main directories: "micrograd" and "test". The "micrograd" directory contains the main source code for the project, while the "test" directory contains the test code.

The project uses Python 3.10 and has dependencies on numpy, sklearn, and matplotlib. The build system requires "poetry-core" and uses "poetry.core.masonry.api" as the build backend.

The main files in the project are:
- `test/test_engine.py`: Contains tests for the engine component of the project.
- `micrograd/nn.py`: Contains code related to neural networks.
- `micrograd/__init__.py`: The initialization file for the "micrograd" package.
- `micrograd/engine.py`: Contains the main engine code for the project. It defines a `Value` class that stores a single scalar value and its gradient. This class is central to the project as it implements methods for basic mathematical operations, and more importantly, methods for automatic differentiation (autograd), which is a key component in training neural networks.
- `micrograd/demo.py`: Likely contains a demonstration or example usage of the project.

This project appears to be a minimalistic implementation of a deep learning library, focusing on the autograd feature. The `Value` class in `engine.py` is the heart of this library, implementing the forward and backward passes necessary for neural network training.
"""
text2 = """
The project, "micrograd", is currently at version 0.8.0 and was authored by Andrej Karpathy. It is structured into two main directories: "micrograd" and "test". The "micrograd" directory contains the main source code for the project, while the "test" directory contains the test code.

The project uses Python 3.10 and has dependencies on numpy, sklearn, and matplotlib. The build system requires "poetry-core" and uses "poetry.core.masonry.api" as the build backend.

The main files in the project are:
- `test/test_engine.py`: Contains tests for the engine component of the project.
- `micrograd/nn.py`: Contains code related to neural networks, including the definition of `Module`, `Neuron`, `Layer`, and `MLP` classes. These classes form the building blocks of the neural network functionality in the project. The `Module` class provides a base for other classes, with methods for zeroing gradients and retrieving parameters. The `Neuron` class represents a single neuron, the `Layer` class represents a layer of neurons, and the `MLP` class represents a multi-layer perceptron.
- `micrograd/__init__.py`: The initialization file for the "micrograd" package.
- `micrograd/engine.py`: Contains the main engine code for the project. It defines a `Value` class that stores a single scalar value and its gradient. This class is central to the project as it implements methods for basic mathematical operations, and more importantly, methods for automatic differentiation (autograd), which is a key component in training neural networks.
- `micrograd/demo.py`: Likely contains a demonstration or example usage of the project.

This project appears to be a minimalistic implementation of a deep learning library, focusing on the autograd feature. The `Value` class in `engine.py` is the heart of this library, implementing the forward and backward passes necessary for neural network training. The `nn.py` file extends this functionality by providing the necessary classes to build and manipulate neural networks.
"""


def colored(diff_line: str) -> str:
    line = diff_line if diff_line.endswith("\n") else f"{diff_line}\n"
    red = "\033[38;2;255;0;0m"
    green = "\033[38;2;0;255;0m"
    reset_color = "\033[0m"

    if line.startswith("+"):
        return f"{green}{line[1:]}{reset_color}"
    elif line.startswith("-"):
        return f"{red}{line[1:]}{reset_color}"
    else:
        return line[1:]


def animate_diff(a: str, b: str):
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    diff = difflib.unified_diff(a_lines, b_lines, n=len(a_lines))
    print("\033[H\033[J", end="")  # Clear the screen

    lines = []
    for line in diff:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        lines.append(colored(line))
    print("".join(lines))


if __name__ == "__main__":
    animate_diff(text1, text2)
