#------------ Bibliotecas nativas do Python --------------
import re
from datetime import datetime
import requests
#------------ Bibliotecas externas---------
from flask import Flask, jsonify, request
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   
from entity.cadastro_entity import Base


#------------ Configuração do banco de dados--------
from config.database_config import session

#------------  Orientação de objetos ------------
from dto.cadastro_dto import CadastroDTO
from entity.cadastro_entity import Cadastro
from repository.cadastro_repository import CadastroRepository
from service.cadastro_service import CadastroService
from utils.cadastro_validations import CadastroValidations
from controller.cadastro_controller import app, cadastro_service
from config.database_config import engine, Base


#------------  testes unitarios------------

import json
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from flask.testing import FlaskClient
import pytest
from unittest.mock import MagicMock






