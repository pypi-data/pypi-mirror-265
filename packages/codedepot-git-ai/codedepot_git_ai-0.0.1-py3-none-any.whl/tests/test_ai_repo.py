from io import TextIOWrapper
from pathlib import Path
import os
import json
import subprocess
import signal
import time
from git_ai.metrics.experiment import Experiment
from tests.utils.ai_repo_read import AIRepoRead
from tests.utils.data_gen import ExperimentDataGen, RepositoryDataGen
from tests.utils.setup_repo import SetupRepo
from git_ai.cmd.ai_repo import AIRepo
import pygit2


class TestAIRepo:
    def run_experiment(self, exp_data: ExperimentDataGen, last_commit: bool):
        with Experiment(exp_data.name) as exp:
            before_metrics = exp_data.get_before_metrics()
            exp.writer.add_hparams(
                metric_dict={
                    m.label: m.value for m in before_metrics
                },
                hparam_dict={},
                metric_unit_dict={
                    m.label: m.unit for m in before_metrics
                })
            exp.checkpoint("experiment start")
            for idx,  epoch in enumerate(exp_data.epochs_generator()):
                for label, value in epoch:
                    exp.writer.add_scalar(
                        tag=label, scalar_value=value)
                exp.checkpoint("epoch %d" % idx)
            after_metrics = exp_data.get_after_metrics()
            exp.writer.add_hparams(
                metric_dict={
                    m.label: m.value for m in after_metrics
                },
                hparam_dict={},
                metric_unit_dict={
                    m.label: m.unit for m in after_metrics
                })
            if last_commit:
                exp.checkpoint("final checkpoint")

    def run_experiments(self, data: RepositoryDataGen, last_commit: bool):
        for exp_data in data:
            self.run_experiment(exp_data, last_commit)

    def test_creation(self, tmp_path):
        with SetupRepo(tmp_path, "test") as handles:
            copy, _, _ = handles
            ai_repo = AIRepo(copy.workdir)
            ai_repo.init_ai_repo()

            assert os.path.isdir(Path(copy.workdir) / ai_repo.GIT_AI_ROOT)
            assert os.path.isdir(Path(copy.workdir) / ai_repo.METRICS_PATH)
            assert os.path.isfile(Path(copy.workdir) / ai_repo.CONFIG_PATH)
            with open(Path(copy.workdir) / ai_repo.CONFIG_PATH) as f:
                config = json.load(f)
                assert config['ai_repo']

    def test_experiment_new_repository(self, tmp_path):
        data = RepositoryDataGen.default()
        with SetupRepo(Path(tmp_path), "test") as handles:
            copy, _, _ = handles
            repo_read = AIRepoRead(copy)
            ai_repo = AIRepo(copy.workdir)
            ai_repo.init_ai_repo()
            self.run_experiments(data, last_commit=True)
            for e in repo_read.get_experiments():
                data.match_data(e, repo_read.get_metrics(e),
                                repo_read.get_plots(e))

    def test_experiment_no_last_commit(self, tmp_path):
        data = RepositoryDataGen.default(experiment_count=2)
        with SetupRepo(Path(tmp_path), "test") as handles:
            copy, _, _ = handles
            repo_read = AIRepoRead(copy)
            ai_repo = AIRepo(copy.workdir)
            ai_repo.init_ai_repo()
            self.run_experiments(data, last_commit=False)
            for e in repo_read.get_experiments():
                data.match_data(e, repo_read.get_metrics(e),
                                repo_read.get_plots(e))

    def test_experiment_dirty_repository(self, tmp_path):
        data = RepositoryDataGen.default(experiment_count=1)
        with SetupRepo(Path(tmp_path), "test") as handles:
            copy, _, repo = handles
            # Add single file and commit

            def create_file(f: TextIOWrapper):
                f.write("test1 \n")
            repo.change_file(create_file, commit=True)

            # Modify the file
            def modify_file(f: TextIOWrapper):
                f.write("test2 \n")
            repo.change_file(modify_file, commit=False)
            ai_repo = AIRepo(copy.workdir)
            ai_repo.init_ai_repo()

            # Run a few experiments
            repo_read = AIRepoRead(copy)
            self.run_experiments(data, last_commit=False)
            for e in repo_read.get_experiments():
                data.match_data(e, repo_read.get_metrics(e),
                                repo_read.get_plots(e))

            commit_oid = copy.branches["exp/exp000"].target
            commit = copy.get(commit_oid)
            new_file = commit.tree / repo.new_file_relative_path   # type: ignore
            assert new_file.data == b'test2 \n'

    def test_merge_experiment(self, tmp_path):
        data = RepositoryDataGen.default()
        with SetupRepo(Path(tmp_path), "test") as handles:
            copy, _, repo = handles
            repo_read = AIRepoRead(copy)
            ai_repo = AIRepo(copy.workdir)
            ai_repo.init_ai_repo()

            def write_file(f: TextIOWrapper):
                f.write("first write")

            repo.change_file(write_file, commit=True)
            for exp_idx, exp_data in enumerate(data):
                def update_file(f: TextIOWrapper):
                    f.write("write number %d" % exp_idx)
                repo.change_file(update_file, commit=True)
                self.run_experiment(exp_data, last_commit=True)

            for e in repo_read.get_experiments():
                data.match_data(e, repo_read.get_metrics(e),
                                repo_read.get_plots(e))

            ai_repo.merge_experiment("exp003", "")

            oid = ai_repo.head.target
            data.match_data('exp003', repo_read.get_metrics(data_commit=oid),
                            repo_read.get_plots(data_commit=oid))

            ai_repo.merge_experiment("exp001", "")

            oid = ai_repo.head.target
            data.match_data('exp001', repo_read.get_metrics(data_commit=oid),
                            repo_read.get_plots(data_commit=oid))

    def test_commands_away_from_root(self):
        assert True == True

    def test_recursive_log(self, tmp_path):
        parent_data = RepositoryDataGen.default()
        child_data = RepositoryDataGen.default()
        with SetupRepo(Path(tmp_path), "test_parent") as parent_handles:
            parent_copy, _, parent_repo = parent_handles
            parent_ai_repo = AIRepo(parent_copy.workdir)
            parent_ai_repo.init_ai_repo()

            with SetupRepo(Path(tmp_path), "test_child") as child_handles:
                child_copy, child_bare, child_repo = child_handles
                child_ai_repo = AIRepo(child_copy.workdir)
                child_ai_repo.init_ai_repo()

                # Run experiments in the child.
                self.run_experiments(child_data, last_commit=True)
                # Merge 3 experiments in the child. Save commits.
                child_ai_repo.merge_experiment("exp000", "")
                child_commit_1 = child_copy.get(child_copy.head.target)
                child_ai_repo.merge_experiment("exp001", "")
                child_ai_repo.merge_experiment("exp002", "")
                child_commit_2 = child_copy.get(child_copy.head.target)
                child_ai_repo.remotes['origin'].push(["+refs/heads/master"])

                # Merge experiment in the parent
                os.chdir(parent_copy.workdir)
                submodule_path = Path('input_repo_test')
                # gets the absolute path of the child repo
                child_repo_path = Path(child_copy.workdir).resolve()
                input_url = 'file://%s' % child_repo_path
                for exp_idx, exp_data in enumerate(parent_data):
                    self.run_experiment(exp_data, last_commit=True)
                    if exp_idx == 2:
                        # Add submodule pointing to first experiment in the child
                        parent_ai_repo.add_input_repo(submodule_path,
                                                      input_url, child_commit_1.hex)
                        sub = parent_ai_repo.lookup_submodule(submodule_path)
                        sub_repo = pygit2.Repository(sub.path)
                        # Check if right commit is in input repo
                        assert str(child_commit_1.hex) == str(
                            sub_repo.head.target)

                    if exp_idx == 3:
                        # Merge an experiment dependent on the input repo
                        parent_ai_repo.merge_experiment("exp003", "")
                        # Update submodule pointing head in the child
                        parent_ai_repo.update_input_repo(
                            submodule_path, commit_spec=child_commit_2.hex)
                        sub = parent_ai_repo.lookup_submodule(submodule_path)
                        assert str(child_commit_2.hex) == str(sub.head_id)

                    if exp_idx == 4:
                        # Merge another experiment in the parent with a new commit
                        parent_ai_repo.merge_experiment("exp004", "")

                # Check if right commit is in input repo
                # Generate log
                log = parent_ai_repo.get_log().serialize_log()
                assert 'exp004' in log[0]
                assert 'Updating input repo input_repo_test' in log[1]
                assert str(child_commit_2.hex) in log[1]
                assert 'input_repo_test' == log[2]
                assert 'exp002' in log[3]
                assert 'exp001' in log[4]
                assert 'exp003' in log[5]
                assert 'Adding input repo input_repo_test' in log[6]
                assert 'input_repo_test' == log[7]
                assert 'exp000' in log[8]

    def test_interrupted_experiment(self, tmp_path):
        """Starts an experiment on a different thread and interrupts it. 
        Then it checks if the repository is back in the main branch whitout any
        changes.
        """
        test_root_path = tmp_path
        p = subprocess.Popen(
            ["python3", "tests/utils/interuptable_test.py", str(test_root_path)], preexec_fn=os.setsid)
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL
        time.sleep(10)
        for _ in range(20):
            p.send_signal(signal.SIGTERM)
        p.wait(timeout=10)

        repo = AIRepo(test_root_path / "interruptable" / "copy")
        # print the current branch of the repo
        assert repo.head.name == "refs/heads/master"
        assert not repo.status()
