import sys,gc,traceback
import math,torch,matplotlib.pyplot as plt, random, numpy as np
from itertools import zip_longest
import fastcore.all as fc
from collections.abc import Mapping
from operator import attrgetter
from functools import partial
from copy import copy

from torch import optim
import torch.nn.functional as F
from torch.optim.lr_scheduler import ExponentialLR
from torch.utils.data import DataLoader

from torcheval.metrics import Mean

from fastprogress import progress_bar,master_bar

import wandb

__all__ = ['def_device', 'set_seed', 'to_device', 'clean_tb', 'clean_ipython_hist', 'clean_mem', 'Dataset', 'DataLoaders', 'def_device', 'show_image', 'subplots', 'get_grid', 'show_images', 
           'CancelFitException', 'CancelBatchException', 'CancelEpochException', 'Callback', 'SingleBatchCB', 'MetricsCB', 'DeviceCB', 'TrainCB', 'ProgressCB', 'Learner', 
           'TrainLearner', 'LRFinderCB', 'lr_find', 'Hook', 'Hooks', 'HooksCallback', 'append_stats', 'ActivationStats', 'BaseSchedCB', 'BatchSchedCB', 'WandBCB', 'AccelerateCB']

# General Utils
    
def set_seed(seed, deterministic=False):
    """
    Sets the seed for random number generators in numpy, random, and torch to ensure reproducible results.
    Optionally makes PyTorch operations deterministic.

    Parameters:
    - seed (int): Seed value.
    - deterministic (bool): Whether to make PyTorch operations deterministic. Default is False.
    """
    torch.use_deterministic_algorithms(deterministic)
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

# Memory Utils

def_device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'

def to_device(x, device=def_device):
    """Move tensor or collection of tensors to a specified device.
    
    Parameters:
    - x: The tensor or collection of tensors to move.
    - device: The target device (e.g., 'cpu', 'cuda:0'). If None, moves to CPU and handles float16 conversion.
    
    Returns:
    - The tensor or collection of tensors moved to the specified device.
    """
    if isinstance(x, torch.Tensor):
        res = x.to(device) if device is not None else x.detach().cpu()
        # Special handling for float16 tensors when moving to CPU without a specified device
        return res.float() if res.dtype == torch.float16 and device is None else res
    elif isinstance(x, Mapping):
        return {k: to_device(v, device) for k, v in x.items()}
    elif isinstance(x, list):
        return [to_device(o, device) for o in x]
    elif isinstance(x, tuple):
        return tuple(to_device(o, device) for o in x)
    else:
        return x  # Return the object as is if it's not a tensor or a collection

def clean_tb():
    """
    Clears traceback information to avoid memory leak in long-running scripts. 
    Useful in environments that keep history of exceptions, like IPython.
    """
    if hasattr(sys, 'last_traceback'):
        traceback.clear_frames(sys.last_traceback)
        delattr(sys, 'last_traceback')
    if hasattr(sys, 'last_type'): delattr(sys, 'last_type')
    if hasattr(sys, 'last_value'): delattr(sys, 'last_value')

def clean_ipython_hist():
    """
    Cleans up IPython command history in the current session to free up memory. 
    Mainly useful when running in IPython environments.
    """
    if not 'get_ipython' in globals(): return
    ip = get_ipython()
    user_ns = ip.user_ns
    ip.displayhook.flush()
    pc = ip.displayhook.prompt_count + 1
    for n in range(1, pc): user_ns.pop('_i'+repr(n),None)
    user_ns.update(dict(_i='',_ii='',_iii=''))
    hm = ip.history_manager
    hm.input_hist_parsed[:] = [''] * pc
    hm.input_hist_raw[:] = [''] * pc
    hm._i = hm._ii = hm._iii = hm._i00 =  ''

def clean_mem():
    """
    A comprehensive memory cleanup utility function. It clears Python garbage,
    PyTorch CUDA cache, IPython command history, and traceback information.
    """
    clean_tb()
    clean_ipython_hist()
    gc.collect()
    torch.cuda.empty_cache()

# Data & Vis Utils

class Dataset():
    """
    A simple dataset wrapper for PyTorch. It stores inputs and targets and retrieves them based on index.
    
    Parameters:
    - x: The inputs to the model.
    - y: The target outputs for the inputs.
    """
    def __init__(self, x, y): self.x, self.y = x, y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i], self.y[i] 

