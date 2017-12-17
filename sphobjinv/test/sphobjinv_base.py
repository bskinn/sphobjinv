# ------------------------------------------------------------------------------
# Name:        sphobjinv_base
# Purpose:     Base module for sphobjinv tests
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2016-2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#            https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Base module for sphobjinv tests."""


from contextlib import contextmanager
from filecmp import cmp
import os
import os.path as osp
import shutil as sh
import sys
import unittest as ut


# Useful constants
RES_FNAME_BASE = 'objects_attrs'
INIT_FNAME_BASE = 'objects'
MOD_FNAME_BASE = 'objects_mod'
ENC_EXT = '.inv'
DEC_EXT = '.txt'
SOI_PATH = osp.abspath(osp.join('sphobjinv', 'sphobjinv.py'))
INVALID_FNAME = '*?*?.txt' if os.name == 'nt' else '/'
B_LINES_0 = {False:
             b'attr.Attribute py:class 1 api.html#$ -',
             True:
             b'attr.Attribute py:class 1 api.html#attr.Attribute '
             b'attr.Attribute'}
S_LINES_0 = {_: B_LINES_0[_].decode('utf-8') for _ in B_LINES_0}


# Useful functions
def res_path(fname=''):
    """Construct file path in resource dir from project root."""
    return osp.join('sphobjinv', 'test', 'resource', fname)


# Absolute path to the .txt file in `resource`
# This has to come after res_path is defined
RES_DECOMP_PATH = osp.abspath(res_path(RES_FNAME_BASE + DEC_EXT))


def scr_path(fname=''):
    """Construct file path in scratch dir from project root."""
    return osp.join('sphobjinv', 'test', 'scratch', fname)


def ensure_scratch():
    """Ensure the scratch folder exists."""
    if not osp.isdir(scr_path()):
        os.mkdir(scr_path())


def clear_scratch():
    """Clear the scratch folder."""
    for fn in os.listdir(scr_path()):
        if osp.isfile(scr_path(fn)):
            os.remove(scr_path(fn))


