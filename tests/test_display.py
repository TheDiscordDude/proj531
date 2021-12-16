import chess
from io import StringIO
import unittest
import sys
sys.path.append('../src')
sys.path.append('./src')

import display as dp


class Test_display(unittest.TestCase):
    def test_display_board(self):
        board = chess.Board()
        expectedOutput = '\x1b[94mr\x1b[0m \x1b[94mn\x1b[0m \x1b[94mb\x1b[0m \x1b[94mq\x1b[0m \x1b[94mk\x1b[0m \x1b[94mb\x1b[0m \x1b[94mn\x1b[0m \x1b[94mr\x1b[0m\n\x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m \x1b[94mp\x1b[0m\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n\x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m \x1b[96mP\x1b[0m\n\x1b[96mR\x1b[0m \x1b[96mN\x1b[0m \x1b[96mB\x1b[0m \x1b[96mQ\x1b[0m \x1b[96mK\x1b[0m \x1b[96mB\x1b[0m \x1b[96mN\x1b[0m \x1b[96mR\x1b[0m\n'
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        dp.display_board(board)
        sys.stdout = sys.__stdout__
        assert repr(capturedOutput.getvalue()) == repr(expectedOutput)

if __name__=="__main__":
    import nose2
    nose2.main()
