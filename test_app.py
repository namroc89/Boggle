from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_boggle_board(self):
        with app.test_client() as client:

            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p class='highscore'>Highscore:", html)
            self.assertIn("board", session)
            self.assertIsNone(session.get("times_played"))
            self.assertIsNone(session.get("highscore"))
            self.assertEqual(len(session.get("board")), 5)

    def test_correct_word(self):
        with app.test_client() as client:

            with client.session_transaction() as sess:
                sess["board"] = [['H', 'E', 'L', 'L', 'O'],
                                 ['H', 'E', 'L', 'L', 'O'],
                                 ['H', 'E', 'L', 'L', 'O'],
                                 ['H', 'E', 'L', 'L', 'O'],
                                 ['H', 'E', 'L', 'L', 'O']]
        res = client.get("/check-word?word=hello")
        self.assertEqual(res.json["response"], 'ok')

    def test_incorrect_word(self):
        with app.test_client() as client:
            client.get('/')
            res = client.get("/check-word?word=unicorn")
            self.assertEqual(res.json["response"], 'not-on-board')

    def test_not_word(self):
        with app.test_client() as client:
            client.get('/')
            res = client.get("/check-word?word=esfsgsdfhehwesb")
            self.assertEqual(res.json["response"], 'not-word')

    # def test_posted_highscore(self):
    #     with app.test_client() as client:

    #         client.get('/')
    #         res = client.post("/post-score", {"score": "10"})