class DataLoaders():
    """
    A convenience wrapper for creating training and validation DataLoader instances.

    Parameters:
    - train_ds: The training dataset.
    - valid_ds: The validation dataset.
    - bs (int): Batch size. Default is 64.
    - shuffle (bool): Whether to shuffle the training dataset. Default is True.
    """
    def __init__(self, train_ds, valid_ds, bs=64, shuffle=True):
        self.train = DataLoader(train_ds, bs, shuffle=shuffle)
        self.valid = DataLoader(valid_ds, bs)

@fc.delegates(plt.Axes.imshow)
def show_image(im, ax=None, figsize=None, title=None, noframe=True, **kwargs):
    """
    Show a PIL or PyTorch image on `ax`.

    Parameters:
    - im: The image to display. Can be a PIL image, PyTorch tensor, or NumPy array.
    - ax: The Matplotlib axes to use for plotting. If None, a new axes is created.
    - figsize: Figure size in inches.
    - title: Title for the image.
    - noframe (bool): If True, no frame is shown around the image. Default is True.
    - **kwargs: Additional keyword arguments for plt.imshow.

    Returns:
    The Matplotlib axes with the image.
    """
    if fc.hasattrs(im, ('cpu','permute','detach')):
        im = im.detach().cpu()
        if len(im.shape)==3 and im.shape[0]<5: im=im.permute(1,2,0)
    elif not isinstance(im,np.ndarray): im=np.array(im)
    if im.shape[-1]==1: im=im[...,0]
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    ax.imshow(im, **kwargs)
    if title is not None: ax.set_title(title)
    ax.set_xticks([]) 
    ax.set_yticks([]) 
    if noframe: ax.axis('off')
    return ax

@fc.delegates(plt.subplots, keep=True)
def subplots(
    nrows:int=1, # Number of rows in returned axes grid
    ncols:int=1, # Number of columns in returned axes grid
    figsize:tuple=None, # Width, height in inches of the returned figure
    imsize:int=3, # Size (in inches) of images that will be displayed in the returned figure
    suptitle:str=None, # Title to be set to returned figure
    **kwargs
): 
    """
    Creates a figure and a set of subplots.

    Parameters:
    - nrows (int): Number of rows in the grid.
    - ncols (int): Number of columns in the grid.
    - figsize (tuple): Width, height in inches of the figure. If None, size is determined by imsize.
    - imsize (int): Size in inches of images that will be displayed. Affects default figsize.
    - suptitle (str): A title to be set on the figure.
    - **kwargs: Additional keyword arguments for plt.subplots.

    Returns:
    A figure and an array of Axes objects.
    """
    if figsize is None: figsize=(ncols*imsize, nrows*imsize)
    fig,ax = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
    if suptitle is not None: fig.suptitle(suptitle)
    if nrows*ncols==1: ax = np.array([ax])
    return fig,ax

@fc.delegates(subplots)
def get_grid(
    n:int, # Number of axes
    nrows:int=None, # Number of rows, defaulting to `int(math.sqrt(n))`
    ncols:int=None, # Number of columns, defaulting to `ceil(n/rows)`
    title:str=None, # If passed, title set to the figure
    weight:str='bold', # Title font weight
    size:int=14, # Title font size
    **kwargs,
): 
    """
    Return a grid of `n` axes, organized in `rows` by `cols`.

    Parameters:
    - n (int): Number of axes to create.
    - nrows (int): Number of rows. If None, calculated based on `n`.
    - ncols (int): Number of columns. If None, calculated based on `n` and `nrows`.
    - title (str): Title for the figure.
    - weight (str): Font weight for the title.
    - size (int): Font size for the title.
    - **kwargs: Additional arguments to pass to the subplots function.

    Returns:
    A figure and a grid of Axes objects.
    """
    if nrows: ncols = ncols or int(np.floor(n/nrows))
    elif ncols: nrows = nrows or int(np.ceil(n/ncols))
    else:
        nrows = int(math.sqrt(n))
        ncols = int(np.floor(n/nrows))
    fig,axs = subplots(nrows, ncols, **kwargs)
    for i in range(n, nrows*ncols): axs.flat[i].set_axis_off()
    if title is not None: fig.suptitle(title, weight=weight, size=size)
    return fig,axs

