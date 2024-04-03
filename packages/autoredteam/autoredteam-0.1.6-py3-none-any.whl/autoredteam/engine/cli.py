"""Flow for invoking autoredteam from the command line"""
import argparse
from datetime import datetime
import importlib
import contextlib
import logging
import os
import uuid
import json
from autoredteam.harnesses.rag import RAGHarness
from autoredteam.utils import TRUST_DICT_METRICS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import PyPDF2
from garak import _config


def start_logging():
    # create the logging directory if it doesn't exist
    if not os.path.isdir(_config.reporting.report_dir):
        try:
            os.mkdir(_config.reporting.report_dir)
        except PermissionError as e:
            raise PermissionError(
                "Can't create logging directory %s, quitting",
                _config.reporting.report_dir,
            ) from e

    logging.basicConfig(
        filename=f"{_config.reporting.report_dir}/autoredteam.log",
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)s  %(message)s",
    )


def start_run():
    logging.info("started at %s", _config.transient.starttime_iso)
    _config.transient.run_id = str(uuid.uuid4())  # uuid1 is safe but leaks host info
    _config.transient.report_filename = f"{_config.reporting.report_dir}/autoredteam.{_config.transient.run_id}.report.jsonl"
    _config.transient.reportfile = open(
        _config.transient.report_filename, "w", buffering=1, encoding="utf-8"
    )
    _config.transient.reportfile.write(
        json.dumps(
            {
                "entry_type": "init",
                "autoredteam_version": _config.version,
                "start_time": _config.transient.starttime_iso,
                "run": _config.transient.run_id,
            }
        )
        + "\n"
    )
    logging.info("reporting to %s", _config.transient.report_filename)
    print(f"Reporting to {_config.transient.report_filename}")


def end_run(agent_instance):
    # mistral needs to be shut down explicitly
    if "MistralAPI" in str(type(agent_instance)):
        agent_instance.agent.__del__()

    _config.transient.reportfile.close()
    print(f"Results saved at {_config.transient.report_filename}")
    if _config.transient.hitlogfile:
        _config.transient.hitlogfile.close()

    timetaken = (datetime.now() - _config.transient.starttime).total_seconds()
    msg = f"autoredteam run complete in {timetaken:.1f}s"
    print(msg)
    logging.info(msg)

def process_files(path):
    if os.path.isdir(path):
        files = os.listdir(path)
    else:
        files = [os.path.basename(path)]
        path = os.path.dirname(path)

    documents = []
    for file in files:
        file_path = os.path.join(path, file)
        if file.endswith('.txt'):
            with open(file_path, 'r') as f:
                file_text = f.read()
        elif file.endswith('.pdf'):
            pdf_file_obj = open(file_path, 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
            file_text = ''
            for page_num in range(pdf_reader.numPages):
                page_obj = pdf_reader.getPage(page_num)
                file_text += page_obj.extractText()
            pdf_file_obj.close()

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1024, chunk_overlap=64,
        )
        texts = text_splitter.split_text(file_text)
        for i, chunked_text in enumerate(texts):
            documents.append(Document(
                page_content=chunked_text,
                metadata={"doc_title": file.split(".")[0], "chunk_num": i}))
    return documents

def import_modules_from_dict_keys(elements, mapping_dict):
    imported_modules = []
    for element in elements:
        if element in mapping_dict:
            module_name, class_name = mapping_dict[element].split('.')
            module = importlib.import_module(f'autoredteam.metrics.{module_name}')
            metric_class = getattr(module, class_name)
            imported_modules.append(metric_class())
    return imported_modules


