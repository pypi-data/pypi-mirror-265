# tiny-torch-util

tiny-torch-util is a personal toy package containing a collection of utility functions and classes designed to streamline PyTorch-based deep learning model training. It offers flexibility through the learner framework, utilizing callbacks for various use cases. Some of these utilities are built from scratch, while others are inspired by the fastai library. Below are the main components of this package:

## Installation

You can install tiny-torch-util using pip:

```bash
pip install tinytorchutil
```

## Usage

Here's how you can utilize the functionalities provided by tiny-torch-util:

### General Utils

- **set_seed(seed, deterministic=False)**: Sets the seed for random number generators in numpy, random, and torch to ensure reproducible results. Optionally makes PyTorch operations deterministic.

- **to_device(x, device=def_device)**: Moves tensors or collections of tensors to a specified device.

- **clean_tb()**: Clears traceback information to avoid memory leaks in long-running scripts.

- **clean_ipython_hist()**: Cleans up IPython command history in the current session to free up memory.

- **clean_mem()**: A comprehensive memory cleanup utility function. It clears Python garbage, PyTorch CUDA cache, IPython command history, and traceback information.

### Data & Vis Utils

- **Dataset(x, y)**: A simple dataset wrapper for PyTorch. It stores inputs and targets and retrieves them based on index.

- **DataLoaders(train_ds, valid_ds, bs=64, shuffle=True)**: A convenience wrapper for creating training and validation DataLoader instances.

- **show_image(im, ax=None, figsize=None, title=None, noframe=True, \*\*kwargs)**: Show a PIL or PyTorch image on `ax`.

- **subplots(nrows=1, ncols=1, figsize=None, imsize=3, suptitle=None, \*\*kwargs)**: Creates a figure and a set of subplots.

- **get_grid(n, nrows=None, ncols=None, title=None, weight='bold', size=14, \*\*kwargs)**: Return a grid of `n` axes, organized in `rows` by `cols`.

- **show_images(ims, nrows=None, ncols=None, titles=None, \*\*kwargs)**: Display a list of images in a grid.

### Training Utils - Learner and Callbacks

- **Learner(model, dls=(0,), loss_func=F.mse_loss, lr=0.1, cbs=None, opt_func=optim.SGD)**: Encapsulates training logic for a learning model, including callbacks and optimization.

- **TrainLearner(Learner)**: A subclass of Learner with overridden methods for the training process.

- **SingleBatchCB**: A callback to stop training after a single batch. Useful for quick tests.

- **TrainCB**: A callback that implements the basic training loop operations for a batch.

- **DeviceCB**: A callback to ensure all tensors are moved to the specified device before training.

- **MetricsCB**: A callback to compute and log metrics after each epoch.

- **ProgressCB**: A callback to display training progress using fastprogress bars.

- **LRFinderCB**: Callback for finding an optimal learning rate using the LR Finder approach.

### Hooks and Activation Stats

- **Hook(m, f)**: Hook for PyTorch models to capture layer outputs.

- **Hooks(ms, f)**: A container for managing multiple hooks.

- **HooksCallback**: Callback to manage a set of hooks during training.

- **ActivationStats**: A callback using hooks to collect and plot statistics of model activations, useful for diagnosing training issues.

### Additional Utilities

- **WandBCB**: A callback to integrate with Weights & Biases for experiment tracking.

- **AccelerateCB**: A callback to utilize PyTorch Lightning's Accelerator for distributed training and mixed precision.

Feel free to explore these utilities and integrate them into your PyTorch-based deep learning projects. If you have any questions or suggestions, please don't hesitate to reach out!
