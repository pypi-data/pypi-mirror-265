import unittest
import sys

from pydicom import dcmread

import tempfile
import os
from glob import glob
from shutil import rmtree
from os.path import join, dirname, abspath
from subprocess import check_output, check_call, STDOUT, DEVNULL
from time import sleep

from requests.exceptions import HTTPError

# There will be four lots of images on the server, the first two 3 each
PATID = 'PQA20160906RHD'
STUDYUID = '1.3.12.2.1107.5.2.19.45064.30000016090616040707700000004'
SERIESUID = '1.3.12.2.1107.5.2.19.45064.2016090617560117683773517.0.0.0'
IMAGEUID = '1.3.12.2.1107.5.2.19.45064.2016090617561210676173525'
NIMAGES = 3
INSTANCENUMBER = 1

PATID_B = 'QQA20180418BCHSKYRA'
STUDYUID_B = '1.3.12.2.1107.5.2.19.45622.30000018041807565753300000009'
SERIESUID_B = '1.3.12.2.1107.5.2.19.45622.201804181719501256341027.0.0.0'
IMAGEUID_B = '1.3.12.2.1107.5.2.19.45622.2018041817195878456941032'

# This is a very old philips with dicom bugs
PATID_C = 'PQA20171120Cossham2'
STUDYUID_C = '1.3.46.670589.11.18637.5.0.32660.2017112014111159010'
SERIESUID_C = '1.3.46.670589.11.18637.5.0.5868.2017112015112178610'
IMAGEUID_C = '1.3.46.670589.11.18637.5.0.5868.2017112015133617622'
NIMAGES_C = 1
INSTANCENUMBER_C = 1

# This is a philips exam card with lots of missing and dubious fields
PATID_D = 'QQA20180927NBTMR12'
STUDYUID_D = '1.3.46.670589.11.42358.5.0.8760.2018092713045083003'
SERIESUID_D = '1.3.46.670589.11.42358.5.0.1488.2018092713051884004'
IMAGEUID_D = '1.3.46.670589.11.42358.5.24.5.1.1488.2018092713051884004'
NIMAGES_D = 1
INSTANCENUMBER_D = 1


TESTDIR = dirname(abspath(__file__))
sys.path.insert(0, abspath(join(TESTDIR, '..')))
TESTDATA = join(TESTDIR, 'testdata')

# nb: we want dcm4chee3 tool not dcmtk program of same name
os.environ['PATH'] = os.pathsep.join([TESTDIR] + os.environ['PATH'].split(os.pathsep))

from dcmfetch.dicomweb import (
    rst_pat_level_find,
    rst_stu_level_find,
    rst_ser_level_find,
    rst_img_level_find,
    rst_ser_level_get,
    rst_img_level_get
)

DCKPROG = 'docker'
DCKARGS = ['run', '-d', '-p', '5242:4242', '-p', '9042:8042', 'jodogne/orthanc-plugins']

SCUPROG = join(TESTDIR, 'storescu.exe' if os.name == 'nt' else 'storescu')
SCUARGS = ['-c', 'Orthanc@localhost:5242'] + glob(join(TESTDATA, '[MOP]*'))


