import pytest


# st = subtest; mt = main test



@pytest.mark.parametrize('st_2', [True, False], ids=(lambda v: f'st2_{v}'))
@pytest.mark.parametrize('st_1', [True, False], ids=(lambda v: f'st1_{v}'))
def test_two_st_no_mt(st_1, st_2, subtests):
    with subtests.test(msg="subtest1"):
        assert st_1
    with subtests.test(msg="subtest2"):
        assert st_2


@pytest.mark.parametrize('mt', [True, False], ids=(lambda v: f'mt_{v}'))
@pytest.mark.parametrize('st_2', [True, False], ids=(lambda v: f'st2_{v}'))
@pytest.mark.parametrize('st_1', [True, False], ids=(lambda v: f'st1_{v}'))
def test_two_st_one_mt(st_1, st_2, mt, subtests):
    with subtests.test(msg="subtest1"):
        assert st_1
    with subtests.test(msg="subtest2"):
        assert st_2

    assert mt


@pytest.mark.parametrize('st_2', [True, False], ids=(lambda v: f'st2_{v}'))
@pytest.mark.parametrize('st_1', [True, False], ids=(lambda v: f'st1_{v}'))
@pytest.mark.xfail(reason="Testing xfail")
def test_two_st_no_mt_xfail(st_1, st_2, subtests):
    with subtests.test(msg="subtest1"):
        assert st_1
    with subtests.test(msg="subtest2"):
        assert st_2


@pytest.mark.parametrize('mt', [True, False], ids=(lambda v: f'mt_{v}'))
@pytest.mark.parametrize('st_2', [True, False], ids=(lambda v: f'st2_{v}'))
@pytest.mark.parametrize('st_1', [True, False], ids=(lambda v: f'st1_{v}'))
@pytest.mark.xfail(reason="Testing xfail")
def test_two_st_one_mt_xfail(st_1, st_2, mt, subtests):
    with subtests.test(msg="subtest1"):
        assert st_1
    with subtests.test(msg="subtest2"):
        assert st_2

    assert mt


@pytest.mark.xfail(reason="Testing XPASS")
def test_xpass():
    assert True
