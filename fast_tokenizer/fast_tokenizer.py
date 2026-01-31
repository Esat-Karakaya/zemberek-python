import ctypes
import os

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'libfast_tokenizer.so')
lib = ctypes.CDLL(lib_path)

# Define the callback type
CALLBACK_TYPE = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

# Define the function signature
lib.tokenize_to_callback.argtypes = [ctypes.c_char_p, CALLBACK_TYPE]
lib.tokenize_to_callback.restype = None

def tokenize(text: str):
    tokens = []
    
    def callback(token_ptr):
        tokens.append(token_ptr.decode('utf-8'))
        
    # Python callback must be kept alive during the call
    cb_func = CALLBACK_TYPE(callback)
    
    lib.tokenize_to_callback(text.encode('utf-8'), cb_func)
    
    return tokens
