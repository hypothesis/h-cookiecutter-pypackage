import os
import subprocess


class TestBuildFunctions:
    def run_command(self, command, cwd, env=None):
        try:
            kwargs = {"cwd": cwd}
            if env:
                copy_env = os.environ.copy()
                copy_env.update(env)
                kwargs["env"] = copy_env

            results = subprocess.check_output(command, **kwargs)

            return True, results

        except subprocess.CalledProcessError as e:  # pragma: no cover
            return False, e.output

    def assert_run_command_ok(self, command, cwd, env=None):
        ok, results = self.run_command(command, cwd, env)
        assert ok

        return results

    def test_build(self, existing_project):
        # The build here takes a while, so we'll perform many tests on the
        # output instead of having more conventional unit tests
        results = self.assert_run_command_ok(
            ["python", "setup.py", "sdist"],
            cwd=existing_project,
            env={"BUILD": "1234.5678"},
        )

        # This is the last step in the build
        assert "removing 'h_test_lib-1.0.1234.5678'" in results.decode("utf-8")
        expected_artifact = "h_test_lib-1.0.1234.5678.tar.gz"

        assert expected_artifact in os.listdir(os.path.join(existing_project, "dist"))

        # Check the artifact is ok by twine
        self.assert_run_command_ok(
            ["twine", "check", f"dist/{expected_artifact}"], cwd=existing_project
        )