@fc.delegates(subplots)
def show_images(ims:list, # Images to show
                nrows:int|None=None, # Number of rows in grid
                ncols:int|None=None, # Number of columns in grid (auto-calculated if None)
                titles:list|None=None, # Optional list of titles for each image
                **kwargs):
    """
    Display a list of images in a grid.

    Parameters:
    - ims (list): Images to display.
    - nrows (int|None): Number of rows in the grid. If None, the square root of the number of images is used.
    - ncols (int|None): Number of columns in the grid. If None, calculated based on `nrows` and number of images.
    - titles (list|None): A list of titles for each image.
    - **kwargs: Additional keyword arguments to pass to `get_grid`.

    Returns:
    None. The images are displayed using Matplotlib.
    """
    axs = get_grid(len(ims), nrows, ncols, **kwargs)[1].flat
    for im,t,ax in zip_longest(ims, titles or [], axs): show_image(im, ax=ax, title=t)

# Training Utils - Leaner and Callbacks
    
# Exception classes to signal the cancellation of fit, batch, or epoch processes
class CancelFitException(Exception): pass
class CancelBatchException(Exception): pass
class CancelEpochException(Exception): pass

# Base class for callbacks with a default order
class Callback(): order = 0

class with_cbs:
    """
    A decorator to manage the calling of callbacks around a method call.

    Parameters:
    - nm (str): The name of the method around which callbacks are to be fired.
    """
    def __init__(self, nm): self.nm = nm
    def __call__(self, f):
        def _f(o, *args, **kwargs):
            try:
                o.callback(f'before_{self.nm}')
                f(o, *args, **kwargs)
                o.callback(f'after_{self.nm}')
            except globals()[f'Cancel{self.nm.title()}Exception']: pass
            finally: o.callback(f'cleanup_{self.nm}')
        return _f

def run_cbs(cbs, method_nm, learn=None):
    """
    Runs callbacks based on their defined order.

    Parameters:
    - cbs (list): List of callbacks to be run.
    - method_nm (str): The name of the callback method to run.
    - learn (Learner, optional): The learner object.
    """
    for cb in sorted(cbs, key=attrgetter('order')):
        method = getattr(cb, method_nm, None)
        if method is not None: method(learn)

class Learner():
    """
    Encapsulates training logic for a learning model, including callbacks and optimization.

    Parameters:
    - model: The model to train.
    - dls: Tuple of data loaders for training and validation.
    - loss_func: The loss function.
    - lr (float): Learning rate for the optimizer.
    - cbs (list, optional): List of callbacks to use during training.
    - opt_func: The optimizer function to use, defaults to SGD.
    """
    def __init__(self, model, dls=(0,), loss_func=F.mse_loss, lr=0.1, cbs=None, opt_func=optim.SGD):
        cbs = fc.L(cbs)
        fc.store_attr()

    @with_cbs('batch')
    def _one_batch(self):
        self.predict()
        self.callback('after_predict')
        self.get_loss()
        self.callback('after_loss')
        if self.training:
            self.backward()
            self.callback('after_backward')
            self.step()
            self.callback('after_step')
            self.zero_grad()

    @with_cbs('epoch')
    def _one_epoch(self):
        for self.iter,self.batch in enumerate(self.dl): self._one_batch()

    def one_epoch(self, training):
        self.model.train(training)
        self.dl = self.dls.train if training else self.dls.valid
        self._one_epoch()

    @with_cbs('fit')
    def _fit(self, train, valid):
        for self.epoch in self.epochs:
            if train: self.one_epoch(True)
            if valid: torch.no_grad()(self.one_epoch)(False)

    def fit(self, n_epochs=1, train=True, valid=True, cbs=None, lr=None):
        cbs = fc.L(cbs)
        for cb in cbs: self.cbs.append(cb)
        try:
            self.n_epochs = n_epochs
            self.epochs = range(n_epochs)
            if lr is None: lr = self.lr
            if self.opt_func: self.opt = self.opt_func(self.model.parameters(), lr)
            self._fit(train, valid)
        finally:
            for cb in cbs: self.cbs.remove(cb)

    def __getattr__(self, name):
        if name in ('predict','get_loss','backward','step','zero_grad'): return partial(self.callback, name)
        raise AttributeError(name)

    def callback(self, method_nm): run_cbs(self.cbs, method_nm, self)
    
    @property
    def training(self): return self.model.training

