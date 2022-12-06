import json
import hashlib
from flask import Flask
from time import  time
from uuid import uuid4
from flask.globals import request
from flask.json import jsonify

class Blockchain(object):
    difficulty_level = "0000"
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        genesis_Hash = self.Block_Hash("genesis_block")
        self.append_block(
            Previous_block_hash = genesis_Hash,
            nonce = self.PoW(0,genesis_Hash, [])
            )
    def Block_Hash(self,block):

        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(blockEncoder).hexdigest()

    def PoW(self,index,Previous_block_hash,transactions):
        nonce=0
        while self.validate_Proof(index,Previous_block_hash,transactions, nonce) is False:
            nonce+=1
            print(nonce)
        print(nonce)
        return nonce
    def validate_Proof(self,index,Previous_block_hash,transactions,nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha512(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level
        
    def append_block(self,nonce, Previous_block_hash):
        block ={
            'index': len(self.chain),
            'transactions':self.current_transaction,
            'timestamp': time(),
            'nonce' : nonce,
            'Previous_block_hash': Previous_block_hash
        }
        self.current_transaction = []
        self.chain.append(block)
        return block
    def add_transaction(self, sender, patient, healthInfo):
        self.current_transaction.append({
            'patient':patient,
            'healthInfo':healthInfo,
            'sender':sender
            })
        return self.last_block['index']+1
    
    def transactions(self):
        return self.current_transaction

    @property
    def last_block(self):
        return self.chain[-1]


app = Flask(__name__)
node_identifier = str(uuid4()).replace('-',"")
blockchain = Blockchain()
