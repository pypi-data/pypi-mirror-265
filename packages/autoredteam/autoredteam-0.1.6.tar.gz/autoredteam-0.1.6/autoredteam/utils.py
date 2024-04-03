import contextlib
import importlib
import inspect
import itertools
import numpy as np
import os
import pathlib
from typing import List

import warnings

warnings.filterwarnings("ignore")

from garak._plugins import enumerate_plugins as ep

# constants
TRUST_DICT = {
    "Security": [
        "dan",
        "encoding",
        "gcg",
        "glitch",
        "goodside",
        "knownbadsignatures",
        "malwaregen",
        "packagehallucination",
        "promptinject",
        "xss",
        "replay",
    ],
    "Privacy": ["leakreplay", "replay"],
    "Hallucination": ["snowball", "misleading", "packagehallucination", "advqa"],
    "Robustness": ["advglue"],
    "Toxicity": ["atkgen", "continuation", "realtoxicityprompts"],
    "Stereotype": ["advstereo"],
    "Fairness": ["adultdata", "winobias"],
    "Ethics": ["lmrc", "hendrycksethics"],
    "Performance": [],
}

TRUST_DICT_PERTURBATIONS = {
    "Security": ["prompt-injection"],
    "Hallucination": ["benign-paraphrases"],
    "Robustness": ["adversarial-paraphrases"],
}

TRUST_DICT_METRICS = {
    "Hallucination": [
        "consistency." + met
        for met in [
            "Entailment",
            "Contradiction",
            "BLEU",
            "BERTScore",
            "AgreementNER",
            "AgreementLLM",
            "CheckLLM",
        ]
    ]
    + ["hhem.HHEM", "ragas.Faithfulness"],
    # + ["hhem.HHEM", "ragas.Faithfulness", "selfcheck.SelfCheck"],
    "Performance": [
        "ragas." + met
        for met in [
            "AnswerCorrectness",
            "AnswerRelevancy",
            "AnswerSimilarity",
            "ContextEntityRecall",
            "ContextPrecision",
            "ContextRecall",
            "ContextRelevancy",
        ]
    ],
}

METADATA_FIELDS = ["__doc__", "detectors", "uri", "name", "description", "tags", "goal"]


# functions
def local_constructor(self):
    super(self.__class__, self).__init__()


# ack: https://joeletts.com/2020/creating-dynamic-modules-python-3/
def new_module(mod_name):
    spec = importlib.machinery.ModuleSpec(mod_name, None)
    return importlib.util.module_from_spec(spec)


def create_module(mod_name, object_list):
    mod = new_module(mod_name)
    for obj in object_list:
        setattr(mod, obj.__name__, obj)

    return mod


all_probes = ep()
active_probes = [p[0] for p in all_probes if p[1] is True]

GARAK_PROBE_MODULES = {}
for probe in active_probes:
    # extract elements from probe string
    _, module_name, probe_name = probe.split(".")

    # create module if needed, then import
    if module_name not in GARAK_PROBE_MODULES.keys():
        GARAK_PROBE_MODULES[module_name] = [probe_name]
    else:
        GARAK_PROBE_MODULES[module_name].append(probe_name)


def simulate_group_ci(counts_vec, nobs_vec, nboot=1000, seed=42, return_boot=False):
    """Compute bootstrap confidence intervals for a group of proportions.

    Parameters
    ----------
    counts_vec : array-like
        Vector of counts for each proportion.
    nobs_vec : array-like
        Vector of total observations for each proportion.
    nboot : int
        Number of bootstrap samples to take.
    seed : int
        Random seed for reproducibility. Default is 42.
    return_boot : bool
        Whether to return the bootstrap samples. Default is False.

    Returns
    -------
    ci_low, ci_upp: float
        Lower and upper confidence interval bounds.
    score_boot : array-like
        Bootstrap samples. Only returned if return_boot is True.
    """
    np.random.seed(seed)
    ncat = len(counts_vec)
    score_boot = np.zeros(nboot)
    for b in range(nboot):
        prob_boot = 0
        for cat in range(ncat):
            # sample with replacement
            prob_boot += (
                np.sum(
                    np.random.binomial(nobs_vec[cat], counts_vec[cat] / nobs_vec[cat])
                )
                / nobs_vec[cat]
            )
        score_boot[b] = prob_boot / ncat

    ci_low = np.percentile(score_boot, 2.5)
    ci_upp = np.percentile(score_boot, 97.5)

    if return_boot:
        return ci_low, ci_upp, score_boot
    else:
        return ci_low, ci_upp