class TrainLearner(Learner):
    """A subclass of Learner with overridden methods for the training process."""
    def predict(self): self.preds = self.model(self.batch[0])
    def get_loss(self): self.loss = self.loss_func(self.preds, self.batch[1])
    def backward(self): self.loss.backward()
    def step(self): self.opt.step()
    def zero_grad(self): self.opt.zero_grad()

class SingleBatchCB(Callback):
    """A callback to stop training after a single batch. Useful for quick tests."""
    order = 1
    def after_batch(self, learn): raise CancelFitException()

class TrainCB(Callback):
    """
    A callback that implements the basic training loop operations for a batch.
    
    Parameters:
        n_inp (int): Number of inputs expected by the model. Default is 1.
    """
    def __init__(self, n_inp=1): self.n_inp = n_inp
    def predict(self, learn): learn.preds = learn.model(*learn.batch[:self.n_inp])
    def get_loss(self, learn): learn.loss = learn.loss_func(learn.preds, *learn.batch[self.n_inp:])
    def backward(self, learn): learn.loss.backward()
    def step(self, learn): learn.opt.step()
    def zero_grad(self, learn): learn.opt.zero_grad()

class DeviceCB(Callback):
    """
    A callback to ensure all tensors are moved to the specified device before training.
    
    Parameters:
        device (str): The device to move tensors to. Defaults to 'def_device'.
    """
    def __init__(self, device=def_device): fc.store_attr()
    def before_fit(self, learn):
        if hasattr(learn.model, 'to'): learn.model.to(self.device)
    def before_batch(self, learn): learn.batch = to_device(learn.batch, device=self.device)

class MetricsCB(Callback):
    """
    A callback to compute and log metrics after each epoch.
    
    Parameters:
        *ms: Metric instances.
        **metrics: Named metric instances.
    """
    def __init__(self, *ms, **metrics):
        for o in ms: metrics[type(o).__name__] = o
        self.metrics = metrics
        self.all_metrics = copy(metrics)
        self.all_metrics['loss'] = self.loss = Mean()

    def _log(self, d): print(d)
    def before_fit(self, learn): learn.metrics = self
    def before_epoch(self, learn): [o.reset() for o in self.all_metrics.values()]

    def after_epoch(self, learn):
        """Log the computed metrics after each epoch."""
        log = {k:f'{v.compute():.3f}' for k,v in self.all_metrics.items()}
        log['epoch'] = learn.epoch
        log['train'] = 'train' if learn.model.training else 'eval'
        self._log(log)

    def after_batch(self, learn):
        """Update metrics after each batch."""
        x,y,*_ = to_device(learn.batch, device=None)
        for m in self.metrics.values(): m.update(to_device(learn.preds, device=None), y)
        self.loss.update(to_device(learn.loss, device=None), weight=len(x))

class ProgressCB(Callback):
    """
    A callback to display training progress using fastprogress bars.
    
    Parameters:
        plot (bool): Whether to plot loss graphs. Default is False.
    """
    order = MetricsCB.order+1
    def __init__(self, plot=False): self.plot = plot

    def before_fit(self, learn):
        """Initialize the progress bar."""
        learn.epochs = self.mbar = master_bar(learn.epochs)
        self.first = True
        if hasattr(learn, 'metrics'): learn.metrics._log = self._log
        self.losses = []
        self.val_losses = []

    def _log(self, d):
        """Log progress to the master bar."""
        if self.first:
            self.mbar.write(list(d), table=True)
            self.first = False
        self.mbar.write(list(d.values()), table=True)

    def before_epoch(self, learn):
        """Wrap the DataLoader with a progress bar.""" 
        learn.dl = progress_bar(learn.dl, leave=False, parent=self.mbar)
    def after_batch(self, learn):
        """Update the progress bar comment with the current loss."""
        learn.dl.comment = f'{learn.loss:.3f}'
        if self.plot and hasattr(learn, 'metrics') and learn.training:
            self.losses.append(learn.loss.item())
            if self.val_losses: self.mbar.update_graph([[fc.L.range(self.losses), self.losses],[fc.L.range(learn.epoch).map(lambda x: (x+1)*len(learn.dls.train)), self.val_losses]])
    
    def after_epoch(self, learn): 
        """Plot validation losses if applicable."""
        if not learn.training:
            if self.plot and hasattr(learn, 'metrics'): 
                self.val_losses.append(learn.metrics.all_metrics['loss'].compute())
                self.mbar.update_graph([[fc.L.range(self.losses), self.losses],[fc.L.range(learn.epoch+1).map(lambda x: (x+1)*len(learn.dls.train)), self.val_losses]])

