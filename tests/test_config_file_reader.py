import os
import pytest

from punch import config_file_reader as cfr


@pytest.fixture
def semver_config_file_content():
    return """
__config_version__ = 1

# http://semver.org/
GLOBALS = {
    'serializer': '{major}.{minor}.{patch}'
}

FILES = [
    'pkg/__init__.py',
    {
        'path': 'version.txt',
        'serializer': '{major}.{minor}'
    }
]

VERSION = [
    {
        'name': 'major',
        'type': 'integer'
    },
    {
        'name': 'minor',
        'type': 'integer'
    },
    {
        'name': 'patch',
        'type': 'integer'
    }
]
"""


@pytest.fixture
def empty_file_content():
    return """
"""


@pytest.fixture
def version_file_content():
    return """
major = 1
minor = 5
patch = 0
"""


@pytest.fixture
def illegal_config_file_content():
    return """
__config_version__ = 2
"""


@pytest.fixture
def config_file_name():
    return 'punch_config.py'


@pytest.fixture
def version_file_name():
    return 'punch_version.py'


def write_file(dir, content, config_file_name):
    with open(os.path.join(dir, config_file_name), 'w') as f:
        f.write(content)


def test_read_empty_config_file(temp_empty_uninitialized_dir, empty_file_content, config_file_name,
                                version_file_content, version_file_name):
    write_file(temp_empty_uninitialized_dir, empty_file_content, config_file_name)
    write_file(temp_empty_uninitialized_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name),
                       os.path.join(temp_empty_uninitialized_dir, version_file_name))

    assert str(exc.value) == "Given config file is invalid: missing '__config_version__' variable"


def test_read_empty_version_file(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name,
                                 empty_file_content, version_file_name):
    write_file(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name)
    write_file(temp_empty_uninitialized_dir, empty_file_content, version_file_name)

    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name),
                       os.path.join(temp_empty_uninitialized_dir, version_file_name))

    assert str(exc.value) == "Given version file is invalid: missing 'major' variable"


def test_read_illegal_config_file(temp_empty_uninitialized_dir, illegal_config_file_content, config_file_name,
                                  version_file_content, version_file_name):
    write_file(temp_empty_uninitialized_dir, illegal_config_file_content, config_file_name)
    write_file(temp_empty_uninitialized_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name),
                       os.path.join(temp_empty_uninitialized_dir, version_file_name))

    assert str(exc.value) == "Unsupported configuration file version 2"

def test_read_plain_variables(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name,
                              version_file_content, version_file_name):
    write_file(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name)
    write_file(temp_empty_uninitialized_dir, version_file_content, version_file_name)

    cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name),
                        os.path.join(temp_empty_uninitialized_dir, version_file_name))

    assert cf.__config_version__ == 1


# def test_read_global_variables(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name,
#                                version_file_content, version_file_name):
#     write_file(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name)
#
#     cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name))
#
#     expected_dict = {
#         'serializer': '{major}.{minor}.{patch}'
#     }
#
#     assert cf.globals == expected_dict
#
#
# def test_read_version(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name,
#                       version_file_content, version_file_name):
#     write_file(temp_empty_uninitialized_dir, semver_config_file_content, config_file_name)
#
#     cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, config_file_name))
#
#     assert len(cf.version.parts) == 3

# def test_read_files(temp_empty_uninitialized_dir, semver_config_file_content):
#     write_config_file(temp_empty_uninitialized_dir, semver_config_file_content)
#
#     cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))
#
#     assert len(cf.files) == 2
