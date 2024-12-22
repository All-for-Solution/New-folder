#
# 
# 
# 
# https://station.jup.ag/docs/apis/swap-api
# reference this document










def swap(self, from_token,to_token, amount, wallet_address, slippage ):
    try:

        decimal = get_spl_token_decimal(from_token)
        buy_amount = int(float(amount)*10** decimal)
        quoteResponse = self.get_quote_solana(from_token,to_token, buy_amount, int(slippage*100))
        url = 'https://quote-api.jup.ag/v6/swap'
        
        payload = {
            'userPublicKey':str(wallet_address),
            'quoteResponse': quoteResponse,
        }

        response = requests.post(url, json=payload)

        data = response.json()
        swapTransaction=data['swapTransaction']
        
        print(swapTransaction)
        
        
        
        obj : WalletAddress = WalletAddress.query.filter_by(address=wallet_address).first()                        
        
        print("😂")
        print(wallet_address)
        print(payload)
        # client = Client("https://mainnet.helius-rpc.com/?api-key=7bb320cb-4879-4a16-87b7-d203523d1782")
        client = Client("https://mainnet.helius-rpc.com/?api-key=7bb320cb-4879-4a16-87b7-d203523d1782")            

        pk_bytes=bytes.fromhex(obj.private_key)                        
        
        sender = Keypair.from_seed(pk_bytes)

        

        
        raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
        signature = sender.sign_message(to_bytes_versioned(raw_transaction.message))
        signed_txn  = VersionedTransaction.populate(raw_transaction.message,[signature])            
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

        transaction_id = json.loads(result.to_json())['result']


        sleep(5)

        elapsed_time = 0
        # while elapsed_time < 30:
        #     response = client.get_transaction(signature, encoding="jsonParsed", max_supported_transaction_version=0,commitment=Confirmed)
        #     if(response.value != None):
        #         return transaction_id                
        #     sleep(2)
        #     elapsed_time += 1
        # return False
        return transaction_id




    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
    except base64.binascii.Error as e:
        print(f"Base64 decoding error")
        return False
    except Exception as e:
        print(f"JSON decode error: {e}")
        return False
    
def swap_sol_direct(self, from_token,to_token, amount, wallet_address, slippage, private_key ):
    try:

        decimal = get_spl_token_decimal(from_token)
        buy_amount = int(float(amount)*10** decimal)

        
        
        quoteResponse = self.get_quote_solana(from_token,to_token, buy_amount, int(slippage*100))
        url = 'https://quote-api.jup.ag/v6/swap'
        
        payload = {
            'userPublicKey':str(wallet_address),
            'quoteResponse': quoteResponse,
        }

        response = requests.post(url, json=payload)

        data = response.json()
        swapTransaction=data['swapTransaction']
        
        print(swapTransaction)
        
        
        

        # client = Client("https://mainnet.helius-rpc.com/?api-key=7bb320cb-4879-4a16-87b7-d203523d1782")
        client = Client("https://mainnet.helius-rpc.com/?api-key=7bb320cb-4879-4a16-87b7-d203523d1782")            
                    
        
        sender = Keypair.from_base58_string(private_key)
        
        print("private_key:")
        print(private_key)

        

        
        raw_transaction = VersionedTransaction.from_bytes(base64.b64decode(swapTransaction))
        signature = sender.sign_message(to_bytes_versioned(raw_transaction.message))
        signed_txn  = VersionedTransaction.populate(raw_transaction.message,[signature])            
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)

        transaction_id = json.loads(result.to_json())['result']


        sleep(5)

        elapsed_time = 0
        # while elapsed_time < 30:
        #     response = client.get_transaction(signature, encoding="jsonParsed", max_supported_transaction_version=0,commitment=Confirmed)
        #     if(response.value != None):
        #         return transaction_id                
        #     sleep(2)
        #     elapsed_time += 1
        # return False
        return transaction_id




    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
    except base64.binascii.Error as e:
        print(f"Base64 decoding error")
        return False
    except Exception as e:
        print(f"JSON decode error: {e}")
        return False

# get quote for token solana
def get_quote_solana(self,input_mint, output_mint, amount, slippage_bps = 50):
    if(input_mint == "So11111111111111111111111111111111111111111"):
        input_mint = "So11111111111111111111111111111111111111112"
    if(output_mint == "So11111111111111111111111111111111111111111"):
        output_mint = "So11111111111111111111111111111111111111112"
    url = (
        'https://quote-api.jup.ag/v6/quote?'
        f'inputMint={input_mint}&'
        f'outputMint={output_mint}&'
        f'amount={amount}&'
        f'slippageBps={slippage_bps}'
    )

    response = requests.get(url)        
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch quote: {response.status_code} - {response.text}")