def main(arguments=[]):
    """Entry point for the application script"""
    from autoredteam import __version__, __description__

    _config.transient.starttime = datetime.now()
    _config.transient.starttime_iso = _config.transient.starttime.isoformat()
    _config.version = __version__
    _config.reporting.report_dir = "runs"

    start_logging()
    print(f"autoredteam {_config.version} at {_config.transient.starttime_iso}")
    parser = argparse.ArgumentParser(
        prog="python -m autoredteam",
        description=__description__,
        epilog="See https://vijil.ai for more information",
    )

    # add arguments
    parser.add_argument(
        "--model_type",
        "-m",
        type=str,
        help="module and optionally also class of the generator, e.g. 'huggingface', or 'openai'",
    )
    parser.add_argument(
        "--model_name",
        "-n",
        type=str,
        default=None,
        help="name of the model, e.g. 'timdettmers/guanaco-33b-merged'",
    )
    parser.add_argument(
        "--generations",
        "-g",
        type=int,
        default=10,
        help="number of generations to run.",
    )
    parser.add_argument(
        "--tests",
        "-t",
        type=str,
        default=None,
        help="list of test modules to run.",
    )
    parser.add_argument(
        "--dimensions",
        "-d",
        type=str,
        default=None,
        help="list of test dimensions to use.",
    )

    parser.add_argument(
        "--rag",
        "-r",
        type=bool,
        default=False,
        help="boolean flag to select rag.",
    )

    parser.add_argument(
        "--metrics",
        "-me",
        type=str,
        nargs='+',
        default=None,
        help="list of metrics to use, separated by space.",
    )

    parser.add_argument(
        "--documents_path",
        "-dp",
        type=str,
        default=None,
        help="path to the documents.",
    )

    # parse arguments
    logging.debug("args - raw argument string received: %s", arguments)
    args = parser.parse_args(arguments)
    logging.debug("args - full argparse: %s", args)

    # run
    start_run()

    # instantiate the agent class
    # if args.model_type in ["octo", "replicate", "anyscale", "together", "mistral"]:
    # else:
    #     agent_module = importlib.import_module(
    #         f"garak.generators.{args.model_type.split('.')[0]}"
    #     )

    if "." not in args.model_type:
        agent_module = importlib.import_module(f"autoredteam.agents.{args.model_type}")
        model_type = getattr(agent_module, agent_module.default_class)
    else:
        module_name, class_name = args.model_type.split(".")
        model_type = getattr(
            importlib.import_module(f"autoredteam.agents.{module_name}"), class_name
        )

    if args.model_type == "rest":
        rest_config = json.loads(open(args.model_name).read())
        agent_instance = model_type(config=rest_config)
    else:
        agent_instance = model_type(name=args.model_name)
    agent_instance.generations = args.generations
    agent_instance.seed = 42

    # instantiate the harnesses to run
    if args.metrics is not None and args.tests is None and args.dimensions is None:
        print("Only metrics supplied. Skipping all tests.")
    elif args.tests is not None:
        from autoredteam.harnesses.modulewise import ModuleHarness

        test_modules = args.tests.split(",")
        harness_instances = [
            ModuleHarness(agent=agent_instance, module=module)
            for module in test_modules
        ]
    elif args.dimensions is not None:
        test_dimensions = args.dimensions.split(",")
        harness_module = importlib.import_module(f"autoredteam.harnesses.dimension")
        with contextlib.redirect_stdout(None):
            harness_instances = [
                getattr(harness_module, dimension + "Harness")(agent=agent_instance)
                for dimension in test_dimensions
            ]
    else:
        from autoredteam.harnesses.modulewise import ModuleHarness
        from autoredteam.utils import list_all_tests

        with contextlib.redirect_stdout(None):
            test_modules = list(list_all_tests().keys())
            harness_instances = [
                ModuleHarness(agent=agent_instance, module=module)
                for module in test_modules
            ]

    if args.rag:
        agent_instance.generations = 1
        agent_instance.temperature = 0

        if args.documents_path is None:
            print("You need to specify the path to the documents when using rag.")
        else:
            documents = process_files(args.documents_path)
            
        if args.metrics is not None:
            all_metrics = [metric for sublist in TRUST_DICT_METRICS.values() for metric in sublist]
            metrics = [metric for metric in all_metrics if metric.split('.')[1].lower() in args.metrics]
        elif args.dimensions is not None:
            mets = {k.lower(): v for k, v in TRUST_DICT_METRICS.items()}
            metrics = mets.get(args.dimensions.lower())
        else:
            metrics = [metric for sublist in TRUST_DICT_METRICS.values() for metric in sublist]
        
        harness_instances.append(RAGHarness(agent=agent_instance, metrics=metrics, documents=documents))

    # For all other harnesses except the RAGHarness, use force_abstain to only look for abstainment in standard tests
    for harness in harness_instances:
        if not isinstance(harness, RAGHarness):
            harness.force_abstain()

    # log the configs
    config_dict = {
        "entry_type": "config",
        "model_type": args.model_type,
        "model_name": rest_config["name"]
        if args.model_type == "rest"
        else args.model_name,
        "generations": args.generations,
        "metrics": args.metrics
    }
    if args.tests is not None:
        config_dict["tests"] = args.tests
    elif args.dimensions is not None:
        config_dict["dimensions"] = args.dimensions
    else:
        config_dict["tests"] = test_modules
    _config.transient.reportfile.write(json.dumps(config_dict) + "\n")

    # run the harnesses
    for harness in harness_instances:
        harness.run(logged=True)

    end_run(agent_instance)
