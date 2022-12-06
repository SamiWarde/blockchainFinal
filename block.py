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


@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200
@app.route('/mine', methods=['GET'])
def mine_block():
    blockchain.add_transaction(
        sender = "0",
        patient = None,
        healthInfo = None,
        )
    last_block_hash = blockchain.Block_Hash(blockchain.last_block)
    
    index = len(blockchain.chain)
    t1 = time()
    nonce = blockchain.PoW(index,last_block_hash,blockchain.current_transaction)
    t2 = time()
    block = blockchain.append_block(nonce,last_block_hash)
    tTime = t2-t1
    response = {
        'message': "new block has been added (mined)",
        'index': block['index'],
        'hash_of_previous_block': block['Previous_block_hash'],
        'nonce':block['nonce'],
        'transaction':block['transactions'],
        'time taken in seconds':tTime
        }
    return jsonify(response), 200
@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required_fields = ['sender','patient','healthInfo']
    if not all (k in values for k in required_fields):
        return ('Missing Fields', 400)
    index = blockchain.add_transaction(
        values['sender'],
        values['patient'],
        values['healthInfo'],
        )
    response = {'message': f'Transaction will be added to the block {index}'}
    return (jsonify(response),201)

@app.route('/transactions', methods=['GET'])
def transactions():
    k = blockchain.transactions()
    return(jsonify(k), 200)
    

@app.route('/search', methods=['POST'])
def searchP():
    values = request.get_json()
    required_fields = ['name']
    if not all (k in values for k in required_fields):
        return ('Missing Fields', 400)
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    sendBack = []
    for i in response['chain']:
        for k,v in i.items():
            if(k == 'transactions'):
                for l in v:
                    if((l['patient'] == values['name']) or (l['sender'] == values['name']) ):
                        sendBack.append(l)
    return jsonify(sendBack), 201




if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(8080))