class LRFinderCB(Callback):
    """
    Callback for finding an optimal learning rate using the LR Finder approach.

    Parameters:
        gamma (float): The multiplicative increase factor for the learning rate after each batch. Default is 1.3.
        max_mult (float): The maximum multiple over the minimum loss at which training is stopped. Default is 3.
    """
    def __init__(self, gamma=1.3, max_mult=3): fc.store_attr()
    
    def before_fit(self, learn):
        self.sched = ExponentialLR(learn.opt, self.gamma)
        self.lrs,self.losses = [],[]
        self.min = math.inf

    def after_batch(self, learn):
        if not learn.training: raise CancelEpochException()
        self.lrs.append(learn.opt.param_groups[0]['lr'])
        loss = to_device(learn.loss, device=None)
        self.losses.append(loss)
        if loss < self.min: self.min = loss
        if math.isnan(loss) or (loss > self.min*self.max_mult):
            raise CancelFitException()
        self.sched.step()

    def cleanup_fit(self, learn):
        plt.plot(self.lrs, self.losses)
        plt.xscale('log')

@fc.patch
def lr_find(self:Learner, gamma=1.3, max_mult=3, start_lr=1e-5, max_epochs=10):
    self.fit(max_epochs, lr=start_lr, cbs=LRFinderCB(gamma=gamma, max_mult=max_mult))

class BaseSchedCB(Callback):
    def __init__(self, sched): self.sched = sched
    def before_fit(self, learn): self.schedo = self.sched(learn.opt)
    def _step(self, learn):
        if learn.training: self.schedo.step()

class BatchSchedCB(BaseSchedCB):
    def after_batch(self, learn): self._step(learn)

# Hooks and Activation Stats

class Hook():
    """
    Hook for PyTorch models to capture layer outputs.

    Parameters:
        m: The model or layer to attach the hook to.
        f: The function to be called when the hook is triggered.
    """
    def __init__(self, m, f): self.hook = m.register_forward_hook(partial(f, self))
    def remove(self): self.hook.remove()
    def __del__(self): self.remove()

class Hooks(list):
    """
    A container for managing multiple hooks.

    Parameters:
        ms: Iterable of models or layers to attach hooks to.
        f: The function to be called by each hook.
    """
    def __init__(self, ms, f): super().__init__([Hook(m, f) for m in ms])
    def __enter__(self, *args): return self
    def __exit__ (self, *args): self.remove()
    def __del__(self): self.remove()
    def __delitem__(self, i):
        self[i].remove()
        super().__delitem__(i)
    def remove(self):
        for h in self: h.remove()

class HooksCallback(Callback):
    """
    Callback to manage a set of hooks during training.

    Parameters:
        hookfunc: The function to be called by the hooks.
        mod_filter: Filter function to select which modules to hook.
        on_train: Whether to apply hooks during training.
        on_valid: Whether to apply hooks during validation.
        mods: Optional specific modules to attach hooks to.
    """
    def __init__(self, hookfunc, mod_filter=fc.noop, on_train=True, on_valid=False, mods=None):
        fc.store_attr()
        super().__init__()
    
    def before_fit(self, learn):
        if self.mods: mods=self.mods
        else: mods = fc.filter_ex(learn.model.modules(), self.mod_filter)
        self.hooks = Hooks(mods, partial(self._hookfunc, learn))

    def _hookfunc(self, learn, *args, **kwargs):
        if (self.on_train and learn.training) or (self.on_valid and not learn.training): self.hookfunc(*args, **kwargs)

    def after_fit(self, learn): self.hooks.remove()
    def __iter__(self): return iter(self.hooks)
    def __len__(self): return len(self.hooks)

