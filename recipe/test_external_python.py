"""Test that the link from C back to Python works.
"""

import lal
import lalsimulation
import pytest


def test_external_python(capsys):
    """Test that the embedded python responds.
    """
    params = lal.CreateDict()
    lal.DictInsertStringValue(params, "module", 'myrandom_module')
    lal.DictInsertStringValue(params, "object", 'random_object')

    # this call will fail because myrandom_module isn't a real thing
    with pytest.raises(RuntimeError):
        lalsimulation.SimInspiralChooseGenerator(
            lalsimulation.ExternalPython,
            params,
        )

    # the important thing is that the embedded python responded with
    # the appropriate error, rather than liblalsimulation.so failing
    # to load the embedded python in the first place.
    out, err = capsys.readouterr()
    assert "ModuleNotFoundError: No module named 'myrandom_module'" in err
