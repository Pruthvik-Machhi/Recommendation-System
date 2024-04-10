import streamlit as st
import pickle
import pandas as pd
import ast

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer