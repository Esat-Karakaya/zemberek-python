import ctypes
import os
from typing import List, Tuple

class StarlangAnalyzer:
    def __init__(self, lib_path: str = None):
        if lib_path is None:
            # Default to the one we expect to build in the same directory
            lib_path = os.path.join(os.path.dirname(__file__), "libstarlang.so")
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Starlang shared library not found at {lib_path}. Please build it first.")
            
        self.lib = ctypes.CDLL(lib_path)
        
        self.lib.starlang_init.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.starlang_init.restype = None
        
        self.lib.starlang_analyze.argtypes = [ctypes.c_char_p]
        self.lib.starlang_analyze.restype = ctypes.c_char_p
        
        self.initialized = False

    def init(self, fsm_path: str, dict_path: str, data_dir: str = ""):
        self.lib.starlang_init(
            fsm_path.encode('utf-8'),
            dict_path.encode('utf-8'),
            data_dir.encode('utf-8') if data_dir else b""
        )
        self.initialized = True

    def analyze(self, text: str) -> List[Tuple[str, str]]:
        if not self.initialized:
            raise RuntimeError("Analyzer not initialized. Call init() first.")
            
        result_ptr = self.lib.starlang_analyze(text.encode('utf-8'))
        if not result_ptr:
            return []
            
        result_str = result_ptr.decode('utf-8')
        lines = result_str.strip().split('\n')
        
        analyses = []
        for line in lines:
            if '|' in line:
                token, analysis = line.split('|', 1)
                analyses.append((token, analysis))
        
        return analyses

# Global instance
_analyzer = None

def init(fsm_path: str = None, dict_path: str = None, data_dir: str = None):
    global _analyzer
    if _analyzer is None:
        # Try to find default paths if not provided
        base_path = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(base_path, "TurkishMorphologicalAnalysis-CPP-master", "build")
        
        if fsm_path is None:
            fsm_path = os.path.join(data_path, "turkish_finite_state_machine.xml")
        if dict_path is None:
            dict_path = os.path.join(data_path, "turkish_dictionary.txt")
        if data_dir is None:
            data_dir = data_path
            
        _analyzer = StarlangAnalyzer()
        _analyzer.init(fsm_path, dict_path, data_dir)

def analyze(text: str) -> List[Tuple[str, str]]:
    if _analyzer is None:
        init()
    return _analyzer.analyze(text)