def copy_enc():
    """Copy the encoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + ENC_EXT),
            scr_path(INIT_FNAME_BASE + ENC_EXT))


def copy_dec():
    """Copy the decoded example file into scratch."""
    sh.copy(res_path(RES_FNAME_BASE + DEC_EXT),
            scr_path(INIT_FNAME_BASE + DEC_EXT))


def sphinx_load_test(testcase, path):
    """Perform 'live' Sphinx inventory load test."""
    # Easier to have the file open the whole time
    with open(path, 'rb') as f:

        # Have to handle it differently for Python 3.3 compared to the rest
        if sys.version_info.major == 3 and sys.version_info.minor < 4:
            from sphinx.ext.intersphinx import read_inventory_v2 as readfunc
            f.readline()    # read_inventory_v2 expects to start on 2nd line
        else:
            from sphinx.util.inventory import InventoryFile as IFile
            readfunc = IFile.load

        # Attempt the load operation
        try:
            readfunc(f, '', osp.join)
        except Exception:
            with testcase.subTest('sphinx_load_ok'):
                testcase.fail()


def run_cmdline_test(testcase, arglist, expect=0):
    """Perform command line test."""
    from sphobjinv.cmdline import main

    # Assemble execution arguments
    runargs = ['sphobjinv']
    list(map(runargs.append, arglist))

    # Mock sys.argv, run main, and restore sys.argv
    stored_sys_argv = sys.argv
    sys.argv = runargs
    try:
        main()
    except SystemExit as e:
        retcode = e.args[0]
    else:
        raise RuntimeError("SystemExit not raised on termination.")
    finally:
        sys.argv = stored_sys_argv

    # Test that execution completed w/o error
    with testcase.subTest('exit_code'):
        testcase.assertEquals(expect, retcode)


def file_exists_test(testcase, path):
    """Confirm indicated filespec exists."""
    with testcase.subTest('file_exists'):
        testcase.assertTrue(osp.isfile(path))


def decomp_cmp_test(testcase, path):
    """Confirm that indicated decoded file compares identical to resource."""
    with testcase.subTest('decomp_cmp'):
        testcase.assertTrue(cmp(RES_DECOMP_PATH, path, shallow=False))


@contextmanager
def dir_change(subdir):
    """Context manager to change to sub-directory & drop back on exit."""
    existed = osp.isdir(subdir)

    if not existed:
        os.mkdir(subdir)

    os.chdir(subdir)
    yield

    if not existed:
        list(map(os.remove, os.listdir()))

    os.chdir(os.pardir)

    if not existed:
        os.rmdir(subdir)


class SuperSphobjinv(object):
    """Superclass with common setup code for all tests."""

    @classmethod
    def setUpClass(cls):
        """Run the class-wide setup code."""
        # Make sure the scratch directory exists.
        ensure_scratch()

    def setUp(self):
        """Run the per-test-method setup code."""
        # Always want to clear the scratch?
        clear_scratch()


class TestSphobjinvAPIExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_API_SourceTypes_IterationCheck(self):
        """Confirm that SourceTypes iterates in the expected order."""
        import itertools as itt

        import sphobjinv as soi

        items = [soi.SourceTypes.Manual,
                 soi.SourceTypes.BytesPlaintext,
                 soi.SourceTypes.BytesZlib,
                 soi.SourceTypes.FnamePlaintext,
                 soi.SourceTypes.FnameZlib,
                 soi.SourceTypes.DictFlat
                 ]

        for it, en in itt.zip_longest(items, soi.SourceTypes, fillvalue=None):
            with self.subTest(en.value if en else it.value):
                self.assertEquals(it, en)

    def test_API_EncodeSucceeds(self):
        """Check that an encode attempt via API throws no errors."""
        import sphobjinv as soi

        # Populate scratch with the decoded ref file
        copy_dec()

        # Store dest filename for reuse
        dest_fname = scr_path(MOD_FNAME_BASE + ENC_EXT)

        # See if it makes it all the way through the process without error
        with self.subTest('error_in_process'):
            try:
                b_dec = soi.readfile(scr_path(INIT_FNAME_BASE + DEC_EXT))
                b_enc = soi.encode(b_dec)
                soi.writefile(dest_fname, b_enc)
            except Exception:
                self.fail(msg='objects.txt encoding failed.')

        # Simple assertion that encoded file now exists
        file_exists_test(self, dest_fname)

        # Seeing if sphinx actually likes the file
        sphinx_load_test(self, dest_fname)

    def test_API_DecodeSucceeds(self):
        """Check that a decode attempt via API throws no errors."""
        import sphobjinv as soi

        # Populate scratch with encoded ref file
        copy_enc()

        # Store target filename for reuse
        dest_fname = scr_path(MOD_FNAME_BASE + DEC_EXT)

        # See if the encode operation completes without error
        with self.subTest('error_in_process'):
            try:
                b_enc = soi.readfile(scr_path(INIT_FNAME_BASE + ENC_EXT))
                b_dec = soi.decode(b_enc)
                soi.writefile(dest_fname, b_dec)
            except Exception:
                self.fail(msg='objects.inv decoding failed.')

        # Simple assertion of the existence of the decoded file
        file_exists_test(self, dest_fname)

        # Testing compare w/original file
        decomp_cmp_test(self, dest_fname)

    def test_API_RegexDataCheck(self):
        """Confirm the regex for loading data lines is working properly."""
        import sphobjinv as soi

        # Populate scratch with the decoded file
        copy_dec()

        # Read the file
        b_str = soi.fileops.readfile(scr_path(INIT_FNAME_BASE + DEC_EXT))

        # Have to convert any DOS newlines
        b_str = b_str.replace(b'\r\n', b'\n')

        # A separate check shows 56 entries in the reference hive."""
        with self.subTest('entries_count'):
            self.assertEquals(56, len(soi.re.pb_data.findall(b_str)))

        # The first entry in the file is:
        #  attr.Attribute py:class 1 api.html#$ -
        # The third entry from the end is:
        #  slots std:label -1 examples.html#$ Slots
        elements = [0, -3]
        testdata = {soi.DataFields.Name: [b'attr.Attribute', b'slots'],
                    soi.DataFields.Domain: [b'py', b'std'],
                    soi.DataFields.Role: [b'class', b'label'],
                    soi.DataFields.Priority: [b'1', b'-1'],
                    soi.DataFields.URI: [b'api.html#$', b'examples.html#$'],
                    soi.DataFields.DispName: [b'-', b'Slots']}

        # Materialize the list of data line matches
        mchs = list(soi.re.pb_data.finditer(b_str))

        # Test each of the id-ed data lines
        for i, e in enumerate(elements):
            for df in soi.DataFields:
                with self.subTest('{0}_{1}'.format(df.value, e)):
                    self.assertEquals(mchs[e].group(df.value),
                                      testdata[df][i])

    def test_API_DataObjBytes_InitCheck(self):
        """Confirm the DataObjBytes type functions correctly."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode(encoding='utf-8')
                     for _ in b_mchdict}

        # Confirm DataObjBytes instantiates w/bytes
        with self.subTest('inst_bytes'):
            try:
                b_dob = soi.DataObjBytes(**b_mchdict)
            except Exception:
                self.fail('bytes instantiation failed')

        # Confirm DataObjBytes instantiates w/str
        with self.subTest('inst_str'):
            try:
                s_dob = soi.DataObjBytes(**s_mchdict)
            except Exception:
                self.fail('str instantiation failed')

        # Confirm members match
        for _ in b_mchdict:
            with self.subTest('match_' + _):
                self.assertEquals(getattr(b_dob, _),
                                  getattr(s_dob, _))

        # Confirm str-equivalents match
        for _ in b_mchdict:
            with self.subTest('str_equiv_' + _):
                self.assertEquals(getattr(b_dob, _),
                                  getattr(b_dob.as_str, _)
                                  .encode(encoding='utf-8'))

    def test_API_DataObjStr_InitCheck(self):
        """Confirm the DataObjStr type functions correctly."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode(encoding='utf-8')
                     for _ in b_mchdict}

        # Confirm DataObjStr instantiates w/bytes
        with self.subTest('inst_bytes'):
            try:
                b_dos = soi.DataObjStr(**b_mchdict)
            except Exception:
                self.fail('bytes instantiation failed')

        # Confirm DataObjStr instantiates w/str
        with self.subTest('inst_str'):
            try:
                s_dos = soi.DataObjStr(**s_mchdict)
            except Exception:
                self.fail('str instantiation failed')

        # Confirm members match
        for _ in s_mchdict:
            with self.subTest('match_' + _):
                self.assertEquals(getattr(b_dos, _),
                                  getattr(s_dos, _))

        # Confirm bytes-equivalents match
        for _ in s_mchdict:
            with self.subTest('str_equiv_' + _):
                self.assertEquals(getattr(s_dos, _),
                                  getattr(s_dos.as_bytes, _)
                                  .decode(encoding='utf-8'))

    def test_API_DataObjBytes_FlatDictFxn(self):
        """Confirm that flat dict generating function works."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)

        # Extract the match information, stuff into a DataObjBytes
        # instance, and extract the flat_dict
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        b_flatdict = soi.DataObjBytes(**b_mchdict).flat_dict()

        # Check matchingness
        for _ in b_mchdict:
            with self.subTest(_):
                self.assertEquals(b_mchdict[_], b_flatdict[_])

    def test_API_DataObjStr_FlatDictFxn(self):
        """Confirm that flat dict generating function works."""
        import sphobjinv as soi

        # Pull .txt file and match first data line
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)

        # Extract the match information, stuff into a DataObjStr
        # instance, and extract the flat_dict
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_flatdict = soi.DataObjStr(**b_mchdict).flat_dict()

        # Check matchingness
        for _ in b_mchdict:
            with self.subTest(_):
                self.assertEquals(b_mchdict[_].decode(encoding='utf-8'),
                                  s_flatdict[_])

    def test_API_DataObjBytes_StructDictFxn(self):
        """Confirm that structured dict updating function works."""
        import sphobjinv as soi
        from sphobjinv import DataFields as DF

        # Pull .txt file and retrieve all matches
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mchs = list(soi.pb_data.finditer(b_dec))
        # mchs = mchs[:3] + mchs[-2:]

        # Extract each match's information, stuff into a DataObjBytes
        # instance, and update a new dict with the structured
        # data
        newdict = {}
        b_mchdicts = []
        for mch in mchs:
            b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
            b_mchdicts.append(b_mchdict)
            soi.DataObjBytes(**b_mchdict).update_struct_dict(newdict)

        # Run through all the matches and confirm all is consistent
        for i, b_mchdict in enumerate(b_mchdicts):
            s_i = str(i)

            # Check top-level is domain
            with self.subTest('domain_' + s_i):
                self.assertIn(b_mchdict[DF.Domain.value], newdict.keys())

            # Check next level is role
            subdict = newdict[b_mchdict[DF.Domain.value]]
            with self.subTest('role_' + s_i):
                self.assertIn(b_mchdict[DF.Role.value], subdict.keys())

            # Check next level is name
            subdict = subdict[b_mchdict[DF.Role.value]]
            with self.subTest('name_' + s_i):
                self.assertIn(b_mchdict[DF.Name.value], subdict.keys())

            # Check priority, URI and dispname
            subdict = subdict[b_mchdict[DF.Name.value]]
            for _ in [DF.Priority.value, DF.URI.value, DF.DispName.value]:
                with self.subTest(_ + '_' + s_i):
                    # Assert key found
                    self.assertIn(_, subdict.keys())

                    # Assert value match
                    self.assertEquals(subdict[_], b_mchdict[_])

    def test_API_DataObjStr_StructDictFxn(self):
        """Confirm that structured dict updating function works."""
        import sphobjinv as soi
        from sphobjinv import DataFields as DF

        # Pull .txt file and match first data line
        b_dec = soi.readfile(res_path(RES_FNAME_BASE + DEC_EXT))
        mch = soi.pb_data.search(b_dec)

        # Extract the match information, convert to str,
        # stuff into a DataObjBytes instance,
        # and update a new dict with the structured data
        b_mchdict = {_: mch.group(_) for _ in mch.groupdict()}
        s_mchdict = {_: b_mchdict[_].decode('utf-8') for _ in b_mchdict}
        newdict = {}
        soi.DataObjStr(**s_mchdict).update_struct_dict(newdict)

        # Check top-level is domain
        with self.subTest('domain'):
            self.assertEquals(list(newdict.keys())[0],
                              s_mchdict[DF.Domain.value])

        # Check next level is role
        subdict = newdict[s_mchdict[DF.Domain.value]]
        with self.subTest('role'):
            self.assertEquals(list(subdict.keys())[0],
                              s_mchdict[DF.Role.value])

        # Check next level is name
        subdict = subdict[s_mchdict[DF.Role.value]]
        with self.subTest('name'):
            self.assertEquals(list(subdict.keys())[0],
                              s_mchdict[DF.Name.value])

        # Check priority, URI and dispname
        subdict = subdict[s_mchdict[DF.Name.value]]
        for _ in [DF.Priority.value, DF.URI.value, DF.DispName.value]:
            with self.subTest(_):
                # Assert key found
                self.assertIn(_, subdict.keys())

                # Assert value match
                self.assertEquals(subdict[_], s_mchdict[_])

    # These methods testing data_line also implicitly test flat_dict
    def test_API_DataObjBytes_DataLineFxn(self):
        """Confirm that data line formatting function works."""
        from itertools import product

        import sphobjinv as soi

        # Generate and check data line as bytes, both expanded
        # and contracted, with both expanded/contracted flag
        for _, __ in product(B_LINES_0, repeat=2):  # True/False product
            dob = soi.DataObjBytes(**soi.pb_data.search(B_LINES_0[_])
                                   .groupdict())
            b_dl = dob.data_line(expand=__)
            with self.subTest(str(_) + '_expand_' + str(__)):
                self.assertEquals(b_dl, B_LINES_0[_ or __])

            b_dl = dob.data_line(contract=__)
            with self.subTest(str(_) + '_contract_' + str(__)):
                self.assertEquals(b_dl, B_LINES_0[_ and not __])

    def test_API_DataObjStr_DataLineFxn(self):
        """Confirm that data line formatting function works."""
        from itertools import product

        import sphobjinv as soi

        # Generate and check data line as str, both expanded
        # and contracted, with both expanded/contracted flag
        for _, __ in product(S_LINES_0, repeat=2):  # True/False product
            dos = soi.DataObjStr(**soi.p_data.search(S_LINES_0[_])
                                 .groupdict())
            s_dl = dos.data_line(expand=__)
            with self.subTest(str(_) + '_expand_' + str(__)):
                self.assertEquals(s_dl, S_LINES_0[_ or __])


class TestSphobjinvAPIInventoryExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing Inventory code accuracy w/good params & expected behavior."""

    def test_API_Inventory_DefaultNoneInstantiation(self):
        """Confirm 'manual' instantiation with None."""
        import sphobjinv as soi

        inv = soi.Inventory()

        with self.subTest('project'):
            self.assertEquals(inv.project, None)

        with self.subTest('version'):
            self.assertEquals(inv.version, None)

        with self.subTest('count'):
            self.assertEquals(inv.count, 0)

        with self.subTest('source_type'):
            self.assertEquals(inv.source_type, soi.SourceTypes.Manual)

    def check_attrs_inventory(self, inv, st):
        """Encapsulate high-level consistency tests for Inventory objects."""
        with self.subTest('{0}_project'.format(st.value)):
            self.assertEquals(inv.project, 'attrs')

        with self.subTest('{0}_version'.format(st.value)):
            self.assertEquals(inv.version, '17.2')

        with self.subTest('{0}_count'.format(st.value)):
            self.assertEquals(inv.count, 56)

        with self.subTest('{0}_source_type'.format(st.value)):
            self.assertEquals(inv.source_type, st)

    def test_API_Inventory_OverallImport(self):
        """Check all high-level modes for Inventory instantiation."""
        from sphobjinv import readfile, Inventory as Inv, SourceTypes as ST

        sources = {ST.BytesPlaintext:
                   readfile(res_path(RES_FNAME_BASE + DEC_EXT)),
                   ST.BytesZlib:
                   readfile(res_path(RES_FNAME_BASE + ENC_EXT)),
                   ST.FnamePlaintext:
                   res_path(RES_FNAME_BASE + DEC_EXT),
                   ST.FnameZlib:
                   res_path(RES_FNAME_BASE + ENC_EXT),
                   }

        for st in ST:
            if st in [ST.Manual, ST.DictFlat]:
                # Manual isn't tested
                # DictFlat is tested independently, to avoid crashing this
                #  test if something goes wrong in the generation & reimport
                continue

            self.check_attrs_inventory(Inv(sources[st]), st)

    def test_API_Inventory_FlatDictJSONValidate(self):
        """Confirm that the flat_dict properties generated valid JSON."""
        import jsonschema

        import sphobjinv as soi
        import sphobjinv.schema as soi_schema

        inv = soi.Inventory(res_path(RES_FNAME_BASE + ENC_EXT))
        v = jsonschema.Draft4Validator(soi_schema.schema_flat)

        for prop in ['flat_dict', 'flat_dict_expanded',
                     'flat_dict_contracted']:
            with self.subTest(prop):
                try:
                    v.validate(getattr(inv, prop))
                except jsonschema.ValidationError:
                    self.fail("'{0}' JSON invalid".format(prop))

    def test_API_Inventory_FlatDictReimport(self):
        """Confirm re-import of a generated flat_dict."""
        from sphobjinv import Inventory, SourceTypes

        inv = Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        inv = Inventory(inv.flat_dict)

        self.check_attrs_inventory(inv, SourceTypes.DictFlat)

    def test_API_Inventory_NameSuggest(self):
        """Confirm object name suggestion is nominally working."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + ENC_EXT))

        rec = inv.suggest('evolve')

        self.assertEquals(rec[0][0], ':py:function:`attr.evolve`')

    def test_API_FuzzyWuzzy_WarningIdentity(self):
        """Confirm only the Levenshtein warning is raised, if any are."""
        import warnings

        with warnings.catch_warnings(record=True) as wc:
            warnings.simplefilter("always")
            from fuzzywuzzy import process

        with self.subTest('has_extract'):
            try:
                # Don't call it, just retrieve it
                # This is mainly to stop flake8 from complaining
                process.extract
            except NameError:
                self.fail("fuzzywuzzy.process oddly has no 'extract' member")

        # Try to import, and adjust tests accordingly
        try:
            import Levenshtein
            Levenshtein.__doc__  # Stop flake8 complaint
        except ImportError:
            lev_present = False
        else:
            lev_present = True

        if lev_present:
            with self.subTest('count_Lev_present'):  # pragma: no cover
                self.assertEquals(len(wc), 0)

        else:
            with self.subTest('count_Lev_absent'):
                self.assertEquals(len(wc), 1)

            with self.subTest('identity_Lev_absent'):
                # 'message' will be a Warning instance, thus 'args[0]'
                # to retrieve the warning message as str.
                self.assertIn('levenshtein', wc[0].message.args[0].lower())


class TestSphobjinvCmdlineExpectGood(SuperSphobjinv, ut.TestCase):
    """Testing code accuracy under good params & expected behavior."""

    def test_CmdlineDecodeNoArgs(self):
        """Confirm commandline decode exec with no args succeeds."""
        copy_enc()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['decode'])

                    file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                    decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineEncodeNoArgs(self):
        """Confirm commandline encode exec with no args succeeds."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['encode'])

                    file_exists_test(self, INIT_FNAME_BASE + ENC_EXT)

                    sphinx_load_test(self, INIT_FNAME_BASE + ENC_EXT)

    def test_CmdlineDecodeSrcFile(self):
        """Confirm cmdline decode with input file arg."""
        copy_enc()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['decode',
                                scr_path(INIT_FNAME_BASE + ENC_EXT)])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeSrcFile(self):
        """Confirm cmdline encode with input file arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + ENC_EXT)
        run_cmdline_test(self, ['encode',
                                scr_path(INIT_FNAME_BASE + DEC_EXT)])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeSrcPath(self):
        """Confirm cmdline decode with input directory arg."""
        copy_enc()
        dest_path = scr_path(INIT_FNAME_BASE + DEC_EXT)
        run_cmdline_test(self, ['decode', scr_path()])

        file_exists_test(self, dest_path)

        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeSrcPath(self):
        """Confirm cmdline encode with input directory arg."""
        copy_dec()
        dest_path = scr_path(INIT_FNAME_BASE + ENC_EXT)
        run_cmdline_test(self, ['encode', scr_path()])

        file_exists_test(self, dest_path)

        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeTgtNewName(self):
        """Confirm cmdline decode to custom target name in same dir."""
        copy_enc()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['decode', '-', dest_fname])

                    file_exists_test(self, dest_fname)

                    decomp_cmp_test(self, dest_fname)

    def test_CmdlineEncodeTgtNewName(self):
        """Confirm cmdline encode to custom target name in same dir."""
        copy_dec()
        dest_fname = MOD_FNAME_BASE + ENC_EXT
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    run_cmdline_test(self, ['encode', '.', dest_fname])

                    file_exists_test(self, dest_fname)

                    sphinx_load_test(self, dest_fname)

    def test_CmdlineDecodeDiffSrcPathNewNameThere(self):
        """Confirm decode in other path outputs there if only name passed."""
        copy_enc()
        dest_fname = MOD_FNAME_BASE + DEC_EXT
        run_cmdline_test(self, ['decode', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        decomp_cmp_test(self, scr_path(dest_fname))

    def test_CmdlineEncodeDiffSrcPathNewNameThere(self):
        """Confirm encode in other path outputs there if only name passed."""
        copy_dec()
        dest_fname = MOD_FNAME_BASE + ENC_EXT
        run_cmdline_test(self, ['encode', scr_path(), dest_fname])

        file_exists_test(self, scr_path(dest_fname))

        sphinx_load_test(self, scr_path(dest_fname))

    def test_CmdlineDecodeDiffSrcTgtPaths(self):
        """Confirm decode from other path to new path."""
        copy_enc()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + DEC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decode', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        decomp_cmp_test(self, dest_path)

    def test_CmdlineEncodeDiffSrcTgtPaths(self):
        """Confirm encode from other path to new path."""
        copy_dec()
        dest_path = osp.join(os.curdir, MOD_FNAME_BASE + ENC_EXT)
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['encode', os.pardir, dest_path])

                        file_exists_test(self, dest_path)

                        sphinx_load_test(self, dest_path)

    def test_CmdlineDecodeTgtBarePath(self):
        """Confirm decode to target as bare path."""
        copy_enc()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['decode', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + DEC_EXT)

                        decomp_cmp_test(self, INIT_FNAME_BASE + DEC_EXT)

    def test_CmdlineEncodeTgtBarePath(self):
        """Confirm encode to target as bare path."""
        copy_dec()
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    with dir_change('tempy'):
                        run_cmdline_test(self,
                                         ['encode', os.pardir, '.'])

                        file_exists_test(self, INIT_FNAME_BASE + ENC_EXT)

                        sphinx_load_test(self, INIT_FNAME_BASE + ENC_EXT)


class TestSphobjinvAPIExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_APINoInputFile(self):
        """Confirm that appropriate exceptions are raised w/no input file."""
        import sphobjinv as soi

        with self.subTest('decoded_input_file'):
            with self.assertRaises(FileNotFoundError):
                soi.readfile(INIT_FNAME_BASE + DEC_EXT)

        with self.subTest('encoded_input_file'):
            with self.assertRaises(FileNotFoundError):
                soi.readfile(INIT_FNAME_BASE + ENC_EXT)

    def test_APIBadOutputFile(self):
        """Confirm OSError raised on bad filename (example of read error)."""
        import sphobjinv as soi

        b_str = b'This is a binary string!'

        with self.assertRaises(OSError):
            soi.writefile(INVALID_FNAME, b_str)

    def test_APIBadDataObjInitTypes(self):
        """Confirm error raised when init-ed w/wrong types."""
        import sphobjinv as soi

        with self.subTest('bytes'):
            with self.assertRaises(TypeError):
                soi.DataObjBytes(*range(6))

        with self.subTest('str'):
            with self.assertRaises(TypeError):
                soi.DataObjStr(*range(6))

    def test_API_DataLine_BothArgsTrue(self):
        """Confirm error raised when both expand and contract are True."""
        import sphobjinv as soi

        dos = soi.DataObjStr(**soi.p_data.search(S_LINES_0[True])
                             .groupdict())
        with self.assertRaises(ValueError):
            dos.data_line(expand=True, contract=True)

    def test_API_Inventory_InvalidSource(self):
        """Confirm error raised when invalid source provided."""
        import sphobjinv as soi

        with self.assertRaises(TypeError):
            soi.Inventory('abcdefg')

    def test_API_Inventory_TooSmallFlatDictImport(self):
        """Confirm error raised when flat dict passed w/too few objects."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.flat_dict
        d.pop('12')

        self.assertRaises(ValueError, soi.Inventory, d)

    def test_API_Inventory_TooBigFlatDictImport(self):
        """Confirm error raised when flat dict passed w/too many objects."""
        import sphobjinv as soi

        inv = soi.Inventory(res_path(RES_FNAME_BASE + DEC_EXT))
        d = inv.flat_dict
        d.update({'112': 'foobarbazquux'})

        self.assertRaises(ValueError, soi.Inventory, d)


