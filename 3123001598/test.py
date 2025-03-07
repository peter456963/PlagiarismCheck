import unittest
import os
import tempfile
import sys
from unittest.mock import patch, mock_open
from main import *

class Test(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.original_file_path = os.path.join(self.test_dir.name, "orig.txt")
        self.plagiarized_file_path = os.path.join(self.test_dir.name, "plag.txt")
        self.answer_file_path = os.path.join(self.test_dir.name, "ans.txt")

    def tearDown(self):
        self.test_dir.cleanup()

    # 测试获得一个可读取的文件内容方法
    def test_get_file_context(self):
        expected_string = "一位真正的作家永远只为内心写作，只有内心才会真实地告诉他，他的自私、他的高尚是多么突出。"
        with open(self.original_file_path, 'w', encoding='utf-8') as f:
            f.write(expected_string)
        self.assertEqual(get_file_context(self.original_file_path), expected_string)

    # 文件不存在的异常测试
    def test_get_file_context_exception(self):
        invalid_path = os.path.join(self.test_dir.name, "invalid_file.txt")
        with self.assertRaises(FileNotFoundError):
            context = get_file_context(invalid_path)
            self.assertEqual(context, None)

    # 测试删除标点符号的方法
    def test_remove_punctuation(self):
        test_cases = [
            ("你好，GDUT！", "你好GDUT"),
            ("《中华人民共和国宪法》", "中华人民共和国宪法"),
            ("、。！？《》【】“”‘’；：·—，!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~", "")
        ]
        for input_string, expected_string in test_cases:
            self.assertEqual(remove_punctuation(input_string), expected_string)

    # 测试分词方法
    def test_tokenize_with_spaces(self):
        test_cases = [
            ("截止期限就要到了", "截止 期限 就要 到 了"),
            ("deadline才是第一生产力", "deadline 才 是 第一 生产力"),
            ("上私塾时我从来不走路都是我家一个雇工背着我去", "上 私塾 时 我 从来不 走路 都 是 我家 一个 雇工 背着 我 去")
        ]
        for input_string, expected_string in test_cases:
            self.assertEqual(tokenize_with_spaces(input_string), expected_string)

    # 测试获得相似度的方法
    def test_get_similarity_score(self):
        test_cases = [
            ("Python单元测试使用unittest框架", "Java开发常用JUnit进行测试", 0, 0.01),
            ("余弦相似度通过TF-IDF向量计算", "TF-IDF向量用于计算文本相似度", 0.5, 0.1),
            ("如何处理标点？例如：“引号”和、顿号！", "如何处理标点 例如 引号 和 顿号", 1, 0.01)
        ]
        for orig, processed, score, d in test_cases:
            self.assertAlmostEqual(get_similarity_score(orig, processed), score, delta=d)


    # 运行主程序，以正确的参数
    def test_main_with_correct_arguments(self):
        test_args = ["main.py", self.original_file_path, self.plagiarized_file_path, self.answer_file_path]

        with open(self.original_file_path, 'w', encoding='utf-8') as f:
            f.write("长期以来，我的作品都是源出于和现实的那一层紧张关系。")

        with open(self.plagiarized_file_path, 'w', encoding='utf-8') as f:
            f.write(" 长期以来，我的作品都是源出于和现实的那一层紧张关系！")

        with patch.object(sys, "argv", test_args):
            main()
            
        self.assertTrue(os.path.exists(self.answer_file_path))
        with open(self.answer_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertRegex(content, r"^\d+\.\d{2}$") 

    # 运行主程序，以不恰当的参数
    def test_main_with_insufficient_arguments(self):
        test_args = ["main.py", "arg1", "arg2"]
        with patch.object(sys, "argv", test_args):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1) 

if __name__ == '__main__':
    unittest.main()