def enumerate_plugins(
    category: str = "tests", skip_base_classes=True, modules=None
) -> List[tuple[str, bool]]:
    """A function for listing all modules & plugins of the specified kind.

    garak's plugins are organised into four packages - probes, detectors, generators
    and harnesses. Each package contains a base module defining the core plugin
    classes. The other modules in the package define classes that inherit from the
    base module's classes.

    enumerate_plugins() works by first looking at the base module in a package
    and finding the root classes here; it will then go through the other modules
    in the package and see which classes can be enumerated from these.

    :param category: the name of the plugin package to be scanned; should
      be one of probes, detectors, generators, or harnesses.
    :type category: str
    :param skip_base_classes: whether to skip the base classes in the package
        when enumerating plugins
    :type skip_base_classes: bool
    :param modules: a list of modules to scan for plugins; if None, all modules
    :return: a list of tuples of the form (plugin name, active)
    """

    if category not in ("tests", "detectors", "agents", "harnesses", "perturbations"):
        raise ValueError("Not a recognised plugin type:", category)

    base_mod = importlib.import_module(f"autoredteam.{category}.base")

    if category == "harnesses":
        root_plugin_classname = "Harness"
    else:
        root_plugin_classname = category.title()[:-1]

    base_plugin_classnames = set(
        [
            n
            for n in dir(base_mod)
            if "__class__" in dir(getattr(base_mod, n))
            and getattr(base_mod, n).__class__.__name__
            == "type"  # be careful with what's imported into base modules
        ]
        + [root_plugin_classname]
    )

    plugin_class_names = []

    basedir = pathlib.Path(__file__).parents[0]
    if not modules:
        modules = [
            m
            for m in os.listdir(basedir / category)
            if not m.startswith("__") and m.endswith(".py")
        ]
    # for module_filename in sorted(os.listdir(basedir / category)):
    #     if not module_filename.endswith(".py"):
    #         continue
    #     if module_filename.startswith("__"):
    #         continue
    exclude = ["Tox"]
    for module_filename in sorted(modules):
        if module_filename == "base.py" and skip_base_classes:
            continue
        module_name = module_filename.replace(".py", "")
        mod = importlib.import_module(f"autoredteam.{category}.{module_name}")
        module_entries = set(
            [
                entry
                for entry in dir(mod)
                if not entry.startswith("__") and entry not in exclude
            ]
        )
        if skip_base_classes:
            module_entries = module_entries.difference(base_plugin_classnames)
        module_plugin_names = set()
        for module_entry in module_entries:
            obj = getattr(mod, module_entry)
            if inspect.isclass(obj):
                if obj.__bases__[-1].__name__ in base_plugin_classnames:
                    module_plugin_names.add((module_entry, obj.active))

        for module_plugin_name, active in sorted(module_plugin_names):
            plugin_class_names.append(
                (f"{category}.{module_name}.{module_plugin_name}", active)
            )
    return plugin_class_names


def list_all_tests(modules=None, active=True, metadata=False):
    """List all tests in the autoredteam.tests package.

    Args:
        modules (list): A list of modules to scan for tests. Defaults to None.

    Returns:
        dict: A dictionary of tests, keyed by module name.
    """
    with contextlib.redirect_stdout(None):
        en = enumerate_plugins(category="tests", modules=modules)

    # filter to active plugins if needed
    if active:
        en = [p for p in en if p[1] == True]

    ret = {
        module: [plugin.split(".")[2] for plugin, _ in plugins]
        for module, plugins in itertools.groupby(en, lambda x: x[0].split(".")[1])
    }

    if metadata:
        ret2 = {}
        for module, plugins in ret.items():
            ret2[module] = {}
            module_instance = importlib.import_module(f"autoredteam.tests.{module}")
            for plugin in plugins:
                plugin_instance = getattr(module_instance, plugin)()
                ret2[module][plugin] = {
                    field: getattr(plugin_instance, field)
                    for field in METADATA_FIELDS
                    if field != "detectors"
                }
        return ret2

    return ret
