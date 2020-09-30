from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session

boggle_game = Boggle()