class TestDicomWeb(unittest.TestCase):
    """Tests for functions in dicomweb.py"""

    @classmethod
    def setUpClass(cls):
        cls._dockerid = check_output([DCKPROG] + DCKARGS).strip()
        sleep(4)
        check_call([SCUPROG] + SCUARGS, stdout=DEVNULL, stderr=STDOUT)

    @classmethod
    def tearDownClass(cls):
        check_call([DCKPROG, "rm", "-f", cls._dockerid], stdout=DEVNULL, stderr=STDOUT)

    def test_rst_pat_level_find(self):
        patients = rst_pat_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patname='', patid=PATID, birthdate='', sex=''
        )
        self.assertEqual(patients[0].patid, PATID)

    def test_rst_pat_level_find_no_auth(self):
        self.assertRaises(
            HTTPError,
            rst_pat_level_find,
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            patname='', patid=PATID, birthdate='', sex=''
        )

    def test_rst_pat_level_find_old_philips(self):
        patients = rst_pat_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patname='', patid=PATID_C, birthdate='', sex=''
        )
        self.assertEqual(patients[0].patid, PATID_C)

    def test_rst_pat_level_find_philips_examcard(self):
        patients = rst_pat_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patname='', patid=PATID_D, birthdate='', sex=''
        )
        self.assertEqual(patients[0].patid, PATID_D)

    def test_rst_pat_level_find_no_match(self):
        patients = rst_pat_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patname='', patid='XXXXX', birthdate='', sex=''
        )
        self.assertEqual(len(patients), 0)

    def test_rst_stu_level_find(self):
        studies = rst_stu_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patid=PATID
        )
        self.assertEqual(studies[0].studyuid, STUDYUID)

    def test_rst_stu_level_find_no_auth(self):
        self.assertRaises(
            HTTPError,
            rst_stu_level_find,
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            patid=PATID
        )

    def test_rst_stu_level_find_old_philips(self):
        studies = rst_stu_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patid=PATID_C
        )
        self.assertEqual(studies[0].studyuid, STUDYUID_C)

    def test_rst_stu_level_find_philips_examcard(self):
        studies = rst_stu_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            patid=PATID_D
        )
        self.assertEqual(studies[0].studyuid, STUDYUID_D)

    def test_rst_ser_level_find(self):
        series = rst_ser_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID
        )
        self.assertEqual(series[0].seriesuid, SERIESUID)

    def test_rst_ser_level_find_no_auth(self):
        self.assertRaises(
            HTTPError,
            rst_ser_level_find,
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            studyuid=STUDYUID
        )

    def test_rst_ser_level_find_old_philips(self):
        series = rst_ser_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_C
        )
        self.assertEqual(series[0].seriesuid, SERIESUID_C)

    def test_rst_ser_level_find_philips_examcard(self):
        series = rst_ser_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_D
        )
        self.assertEqual(series[0].seriesuid, SERIESUID_D)

    def test_rst_img_level_find(self):
        images = rst_img_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID,
            seriesuid=SERIESUID
        )
        self.assertEqual(len(images), NIMAGES)
        images = sorted(images, key=lambda x: x.imagenumber)
        self.assertEqual(images[0].imageuid, IMAGEUID)

    def test_rst_img_level_find_old_philips(self):
        images = rst_img_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_C,
            seriesuid=SERIESUID_C
        )
        self.assertEqual(len(images), NIMAGES_C)
        images = sorted(images, key=lambda x: x.imagenumber)
        self.assertEqual(images[0].imageuid, IMAGEUID_C)

    def test_rst_img_level_find_philips_examcard(self):
        images = rst_img_level_find(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_D,
            seriesuid=SERIESUID_D
        )
        self.assertEqual(len(images), NIMAGES_D)
        images = sorted(images, key=lambda x: x.imagenumber)
        self.assertEqual(images[0].imageuid, IMAGEUID_D)


    def test_rst_img_level_find_no_auth(self):
        self.assertRaises(
            HTTPError,
            rst_img_level_find,
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            studyuid=STUDYUID,
            seriesuid=SERIESUID
        )

    def test_rst_ser_level_get(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID,
            seriesuid=SERIESUID,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len([int(d.InstanceNumber) for d in dobjs]), NIMAGES)
        rmtree(tempd)

    def test_rst_ser_level_get_no_auth(self):
        # nb generator function, will only do hhtp request when iterated over
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            studyuid=STUDYUID,
            seriesuid=SERIESUID,
            savedir=tempd)
        self.assertRaises(
            HTTPError,
            list,
            fetch_iter
        )
        rmtree(tempd)

    def test_rst_ser_level_get_2(self):
        '''Check two series retrieved to same directory are kept distinct'''
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID,
            seriesuid=SERIESUID,
            savedir=tempd)
        list(fetch_iter)
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_B,
            seriesuid=SERIESUID_B,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len([int(d.InstanceNumber) for d in dobjs]), 2*NIMAGES)
        rmtree(tempd)


    def test_rst_ser_level_get_old_philips(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_C,
            seriesuid=SERIESUID_C,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len([int(d.InstanceNumber) for d in dobjs]), NIMAGES_C)
        rmtree(tempd)

    def test_rst_ser_level_get_philips_examcard(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_ser_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_D,
            seriesuid=SERIESUID_D,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len([int(d.InstanceNumber) for d in dobjs]), NIMAGES_D)
        rmtree(tempd)


    def test_rst_img_level_get(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_img_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID,
            seriesuid=SERIESUID,
            imageuid=IMAGEUID,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len(dobjs), 1)
        self.assertEqual(dobjs[0].InstanceNumber, INSTANCENUMBER)
        rmtree(tempd)

    def test_rst_img_level_get_no_auth(self):
        # nb generator function, will only do hhtp request when iterated over
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_img_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth=None,
            studyuid=STUDYUID,
            seriesuid=SERIESUID,
            imageuid=IMAGEUID,
            savedir=tempd)
        self.assertRaises(
            HTTPError,
            list,
            fetch_iter
        )
        rmtree(tempd)

    def test_rst_img_level_get_old_philips(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_img_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_C,
            seriesuid=SERIESUID_C,
            imageuid=IMAGEUID_C,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len(dobjs), 1)
        self.assertEqual(dobjs[0].InstanceNumber, INSTANCENUMBER_C)
        rmtree(tempd)

    def test_rst_img_level_get_philips_examcard(self):
        tempd = tempfile.mkdtemp()
        fetch_iter = rst_img_level_get(
            endpoint='dicom-web',
            node='localhost',
            port=9042,
            auth='orthanc:orthanc',
            studyuid=STUDYUID_D,
            seriesuid=SERIESUID_D,
            imageuid=IMAGEUID_D,
            savedir=tempd)
        list(fetch_iter)

        dobjs = sorted(
            [dcmread(f) for f in glob(join(tempd, '*'))],
            key=lambda d: int(d.InstanceNumber)
        )
        self.assertEqual(len(dobjs), 1)
        self.assertEqual(dobjs[0].InstanceNumber, INSTANCENUMBER_D)
        rmtree(tempd)


if __name__ == '__main__':
    unittest.main()