def append_stats(hook, mod, inp, outp):
    """
    Appends statistics (mean, std, histogram of activations) to the hook object.

    Parameters:
        hook: The hook object where stats will be stored.
        mod: The model/module from which outputs are captured.
        inp: The input to the module (unused in this function but required by PyTorch hook signature).
        outp: The output from the module, used to calculate statistics.
    """
    if not hasattr(hook,'stats'): hook.stats = ([],[],[])
    acts = to_device(outp, device=None)
    hook.stats[0].append(acts.mean())
    hook.stats[1].append(acts.std())
    hook.stats[2].append(acts.abs().histc(40,0,10))

def get_hist(h):
    """Converts activation histograms stored in a hook into a tensor suitable for plotting."""
    return torch.stack(h.stats[2]).t().float().log1p()

def get_min(h):
    """
    Calculates the minimum activation value from the histograms stored in a hook.

    Parameters:
        h: The hook object containing activation histograms.

    Returns:
        The proportion of activations at the minimum value (assumed to be the first bin of the histogram).
    """
    h1 = torch.stack(h.stats[2]).t().float()
    return h1[0]/h1.sum(0)

class ActivationStats(HooksCallback):
    """
    A callback using hooks to collect and plot statistics of model activations, useful for diagnosing training issues.

    Parameters:
        mod_filter: A filter function to select which modules to attach hooks to.
    """
    def __init__(self, mod_filter=fc.noop): super().__init__(append_stats, mod_filter)

    def color_dim(self, figsize=(11,5)):
        """
        Plots the histograms of activations for each hooked module as images, where color intensity represents frequency.

        Parameters:
            figsize: The size of the figure each histogram is plotted in.
        """
        fig,axes = get_grid(len(self), figsize=figsize)
        for ax,h in zip(axes.flat, self):
            show_image(get_hist(h), ax, origin='lower')

    def dead_chart(self, figsize=(11,5)):
        """
        Plots the proportion of dead activations (activations at the minimum value) for each hooked module.

        Parameters:
            figsize: The size of the figure each proportion plot is plotted in.
        """
        fig,axes = get_grid(len(self), figsize=figsize)
        for ax,h in zip(axes.flatten(), self):
            ax.plot(get_min(h))
            ax.set_ylim(0,1)

    def plot_stats(self, figsize=(10,4)):
        """
        Plots the mean and standard deviation of activations for each hooked module over time.

        Parameters:
            figsize: The size of the figure each statistics plot is plotted in.
        """
        fig,axs = plt.subplots(1,2, figsize=figsize)
        for h in self:
            for i in 0,1: axs[i].plot(h.stats[i])
        axs[0].set_title('Means')
        axs[1].set_title('Stdevs')
        plt.legend(fc.L.range(self))
    
class WandBCB(MetricsCB):
    order=100
    def __init__(self, config, *ms, project='ddpm_cifar10', **metrics):
        fc.store_attr()
        super().__init__(*ms, **metrics)
        
    def before_fit(self, learn): wandb.init(project=self.project, config=self.config)
    def after_fit(self, learn): wandb.finish()

    def _log(self, d, learn): 
        if self.train: 
            wandb.log({'train_'+m:float(d[m]) for m in self.all_metrics})
        else: 
            wandb.log({'val_'+m:float(d[m]) for m in self.all_metrics})
            wandb.log({'samples':self.sample_figure(learn)})
        print(d)

        
    def sample_figure(self, learn, sample):
        with torch.no_grad():
            samples = sample(learn.model, (16, 3, 32, 32))
        s = (samples[-1] + 0.5).clamp(0,1)
        plt.clf()
        fig, axs = get_grid(16)
        for im,ax in zip(s[:16], axs.flat): show_image(im, ax=ax)
        return fig

    def after_batch(self, learn):
        super().after_batch(learn) 
        wandb.log({'loss':learn.loss})

from accelerate import Accelerator

class AccelerateCB(TrainCB):
    order = DeviceCB.order+10
    def __init__(self, n_inp=1, mixed_precision="fp16"):
        super().__init__(n_inp=n_inp)
        self.acc = Accelerator(mixed_precision=mixed_precision)
        
    def before_fit(self, learn):
        learn.model,learn.opt,learn.dls.train,learn.dls.valid = self.acc.prepare(
            learn.model, learn.opt, learn.dls.train, learn.dls.valid)

    def backward(self, learn): self.acc.backward(learn.loss)