class TestSphobjinvCmdlineExpectFail(SuperSphobjinv, ut.TestCase):
    """Testing that code raises expected errors when invoked improperly."""

    def test_CmdlineDecodeWrongFileType(self):
        """Confirm exit code 1 with invalid file format."""
        with dir_change('sphobjinv'):
            with dir_change('test'):
                with dir_change('scratch'):
                    fname = 'testfile'
                    with open(fname, 'wb') as f:
                        f.write(b'this is not objects.inv\n')

                    run_cmdline_test(self,
                                     ['decode', fname],
                                     expect=1)

    def test_CmdlineDecodeMissingFile(self):
        """Confirm exit code 1 with nonexistent file specified."""
        run_cmdline_test(self, ['decode', 'thisfileshouldbeabsent.txt'],
                         expect=1)

    def test_CmdlineDecodeBadOutputFilename(self):
        """Confirm exit code 1 with invalid output file name."""
        copy_enc()
        run_cmdline_test(self,
                         ['decode',
                          scr_path(INIT_FNAME_BASE + ENC_EXT),
                          INVALID_FNAME],
                         expect=1)


def suite_cli_expect_good():
    """Create and return the test suite for CLI expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectGood)])

    return s


def suite_api_expect_good():
    """Create and return the test suite for API expect-good cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvAPIExpectGood),
                tl.loadTestsFromTestCase(TestSphobjinvAPIInventoryExpectGood)])

    return s


def suite_cli_expect_fail():
    """Create and return the test suite for CLI expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvCmdlineExpectFail)])

    return s


def suite_api_expect_fail():
    """Create and return the test suite for API expect-fail cases."""
    s = ut.TestSuite()
    tl = ut.TestLoader()
    s.addTests([tl.loadTestsFromTestCase(TestSphobjinvAPIExpectFail)])

    return s


if __name__ == '__main__':
    print("Module not executable.")
