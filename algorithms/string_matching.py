"""String Matching Algorithms"""


def naive_search(text, pattern):
    """Naive String Search - Brute force search"""
    occurrences = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            occurrences.append(i)
    return occurrences


def kmp_search(text, pattern):
    """KMP (Knuth-Morris-Pratt) Search - Uses failure function"""
    
    def build_failure_function(pattern):
        m = len(pattern)
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            
            if pattern[i] == pattern[j]:
                j += 1
            
            failure[i] = j
        
        return failure
    
    n = len(text)
    m = len(pattern)
    failure = build_failure_function(pattern)
    occurrences = []
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            occurrences.append(i - m + 1)
            j = failure[j - 1]
    
    return occurrences


def rabin_karp(text, pattern):
    """Rabin-Karp Search - Uses rolling hash"""
    d = 256  # Size of alphabet
    q = 101  # Prime number for modulo
    
    n = len(text)
    m = len(pattern)
    pattern_hash = 0
    text_hash = 0
    h = 1
    occurrences = []
    
    # Calculate h = d^(m-1) % q
    for i in range(m - 1):
        h = (h * d) % q
    
    # Calculate pattern hash and first window
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q
    
    # Find occurrences
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                occurrences.append(i)
        
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if text_hash < 0:
                text_hash += q
    
    return occurrences


def boyer_moore(text, pattern):
    """Boyer-Moore Search - Starts from right to left"""
    
    def build_bad_char_table(pattern):
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = max(bad_char.get(pattern[i], -1), i)
        return bad_char
    
    n = len(text)
    m = len(pattern)
    bad_char = build_bad_char_table(pattern)
    occurrences = []
    i = 0
    
    while i <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            occurrences.append(i)
            i += 1 if i + m < n else 1
        else:
            bad_char_shift = max(1, j - bad_char.get(text[i + j], -1))
            i += bad_char_shift
    
    return occurrences
