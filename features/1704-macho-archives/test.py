from regression_tests import *
import json

class TestExtractArchiveJson(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        input='20',
        args='--json'
    )

    def test_check_extract_json(self):
        as_json = json.loads(self.retdec_macho_extractor.output)
        self.assertEqual(as_json['architectures'][0]['name'], 'armv7')
        self.assertEqual(as_json['architectures'][0]['index'], 0)
        self.assertEqual(as_json['architectures'][0]['cpuFamily'], 'arm')
        self.assertEqual(as_json['architectures'][0]['supported'], True)
        self.assertEqual(as_json['architectures'][1]['name'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['index'], 1)
        self.assertEqual(as_json['architectures'][1]['cpuFamily'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['supported'], False)

class TestExtractArchiveJsonWithOjects(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        input='20',
        args='--json --objects'
    )

    def test_check_extract_json(self):
        as_json = json.loads(self.retdec_macho_extractor.output)
        self.assertEqual(as_json['architectures'][0]['name'], 'armv7')
        self.assertEqual(as_json['architectures'][0]['index'], 0)
        self.assertEqual(as_json['architectures'][0]['cpuFamily'], 'arm')
        self.assertEqual(as_json['architectures'][0]['supported'], True)
        self.assertEqual(as_json['architectures'][0]['objects'][0]['name'], 'TatvikMpeg2DemuxBitStreamReader.o')
        self.assertEqual(as_json['architectures'][0]['objects'][1]['name'], 'TatvikMpeg2DemuxPESDecoder.o')
        self.assertEqual(as_json['architectures'][0]['objects'][2]['name'], 'TatvikMpeg2TSDemuxer.o')
        self.assertEqual(as_json['architectures'][0]['objects'][3]['name'], 'TatvikTransportStreamParser.o')
        self.assertEqual(as_json['architectures'][1]['name'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['index'], 1)
        self.assertEqual(as_json['architectures'][1]['cpuFamily'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['supported'], False)
        self.assertEqual(as_json['architectures'][1]['objects'][0]['name'], 'TatvikMpeg2DemuxBitStreamReader.o')
        self.assertEqual(as_json['architectures'][1]['objects'][1]['name'], 'TatvikMpeg2DemuxPESDecoder.o')
        self.assertEqual(as_json['architectures'][1]['objects'][2]['name'], 'TatvikMpeg2TSDemuxer.o')
        self.assertEqual(as_json['architectures'][1]['objects'][3]['name'], 'TatvikTransportStreamParser.o')

class TestExtractArchiveWithOjects(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        input='20',
        args='--objects'
    )

    def test_check_extract_json(self):
        self.assertIn('0\tarmv7\tarm\tyes', self.retdec_macho_extractor.output)
        self.assertIn('1\tarm64\tarm64\tno', self.retdec_macho_extractor.output)
        self.assertIn('0\tTatvikMpeg2DemuxBitStreamReader.o', self.retdec_macho_extractor.output)
        self.assertIn('1\tTatvikMpeg2DemuxPESDecoder.o', self.retdec_macho_extractor.output)
        self.assertIn('2\tTatvikMpeg2TSDemuxer.o', self.retdec_macho_extractor.output)
        self.assertIn('3\tTatvikTransportStreamParser.o', self.retdec_macho_extractor.output)

class TestExtractArchivePlain(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        input='20',
        args='--list'
    )

    def test_check_extract_plain(self):
        self.assertIn('0\tarmv7\tarm\tyes', self.retdec_macho_extractor.output)
        self.assertIn('1\tarm64\tarm64\tno', self.retdec_macho_extractor.output)

class TestExtractDetectClassicMacho(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        input='invalid_ar'
    )

    def setUp(self):
        pass

    def test_check_detection_list(self):
        self.assertNotEqual(self.retdec_macho_extractor.return_code, 0)
        self.assertIn('Error: file is not valid Mach-O Universal static library.', self.retdec_macho_extractor.log)

class TestExtractPrintErrorInJson(Test):
    settings = TestSettings(
        tool='retdec-macho-extractor',
        args='--json'
    )

    def setUp(self):
        pass

    def test_check_detection_list(self):
        self.assertNotEqual(self.retdec_macho_extractor.return_code, 0)
        as_json = json.loads(self.retdec_macho_extractor.output)
        self.assertEqual(as_json['error'], 'no input file')

class TestExtractArchiveDecompilationPick(Test):
    settings = TestSettings(
        input='20',
        args=[ '--cleanup', '--cleanup --arch arm' ]
    )

    def setUp(self):
        pass

    def test_check_objet_list(self):
        self.assertNotEqual(self.decompiler.return_code, 0)
        self.assertIn('0\tTatvikMpeg2DemuxBitStreamReader.o', self.decompiler.output)
        self.assertIn('1\tTatvikMpeg2DemuxPESDecoder.o', self.decompiler.output)
        self.assertIn('2\tTatvikMpeg2TSDemuxer.o', self.decompiler.output)
        self.assertIn('3\tTatvikTransportStreamParser.o', self.decompiler.output)

class TestExtractArchiveDecompilationListArchs(Test):
    settings = TestSettings(
        input='20',
        args='--cleanup --arch x86'
    )

    def setUp(self):
        pass

    def test_check_arch_list(self):
        self.assertNotEqual(self.decompiler.return_code, 0)
        self.assertIn('Invalid --arch option "x86". File contains these architecture families:', self.decompiler.output)
        self.assertIn('armv7\tarm\tyes', self.decompiler.output)
        self.assertIn('arm64\tarm64\tno', self.decompiler.output)

class TestExtractArchiveDecompilation(Test):
    settings = TestSettings(
        input='20',
        args=[ '--ar-index 3', '--ar-index 3 --arch arm' ]
    )

    def test_check_decompilation(self):
        assert self.out_c.has_func( '_GetPositionCall' )
        assert self.out_c.has_func( '_MovePositionCall' )

class TestExtractDecompileArchiveJson(Test):
    settings = TestSettings(
        tool='retdec-archive-decompiler.sh',
        input='20',
        args='--list --json'
    )

    def test_check_list(self):
        as_json = json.loads(self.retdec_archive_decompiler_sh.output)
        self.assertEqual(as_json['architectures'][0]['name'], 'armv7')
        self.assertEqual(as_json['architectures'][0]['index'], 0)
        self.assertEqual(as_json['architectures'][0]['cpuFamily'], 'arm')
        self.assertEqual(as_json['architectures'][0]['supported'], True)
        self.assertEqual(as_json['architectures'][0]['objects'][0]['name'], 'TatvikMpeg2DemuxBitStreamReader.o')
        self.assertEqual(as_json['architectures'][0]['objects'][1]['name'], 'TatvikMpeg2DemuxPESDecoder.o')
        self.assertEqual(as_json['architectures'][0]['objects'][2]['name'], 'TatvikMpeg2TSDemuxer.o')
        self.assertEqual(as_json['architectures'][0]['objects'][3]['name'], 'TatvikTransportStreamParser.o')
        self.assertEqual(as_json['architectures'][1]['name'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['index'], 1)
        self.assertEqual(as_json['architectures'][1]['cpuFamily'], 'arm64')
        self.assertEqual(as_json['architectures'][1]['supported'], False)
        self.assertEqual(as_json['architectures'][1]['objects'][0]['name'], 'TatvikMpeg2DemuxBitStreamReader.o')
        self.assertEqual(as_json['architectures'][1]['objects'][1]['name'], 'TatvikMpeg2DemuxPESDecoder.o')
        self.assertEqual(as_json['architectures'][1]['objects'][2]['name'], 'TatvikMpeg2TSDemuxer.o')
        self.assertEqual(as_json['architectures'][1]['objects'][3]['name'], 'TatvikTransportStreamParser.o')

class TestExtractDecompileArchivePlainText(Test):
    settings = TestSettings(
        tool='retdec-archive-decompiler.sh',
        input='20',
        args='--list'
    )

    def test_check_list(self):
        self.assertIn('0\tarmv7\tarm\tyes', self.retdec_archive_decompiler_sh.output)
        self.assertIn('1\tarm64\tarm64\tno', self.retdec_archive_decompiler_sh.output)
        self.assertIn('0\tTatvikMpeg2DemuxBitStreamReader.o', self.retdec_archive_decompiler_sh.output)
        self.assertIn('1\tTatvikMpeg2DemuxPESDecoder.o', self.retdec_archive_decompiler_sh.output)
        self.assertIn('2\tTatvikMpeg2TSDemuxer.o', self.retdec_archive_decompiler_sh.output)
        self.assertIn('3\tTatvikTransportStreamParser.o', self.retdec_archive_decompiler_sh.output)
